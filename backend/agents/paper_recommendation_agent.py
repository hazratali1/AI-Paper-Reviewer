"""
Paper Recommendation Agent: Retrieves and ranks the top 5 most relevant papers,
generating a tailored summary and relevance explanation for each.
"""
import json
from typing import Dict, List
from tools.llm_client import get_groq_client
from tools.search import unified_paper_search

SYSTEM_PROMPT = """You are an expert research librarian. Given an uploaded research paper and
a list of candidate related papers, select the TOP 5 most relevant papers and explain why
each is relevant. Return your response as JSON:
{
  "recommended_papers": [
    {
      "title": "Paper title",
      "authors": ["Author 1", "Author 2"],
      "year": 2023,
      "summary": "2-3 sentence summary of this paper",
      "relevance": "Why this paper is relevant to the uploaded paper",
      "url": "paper url if available"
    }
  ]
}
Return exactly 5 papers. Return ONLY valid JSON."""


def recommend_papers(paper: Dict[str, str], analysis: Dict) -> Dict:
    """
    Find and rank the top 5 most relevant papers for the uploaded paper.
    """
    query = f"{paper.get('title', '')} {' '.join(analysis.get('contributions', []))}"
    query = query[:200].strip()

    candidates = unified_paper_search(query, limit=12)

    # Build candidates text for LLM
    candidates_text = ""
    for i, rp in enumerate(candidates[:10], 1):
        candidates_text += f"\n[{i}] Title: {rp.get('title', 'Unknown')}\n"
        candidates_text += f"    Authors: {', '.join(rp.get('authors', [])[:3])}\n"
        candidates_text += f"    Year: {rp.get('year', 'N/A')}\n"
        candidates_text += f"    URL: {rp.get('url', '')}\n"
        abstract = rp.get("abstract", "")[:400]
        if abstract:
            candidates_text += f"    Abstract: {abstract}\n"

    prompt = f"""
UPLOADED PAPER: {paper.get('title', 'N/A')}

CONTRIBUTIONS:
{chr(10).join(f'- {c}' for c in analysis.get('contributions', []))}

CANDIDATE RELATED PAPERS:
{candidates_text if candidates_text else 'No candidates found. Generate recommendations based on the topic.'}

Select and rank the top 5 most relevant papers from the candidates above.
If fewer than 5 candidates are available, you may generate plausible recommendations.
"""

    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=2000,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Fallback: return top candidates directly
        top_5 = candidates[:5]
        return {
            "recommended_papers": [
                {
                    "title": rp.get("title", ""),
                    "authors": rp.get("authors", []),
                    "year": rp.get("year"),
                    "summary": rp.get("abstract", "")[:300],
                    "relevance": "Related to the paper's topic",
                    "url": rp.get("url", ""),
                }
                for rp in top_5
            ]
        }
