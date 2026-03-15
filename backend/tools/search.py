"""
Search tool: Queries Semantic Scholar, arXiv, and DuckDuckGo.
Returns normalized paper dicts with title, authors, abstract, url.
"""
import arxiv
import httpx
from typing import List, Dict, Optional
from duckduckgo_search import DDGS


def semantic_scholar_search(query: str, limit: int = 10) -> List[Dict]:
    """Search Semantic Scholar public API for papers."""
    results = []
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,abstract,year,url,externalIds",
        }
        response = httpx.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        for paper in data.get("data", []):
            authors = [a.get("name", "") for a in paper.get("authors", [])]
            results.append({
                "title": paper.get("title", ""),
                "authors": authors,
                "abstract": paper.get("abstract", "") or "",
                "year": paper.get("year"),
                "url": paper.get("url", ""),
                "source": "semantic_scholar",
            })
    except Exception as e:
        print(f"[SemanticScholar] Error: {e}")
    return results


def arxiv_search(query: str, max_results: int = 10) -> List[Dict]:
    """Search arXiv for papers."""
    results = []
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        for paper in client.results(search):
            results.append({
                "title": paper.title,
                "authors": [str(a) for a in paper.authors],
                "abstract": paper.summary,
                "year": paper.published.year if paper.published else None,
                "url": paper.entry_id,
                "source": "arxiv",
            })
    except Exception as e:
        print(f"[arXiv] Error: {e}")
    return results


def duckduckgo_search(query: str, max_results: int = 5) -> List[Dict]:
    """Web search via DuckDuckGo (no API key required)."""
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "source": "duckduckgo",
                })
    except Exception as e:
        print(f"[DuckDuckGo] Error: {e}")
    return results


def unified_paper_search(query: str, limit: int = 8) -> List[Dict]:
    """
    Search both Semantic Scholar and arXiv and deduplicate by title.
    Returns up to `limit` results.
    """
    ss_results = semantic_scholar_search(query, limit=limit)
    ax_results = arxiv_search(query, max_results=limit)

    seen_titles = set()
    combined = []
    for paper in ss_results + ax_results:
        title_key = paper["title"].lower().strip()
        if title_key and title_key not in seen_titles:
            seen_titles.add(title_key)
            combined.append(paper)
        if len(combined) >= limit:
            break
    return combined
