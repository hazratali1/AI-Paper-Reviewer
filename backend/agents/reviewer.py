"""
Reviewer Agent: Generates structured peer-review feedback
in the style of a top academic conference like NeurIPS or ICML.
"""
import os
import json
from groq import Groq
from typing import Dict

def get_client():
    return Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

SYSTEM_PROMPT = """You are a senior reviewer for a top-tier AI/ML conference (NeurIPS, ICML, ICLR).
Generate a thorough academic peer review of the given paper in the following JSON format:
{
  "summary": "Brief summary of what the paper does",
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "weaknesses": ["weakness 1", "weakness 2", "weakness 3"],
  "methodology_evaluation": "Detailed evaluation of the methodology",
  "clarity_score": 7,
  "technical_quality_score": 7,
  "novelty_rating": "moderate",
  "questions_for_authors": ["question 1", "question 2"],
  "recommendation": "accept/reject/major_revision/minor_revision",
  "recommendation_reason": "Explanation of the recommendation"
}
Scores are 1-10. novelty_rating is one of: low, moderate, high, very_high.
Return ONLY valid JSON."""


def review_paper(paper: Dict[str, str], analysis: Dict) -> Dict:
    """
    Generate peer-review feedback for a paper.
    paper: raw sections dict; analysis: output from analyzer agent
    """
    paper_snapshot = f"""
TITLE: {paper.get('title', 'N/A')}

ABSTRACT:
{paper.get('abstract', '')[:1500]}

METHOD:
{paper.get('method', '')[:1500]}

RESULTS:
{paper.get('results', '')[:1000]}

KNOWN CONTRIBUTIONS:
{json.dumps(analysis.get('contributions', []))}

KNOWN LIMITATIONS:
{analysis.get('limitations', 'Not stated')}
""".strip()

    client = get_client()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Write a detailed peer review for this paper:\n\n{paper_snapshot}"},
        ],
        temperature=0.4,
        max_tokens=1500,
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
            "summary": content[:400],
            "strengths": [],
            "weaknesses": [],
            "methodology_evaluation": "",
            "clarity_score": 5,
            "technical_quality_score": 5,
            "novelty_rating": "moderate",
            "questions_for_authors": [],
            "recommendation": "major_revision",
            "recommendation_reason": "",
        }
