"""
FastAPI Routes: Handles PDF upload and full paper analysis pipeline.
"""
import os
import uuid
import json
import shutil
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

    # Build RAG index from paper chunks
    full_text = parsed.get("full_text", "")
    if full_text:
        chunks = chunk_text(full_text, chunk_size=512, overlap=64)
        try:
            create_paper_index(chunks, str(paper_dir / "faiss"))
        except Exception as e:
            print(f"[Warning] RAG index build failed: {e}")

    paper_store[paper_id] = {
        "parsed": parsed,
        "pdf_path": str(pdf_path),
        "paper_dir": str(paper_dir),
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
    if paper_id not in paper_store:
        raise HTTPException(status_code=404, detail="Paper not found.")
    data = paper_store.pop(paper_id)
    paper_dir = Path(data["paper_dir"])
    if paper_dir.exists():
        shutil.rmtree(paper_dir)
    return {"message": "Paper deleted successfully."}
