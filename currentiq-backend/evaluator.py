from nova_engine import call_nova_eval, parse_nova_json

EVALUATION_PROMPT = """
You are a senior UPSC examiner with 20 years of Mains evaluation experience.

QUESTION: {question}
WORD LIMIT: {word_limit} words

STUDENT'S ANSWER:
---
{answer}
---

Evaluate strictly on UPSC Mains criteria. Score each criterion:

1. INTRODUCTION (0-2): Key terms defined? Contextualised?
2. BODY CONTENT (0-3): Facts accurate? Multiple dimensions covered (economic/social/political)?
3. ANALYSIS DEPTH (0-2): Beyond facts? Causes, effects, implications analysed?
4. BALANCED PERSPECTIVE (0-1): Both sides / multiple views presented?
5. CONCLUSION (0-1): Forward-looking or solution-oriented?
6. LANGUAGE & STRUCTURE (0-1): Clarity, flow, word limit adherence

Provide:
- "strengths": 2-3 things done well
- "improvements": 3-4 specific actionable suggestions
- "model_intro": One sample introductory sentence they could use
- "missed_points": Key points that should have been included
- "overall_grade": A/B/C/D with one-line reasoning

Respond ONLY with this exact JSON:
{{
  "scores": {{
    "introduction": 0,
    "body_content": 0,
    "analysis_depth": 0,
    "balanced_perspective": 0,
    "conclusion": 0,
    "language_structure": 0
  }},
  "total": 0,
  "max_total": 10,
  "overall_grade": "B",
  "grade_reasoning": "...",
  "strengths": ["..."],
  "improvements": ["..."],
  "model_intro": "...",
  "missed_points": ["..."],
  "word_limit_feedback": "Within limit / Over by X words"
}}
"""

async def evaluate_answer(question: str, answer: str, word_limit: int = 150) -> dict:
    word_count = len(answer.split())
    prompt = EVALUATION_PROMPT.format(
        question=question,
        answer=answer,
        word_limit=word_limit
    )

    raw = await call_nova_eval(prompt)
    result = parse_nova_json(raw)
    result["word_count_actual"] = word_count
    result["question"] = question
    result["powered_by"] = "Amazon Nova 2 Lite"
    return result