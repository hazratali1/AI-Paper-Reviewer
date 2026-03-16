"""
FastAPI Routes: Handles PDF upload and full paper analysis pipeline.
"""
import os
import uuid
import json
import shutil
import time
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from groq import AuthenticationError, APIError, RateLimitError
from tools.pdf_parser import parse_pdf, chunk_text
from rag.embeddings import create_paper_index
from agents.analyzer import analyze_paper
from agents.reviewer import review_paper
from agents.novelty_agent import detect_novelty
from agents.literature_agent import generate_literature_review
from agents.paper_recommendation_agent import recommend_papers
from tools.search import unified_paper_search

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

# Temp storage directory for uploaded papers
UPLOAD_DIR = Path("./uploaded_papers")
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory store: paper_id -> parsed paper data
paper_store: dict = {}

# Auto-cleanup window for RAG memory (7 days)
RAG_RETENTION_SECONDS = 7 * 24 * 60 * 60


def should_build_rag_index_on_upload() -> bool:
    """Enable index build by env override; default to off on Hugging Face Spaces."""
    env_value = os.getenv("RAG_BUILD_ON_UPLOAD")
    if env_value is not None:
        return env_value.strip().lower() in {"1", "true", "yes", "on"}
    return not bool(os.getenv("SPACE_ID"))


def cleanup_expired_rag_memory() -> None:
    """Delete uploaded paper data and in-memory entries older than retention period."""
    now = time.time()

    # Clean on-disk uploaded paper folders (including FAISS indexes)
    for paper_dir in UPLOAD_DIR.iterdir():
        if not paper_dir.is_dir():
            continue
        try:
            age_seconds = now - paper_dir.stat().st_mtime
            if age_seconds > RAG_RETENTION_SECONDS:
                shutil.rmtree(paper_dir, ignore_errors=True)
        except Exception as e:
            print(f"[Warning] Failed to clean expired paper dir {paper_dir}: {e}")

    # Clean in-memory paper cache entries by creation time
    expired_ids = []
    for paper_id, data in paper_store.items():
        created_at = data.get("created_at", now)
        if now - created_at > RAG_RETENTION_SECONDS:
            expired_ids.append(paper_id)

    for paper_id in expired_ids:
        paper_store.pop(paper_id, None)


class AnalyzeRequest(BaseModel):
    paper_id: str


@router.post("/upload")
async def upload_paper(file: UploadFile = File(...)):
    """
    Upload a PDF research paper.
    Returns a paper_id for subsequent analysis.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    cleanup_expired_rag_memory()

    # Check file size (max 20MB)
    contents = await file.read()
    if len(contents) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 20MB limit.")

    paper_id = str(uuid.uuid4())
    paper_dir = UPLOAD_DIR / paper_id
    paper_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = paper_dir / "paper.pdf"
    with open(pdf_path, "wb") as f:
        f.write(contents)

    # Parse PDF immediately
    try:
        parsed = parse_pdf(str(pdf_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

    # Build RAG index from paper chunks. This is heavy and can time out on free Spaces.
    full_text = parsed.get("full_text", "")
    if full_text and should_build_rag_index_on_upload():
        chunks = chunk_text(full_text, chunk_size=512, overlap=64)
        try:
            create_paper_index(chunks, str(paper_dir / "faiss"))
        except Exception as e:
            print(f"[Warning] RAG index build failed: {e}")
    elif full_text:
        print("[Info] Skipping RAG index build on upload.")

    paper_store[paper_id] = {
        "parsed": parsed,
        "pdf_path": str(pdf_path),
        "paper_dir": str(paper_dir),
        "created_at": time.time(),
    }

    return JSONResponse({
        "paper_id": paper_id,
        "title": parsed.get("title", "Unknown"),
        "has_abstract": bool(parsed.get("abstract")),
        "message": "Paper uploaded and parsed successfully.",
    })


@router.post("/analyze")
async def analyze_paper_endpoint(request: AnalyzeRequest):
    """
    Run all five AI agents on the uploaded paper.
    Returns the complete analysis report.
    """
    paper_id = request.paper_id
    cleanup_expired_rag_memory()

    if paper_id not in paper_store:
        raise HTTPException(status_code=404, detail="Paper not found. Please upload first.")

    data = paper_store[paper_id]
    parsed = data["parsed"]

    try:
        # Step 1: Analyze paper
        analysis = analyze_paper(parsed)

        # Step 2: Generate peer review
        review = review_paper(parsed, analysis)

        # Step 3: Search related papers
        query = f"{parsed.get('title', '')} {analysis.get('research_problem', '')}"
        related_papers = unified_paper_search(query[:200], limit=10)

        # Step 4: Literature review
        lit_review = generate_literature_review(parsed, analysis)

        # Step 5: Novelty detection
        novelty = detect_novelty(parsed, analysis, related_papers)

        # Step 6: Paper recommendations
        recommendations = recommend_papers(parsed, analysis)

        report = {
            "paper_id": paper_id,
            "title": parsed.get("title", "Unknown"),
            "analysis": analysis,
            "review": review,
            "literature_review": lit_review,
            "novelty": novelty,
            "related_papers": recommendations,
        }

        return JSONResponse(report)

    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid Groq API Key. Please check your .env file.")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Groq API Rate Limit Reached. Please wait a moment or upgrade your plan.")
    except APIError as e:
        raise HTTPException(status_code=502, detail=f"Groq API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/paper/{paper_id}")
async def get_paper_info(paper_id: str):
    """Get basic info about an uploaded paper."""
    cleanup_expired_rag_memory()

    if paper_id not in paper_store:
        raise HTTPException(status_code=404, detail="Paper not found.")
    parsed = paper_store[paper_id]["parsed"]
    return {
        "paper_id": paper_id,
        "title": parsed.get("title", "Unknown"),
        "abstract_preview": parsed.get("abstract", "")[:300],
    }


@router.delete("/paper/{paper_id}")
async def delete_paper(paper_id: str):
    """Delete an uploaded paper and its index."""
    cleanup_expired_rag_memory()

    if paper_id not in paper_store:
        raise HTTPException(status_code=404, detail="Paper not found.")
    data = paper_store.pop(paper_id)
    paper_dir = Path(data["paper_dir"])
    if paper_dir.exists():
        shutil.rmtree(paper_dir)
    return {"message": "Paper deleted successfully."}
