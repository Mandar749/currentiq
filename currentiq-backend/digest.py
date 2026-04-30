from nova_engine import call_nova_digest, parse_nova_json
from news_fetcher import fetch_articles_for_exam
from config import EXAM_CONFIG
from typing import Optional
from datetime import date

DIGEST_PROMPTS = {
    "upsc": """
You are a senior IAS officer and UPSC mentor.
Given these news article headlines and summaries, create a UPSC Current Affairs Digest.

For each important story (pick top 5-7), provide:
- "headline": Short descriptive headline
- "gs_paper": Which GS paper (GS1/GS2/GS3/GS4) or "Prelims"
- "topic_tag": Subject tag (Polity/Economy/IR/Environment/Science/etc)
- "summary": 3-sentence analytical summary
- "upsc_angle": Why this matters for UPSC - linked scheme, act, or concept
- "key_facts": Array of 3-4 bullet point facts
- "mains_relevance": One sentence on Mains application

Respond ONLY with this exact JSON:
{
  "exam": "UPSC",
  "date": "today",
  "digest_items": [
    {
      "headline": "...", "gs_paper": "GS2", "topic_tag": "Polity",
      "summary": "...", "upsc_angle": "...",
      "key_facts": ["...", "..."], "mains_relevance": "..."
    }
  ]
}
""",

    "nda": """
You are an NDA coaching expert.
Create an NDA Current Affairs digest from these news articles.

For each story (top 6-8):
- "headline": Short factual headline
- "topic": Category (Defence/Geography/History/Science/Sports/Awards)
- "summary": 2-sentence factual summary
- "key_facts": 5 quick-recall facts (names, dates, numbers, places)
- "exam_tip": What type of MCQ this could generate

Respond ONLY with JSON:
{ "exam": "NDA", "date": "today", "digest_items": [...] }
""",

    "cds": """
You are a CDS exam expert. Create a CDS Current Affairs digest.
For each story (top 6): headline, topic, 2-sentence summary,
4 rapid-recall facts, and a static_link (related History/Geography fact).
JSON: { "exam": "CDS", "date": "today", "digest_items": [...] }
""",

    "afcat": """
You are an AFCAT exam coach. Focus on Defence, Aviation, Science & Tech.
For each story (top 5): headline, topic, 2-sentence summary,
4 facts, defence_relevance (any IAF/military/aviation connection).
JSON: { "exam": "AFCAT", "date": "today", "digest_items": [...] }
""",

    "ssc": """
You are an SSC CGL/CHSL coaching expert. Create a one-liner digest.
For each story (top 8): headline, topic, one_liner (1 sentence), 3 super-short facts.
JSON: { "exam": "SSC", "date": "today", "digest_items": [...] }
""",

    "gate": """
You are a GATE coaching expert. Focus on Science, Technology, Engineering.
For each story (top 5): headline, topic, technical_summary (2 sentences),
3 technical facts, exam_relevance (which GATE paper/topic connects).
JSON: { "exam": "GATE", "date": "today", "digest_items": [...] }
"""
}

async def generate_digest(exam: str, days: int = 1, topic: Optional[str] = None) -> dict:
    articles = await fetch_articles_for_exam(exam, topic, days)

    if not articles:
        return {"error": "No articles found", "exam": exam, "digest_items": []}

    article_context = "\n\n".join([
        f"SOURCE: {a['source']}\nTITLE: {a['title']}\nSUMMARY: {a['summary']}"
        for a in articles[:15]
    ])

    base_prompt = DIGEST_PROMPTS.get(exam, DIGEST_PROMPTS["upsc"])
    topic_instruction = f"Focus on news about: {topic}\n\n" if topic else ""

    full_prompt = (
        f"{base_prompt}"
        f"\n{topic_instruction}"
        f"TODAY'S NEWS:\n{article_context}\n\n"
        f"Today's date: {date.today().strftime('%B %d, %Y')}"
    )

    raw = await call_nova_digest(full_prompt)
    result = parse_nova_json(raw)
    result["sources_used"] = list(set(a["source"] for a in articles))
    result["article_count"] = len(articles)
    result["powered_by"] = "Amazon Nova 2 Lite"
    return result