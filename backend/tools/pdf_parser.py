"""
PDF Parser: Extracts structured sections from academic PDFs
using PyMuPDF with heuristic heading detection.
"""
import re
import fitz  # PyMuPDF
from typing import Dict, List


SECTION_KEYWORDS = {
    "abstract": ["abstract"],
    "introduction": ["introduction", "1 introduction", "1. introduction"],
    "method": [
        "method", "methods", "methodology", "approach", "proposed method",
        "2 method", "3 method", "2. method", "3. method",
        "2 approach", "3 approach",
    ],
    "results": [
        "results", "experiments", "experimental results", "evaluation",
        "4 results", "5 results", "4. results", "5. results",
    ],
    "conclusion": [
        "conclusion", "conclusions", "concluding remarks",
        "5 conclusion", "6 conclusion", "5. conclusion", "6. conclusion",
    ],
    "references": ["references", "bibliography"],
}


def _is_heading(text: str, font_size: float, avg_font_size: float) -> bool:
    """Heuristic: a line is a heading if it's larger/bolder than average or matches a keyword."""
    stripped = text.strip().lower()
    if font_size > avg_font_size * 1.1 and len(stripped) < 120:
        return True
    for keywords in SECTION_KEYWORDS.values():
        for kw in keywords:
            if stripped == kw or stripped.startswith(kw + " "):
                return True
    return False


def _classify_heading(text: str) -> str | None:
    """Map a heading text to a known section key."""
    stripped = text.strip().lower()
    for section, keywords in SECTION_KEYWORDS.items():
        for kw in keywords:
            if stripped == kw or stripped.startswith(kw):
                return section
    return None


def extract_text_blocks(pdf_path: str) -> List[Dict]:
    """Extract text blocks with font size info from a PDF."""
    doc = fitz.open(pdf_path)
    blocks = []
    for page in doc:
        page_dict = page.get_text("dict")
        for block in page_dict.get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                line_text = ""
                max_size = 0.0
                for span in line.get("spans", []):
                    line_text += span.get("text", "")
                    max_size = max(max_size, span.get("size", 0))
                if line_text.strip():
                    blocks.append({"text": line_text, "size": max_size})
    doc.close()
    return blocks


def parse_pdf(pdf_path: str) -> Dict[str, str]:
    """
    Parse a PDF and return a dict with keys:
    title, abstract, introduction, method, results, conclusion, references, full_text
    """
    blocks = extract_text_blocks(pdf_path)

    if not blocks:
        return {k: "" for k in ["title", "abstract", "introduction", "method", "results", "conclusion", "references", "full_text"]}

    sizes = [b["size"] for b in blocks if b["size"] > 0]
    avg_size = sum(sizes) / len(sizes) if sizes else 12.0
    max_size = max(sizes) if sizes else 12.0

    # Title heuristic: largest font in first 30 blocks
    title_blocks = blocks[:30]
    title_candidates = [b for b in title_blocks if b["size"] >= max_size * 0.85]
    title = " ".join(b["text"].strip() for b in title_candidates[:4]).strip()

    sections: Dict[str, List[str]] = {k: [] for k in SECTION_KEYWORDS}
    current_section = None
    full_lines = []

    for block in blocks:
        text = block["text"].strip()
        size = block["size"]
        full_lines.append(text)

        if _is_heading(text, size, avg_size):
            classified = _classify_heading(text)
            if classified:
                current_section = classified
                continue

        if current_section:
            sections[current_section].append(text)

    result = {"title": title}
    for key in SECTION_KEYWORDS:
        result[key] = "\n".join(sections[key]).strip()

    result["full_text"] = "\n".join(full_lines).strip()
    return result


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> List[str]:
    """Split text into overlapping chunks by word count."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks
