"""
Novelty Detection Agent: Compares the uploaded paper's contributions
with retrieved similar papers to detect novel vs overlapping work.
Outputs a novelty score (0-10) and detailed breakdown.
"""
import os
import json
from groq import Groq
from typing import Dict, List

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

SYSTEM_PROMPT = """You are an expert at analyzing research novelty and originality.
Given an uploaded paper's contributions and a set of related existing papers,
assess the novelty of the uploaded paper.

Return your assessment in the following JSON format:
{
  "novelty_score": 7.5,
  "verdict": "High Novelty",
  "novel_contributions": [
    "Specific novel aspect 1",
    "Specific novel aspect 2"
  ],
  "overlapping_aspects": [
    "Aspect that overlaps with existing work and with which paper"
  ],
  "innovation_type": "Incremental / Significant / Transformative",
  "comparison_summary": "2-3 sentence summary comparing this paper to related work",
  "missing_comparisons": ["Paper or method that should be compared but is missing"]
}
novelty_score is a float 0.0-10.0. Return ONLY valid JSON."""


def detect_novelty(paper: Dict[str, str], analysis: Dict, related_papers: List[Dict]) -> Dict:
    """
    Compare the paper's contributions against related papers and score novelty.
    related_papers: list of dicts with title, abstract, authors
    """
    # Build related papers snippet
    related_text = ""
    for i, rp in enumerate(related_papers[:6], 1):
        related_text += f"\n[{i}] {rp.get('title', 'Unknown')}\n"
        related_text += f"    Abstract: {rp.get('abstract', '')[:400]}\n"

    contributions_text = "\n".join(
        f"- {c}" for c in analysis.get("contributions", [])
    ) or analysis.get("summary", "")

    prompt = f"""
UPLOADED PAPER TITLE: {paper.get('title', 'N/A')}

CLAIMED CONTRIBUTIONS:
{contributions_text}

RESEARCH PROBLEM:
{analysis.get('research_problem', '')}

METHOD SUMMARY:
{analysis.get('method', '')}

RELATED / EXISTING PAPERS:
{related_text}

Assess the novelty of the uploaded paper relative to the existing work above.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    content = response.choices[0].message.content.strip()
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "novelty_score": 5.0,
            "verdict": "Moderate Novelty",
            "novel_contributions": [],
            "overlapping_aspects": [],
            "innovation_type": "Incremental",
            "comparison_summary": content[:300],
            "missing_comparisons": [],
        }
