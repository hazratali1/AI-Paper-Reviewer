"""
Scraper: Fetches and parses text from arXiv HTML abstract pages.
"""
import httpx
from bs4 import BeautifulSoup
from typing import Optional


def fetch_arxiv_abstract(arxiv_url: str) -> Optional[str]:
    """
    Fetch the abstract text from an arXiv page.
    Accepts abs or html URLs.
    """
    try:
        # Normalize to abs URL
        url = arxiv_url.replace("/pdf/", "/abs/").replace(".pdf", "")
        response = httpx.get(url, timeout=15, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # arXiv abstract page
        abstract_block = soup.find("blockquote", class_="abstract")
        if abstract_block:
            return abstract_block.get_text(separator=" ", strip=True).replace("Abstract:", "").strip()

        # Fallback: first large paragraph
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 100:
                return text
    except Exception as e:
        print(f"[Scraper] Error fetching {arxiv_url}: {e}")
    return None


def fetch_page_text(url: str, max_chars: int = 3000) -> Optional[str]:
    """Generic page text fetcher, returns first max_chars characters."""
    try:
        response = httpx.get(url, timeout=15, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Remove scripts and styles
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n", strip=True)
        return text[:max_chars]
    except Exception as e:
        print(f"[Scraper] Error fetching {url}: {e}")
    return None
