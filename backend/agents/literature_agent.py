"""
Literature Review Agent: Searches for related papers via Semantic Scholar / arXiv,
then synthesizes a structured literature review using Groq.
"""
import os
import json
from groq import Groq
from typing import Dict, List
from tools.search import unified_paper_search

def get_client():
    return Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

SYSTEM_PROMPT = """You are an expert academic writer specializing in literature reviews.
Given a research topic and a set of related papers, write a structured 3-4 paragraph
literature review. Return your response as JSON in this format:
{
  "literature_review": "Full 3-4 paragraph literature review text",
  "research_trends": ["Trend 1", "Trend 2", "Trend 3"],
  "existing_limitations": ["Limitation 1", "Limitation 2"],
  "key_references": [
    {"title": "Paper title", "contribution": "Why it matters"}
  ]
}
The literature review should discuss: prior work, methodology comparisons, trends, and gaps.
Return ONLY valid JSON."""


def generate_literature_review(paper: Dict[str, str], analysis: Dict) -> Dict:
    """
    Search for related papers and synthesize a literature review.
    Returns structured dict with literature_review, trends, limitations, references.
    """
    # Build search query from paper topic
    query = f"{paper.get('title', '')} {analysis.get('research_problem', '')}"
    query = query[:200].strip()

    related_papers = unified_paper_search(query, limit=8)

    related_text = ""
    for i, rp in enumerate(related_papers[:6], 1):
        related_text += f"\n[{i}] Title: {rp.get('title', 'Unknown')}\n"
        abstract = rp.get("abstract", "")[:500]
        if abstract:
            related_text += f"    Abstract: {abstract}\n"

    prompt = f"""
RESEARCH PAPER TOPIC: {paper.get('title', 'N/A')}

RESEARCH PROBLEM: {analysis.get('research_problem', '')}

MAIN METHOD: {analysis.get('method', '')}

RELATED PAPERS FOUND:
{related_text if related_text else 'No related papers found. Write a general literature review based on the topic.'}

Write a comprehensive literature review synthesizing the above information.
"""

    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=4000,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    try:
        result = json.loads(content)
        result["related_papers_fetched"] = related_papers
        return result
    except json.JSONDecodeError:
        # Robust extraction for broken/truncated JSON
        import re
        
        def extract_list(key, text):
            # Try to match ["item1", "item2" ... ]
            match = re.search(f'"{key}"\\s*:\\s*\\[([\\s\\S]*?)\\]', text)
            if match:
                items_str = match.group(1)
                # Split by commas and clean up quotes/whitespace
                items = [i.strip().strip('"').strip("'") for i in items_str.split(',') if i.strip()]
                return [i for i in items if i]
            return []

        def extract_text(key, text):
            match = re.search(f'"{key}"\\s*:\\s*"([\\s\\S]*?)"', text)
            if match: return match.group(1)
            # Fallback for truncated content
            match = re.search(f'"{key}"\\s*:\\s*"([\\s\\S]*)', text)
            if match: return match.group(1).replace('"}', '').strip().rstrip('"')
            return text

        return {
            "literature_review": extract_text("literature_review", content),
            "research_trends": extract_list("research_trends", content),
            "existing_limitations": extract_list("existing_limitations", content),
            "key_references": [],
            "related_papers_fetched": related_papers,
        }
