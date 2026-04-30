from nova_engine import call_nova_mcq, parse_nova_json
from config import EXAM_CONFIG

MCQ_PROMPTS = {
    "upsc": """
Generate {count} UPSC Prelims-style MCQs on: "{topic}"

Rules:
- 4 options labeled (a)(b)(c)(d)
- Use statement-based format: "Consider the following statements..."
- Mix conceptual, analytical, factual
- Negative marking 1/3 — plausible distractors required
- One question must test a government scheme or policy

Respond ONLY with this exact JSON:
{{
  "exam": "UPSC Prelims",
  "topic": "{topic}",
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": {{"a": "...", "b": "...", "c": "...", "d": "..."}},
      "correct": "a",
      "explanation": "One-line explanation",
      "difficulty": "medium"
    }}
  ]
}}
""",

    "nda": """
Generate {count} NDA-style MCQs on: "{topic}"

Rules: 4 options (A)(B)(C)(D), direct factual recall,
WHO/WHAT/WHERE/WHEN format, moderate difficulty.

Respond ONLY with JSON:
{{
  "exam": "NDA",
  "topic": "{topic}",
  "questions": [
    {{
      "id": 1,
      "question": "...",
      "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
      "correct": "A",
      "explanation": "...",
      "difficulty": "easy"
    }}
  ]
}}
""",

    "cds": """
Generate {count} CDS-style MCQs on: "{topic}"
Similar to NDA but include some 2-step reasoning questions.
Same JSON structure as NDA, use "exam": "CDS"
""",

    "afcat": """
Generate {count} AFCAT-style MCQs on: "{topic}"
Focus on General Awareness, Science, Defence, Aviation.
Same JSON structure as NDA, use "exam": "AFCAT"
""",

    "ssc": """
Generate {count} SSC CGL-style MCQs on: "{topic}"
Simple 4-option, one-line questions, quick recall, easy-medium difficulty.
Same JSON structure as NDA, use "exam": "SSC CGL"
""",

    "gate": """
Generate {count} GATE-style MCQs on: "{topic}"
Technical questions, mix of MCQ and numerical answer type.
Same JSON structure as NDA, use "exam": "GATE"
"""
}

async def generate_mcqs(exam: str, topic: str, count: int = 5) -> dict:
    template = MCQ_PROMPTS.get(exam, MCQ_PROMPTS["upsc"])
    prompt = template.format(count=count, topic=topic)

    raw = await call_nova_mcq(prompt)
    result = parse_nova_json(raw)
    result["exam_full_name"] = EXAM_CONFIG.get(exam, {}).get("name", exam.upper())
    result["powered_by"] = "Amazon Nova 2 Lite"
    return result