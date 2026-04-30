import feedparser
import httpx
from datetime import datetime, timedelta
from typing import List, Dict
from config import NEWS_API_KEY

RSS_FEEDS = {
    "pib": {
        "url": "https://www.pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3",
        "source": "PIB",
        "relevance": ["upsc", "nda", "cds", "afcat", "ssc", "gate"]
    },
    "the_hindu": {
        "url": "https://www.thehindu.com/news/national/?service=rss",
        "source": "The Hindu",
        "relevance": ["upsc", "ssc", "afcat", "gate"]
    },
    "bbc_india": {
        "url": "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
        "source": "BBC India",
        "relevance": ["upsc", "nda", "cds", "afcat"]
    },
    "dd_news": {
        "url": "https://ddnews.gov.in/en/feed/",
        "source": "DD News",
        "relevance": ["upsc", "nda", "cds", "afcat"]
    },
    "economic_times": {
        "url": "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
        "source": "Economic Times",
        "relevance": ["upsc", "ssc", "gate"]
    },
    "hindu_sci_tech": {
        "url": "https://www.thehindu.com/sci-tech/?service=rss",
        "source": "The Hindu Science",
        "relevance": ["gate", "afcat", "upsc"]
    },
    "bbc_science": {
        "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
        "source": "BBC Science",
        "relevance": ["gate", "afcat", "upsc"]
    }
}

async def fetch_rss_articles(exam: str, max_per_feed: int = 8) -> List[Dict]:
    articles = []
    for feed_key, feed_info in RSS_FEEDS.items():
        if exam not in feed_info["relevance"]:
            continue
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:max_per_feed]:
                articles.append({
                    "title":     entry.get("title", "").strip(),
                    "summary":   entry.get("summary", "")[:500],
                    "link":      entry.get("link", ""),
                    "source":    feed_info["source"],
                    "published": entry.get("published", "")
                })
        except Exception as e:
            print(f"RSS fetch failed for {feed_key}: {e}")
    return articles

async def fetch_newsapi_articles(query: str, days: int = 1) -> List[Dict]:
    if not NEWS_API_KEY:
        return []
    from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query,
                    "from": from_date,
                    "language": "en",
                    "sortBy": "relevancy",
                    "pageSize": 10,
                    "apiKey": NEWS_API_KEY
                },
                timeout=10.0
            )
            data = resp.json()
            return [
                {
                    "title":     a["title"] or "",
                    "summary":   a["description"] or "",
                    "link":      a["url"] or "",
                    "source":    a.get("source", {}).get("name", "NewsAPI"),
                    "published": a.get("publishedAt", "")
                }
                for a in data.get("articles", [])
            ]
        except:
            return []

def deduplicate_articles(articles: List[Dict]) -> List[Dict]:
    seen_words = set()
    unique = []
    for article in articles:
        words = frozenset(
            w.lower() for w in article["title"].split()[:6]
            if len(w) > 3
        )
        if not words.intersection(seen_words):
            unique.append(article)
            seen_words.update(words)
    return unique

async def fetch_todays_headlines() -> List[Dict]:
    articles = await fetch_rss_articles("upsc", max_per_feed=3)
    return deduplicate_articles(articles)[:12]

async def fetch_articles_for_exam(exam: str, topic: str = None, days: int = 1) -> List[Dict]:
    rss_articles = await fetch_rss_articles(exam)
    if topic:
        api_articles = await fetch_newsapi_articles(f"{topic} India", days)
        all_articles = rss_articles + api_articles
    else:
        all_articles = rss_articles
    return deduplicate_articles(all_articles)[:20]