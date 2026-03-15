"""
Paper Analyzer Agent: Summarizes the paper, extracts contributions,
identifies the research problem, method, and results.
"""
import os
from groq import Groq
from typing import Dict

client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

SYSTEM_PROMPT = """You are an expert academic research analyst. 
Given a research paper's text, extract and return a structured analysis in the following JSON format:
{
  "summary": "2-3 sentence concise summary of the paper",
  "research_problem": "The main problem or question the paper addresses",
  "detailed_methodology": "A comprehensive, highly detailed multi-paragraph description of the methodology or approach used. Do not be brief.",
  "contributions": ["contribution 1", "contribution 2", "contribution 3"],
  "results": "Key results and findings",
  "datasets": "Datasets used (if any)",
  "limitations": ["First explicit limitation", "Second explicit limitation"],
  "future_scope": ["A specific, actionable improvement point", "A suggested extension of the work", "A potential follow-up study direction"]
}
Return ONLY valid JSON. Ensure 'future_scope' contains all possible forward-looking improvements derived from the paper's current limitations and potential follow-up work.
Return ONLY valid JSON, no markdown, no extra text."""


def analyze_paper(paper: Dict[str, str]) -> Dict:
    """
    Analyze a parsed paper dict and return structured analysis.
    paper keys: title, abstract, introduction, method, results, conclusion
    """
    # Build a concise paper snapshot
    paper_text = f"""
TITLE: {paper.get('title', 'N/A')}

ABSTRACT:
{paper.get('abstract', '')[:1500]}

INTRODUCTION:
{paper.get('introduction', '')[:1000]}

METHOD:
{paper.get('method', '')[:1500]}

RESULTS:
{paper.get('results', '')[:1000]}

CONCLUSION:
{paper.get('conclusion', '')[:800]}
""".strip()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyze this research paper:\n\n{paper_text}"},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    import json
    content = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Robust extraction for broken/truncated JSON
        import re
        
        def extract_list(key, text):
            match = re.search(f'"{key}"\\s*:\\s*\\[([\\s\\S]*?)\\]', text)
            if match:
                items_str = match.group(1)
                items = [i.strip().strip('"').strip("'") for i in items_str.split(',') if i.strip()]
                return [i for i in items if i]
            return []

        def extract_text(key, text):
            match = re.search(f'"{key}"\\s*:\\s*"([\\s\\S]*?)"', text)
            if match: return match.group(1).replace('\\n', '\n').replace('\\"', '"')
            # Fallback for truncated
            match = re.search(f'"{key}"\\s*:\\s*"([\\s\\S]*)', text)
            if match: return match.group(1).replace('"}', '').strip().rstrip('"').replace('\\n', '\n').replace('\\"', '"')
            return ""

        return {
            "summary": extract_text("summary", content) or content[:2000],
            "research_problem": extract_text("research_problem", content),
            "detailed_methodology": extract_text("detailed_methodology", content),
            "contributions": extract_list("contributions", content),
            "results": extract_text("results", content),
            "datasets": extract_text("datasets", content),
            "limitations": extract_list("limitations", content),
            "future_scope": extract_list("future_scope", content),
        }
