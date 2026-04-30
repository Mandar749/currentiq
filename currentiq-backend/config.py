from dotenv import load_dotenv
import os

load_dotenv()

# AWS / Nova Config
AWS_ACCESS_KEY_ID     = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION            = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

NOVA_MODEL_DIGEST = os.getenv("NOVA_MODEL_DIGEST", "amazon.nova-lite-v1:0")
NOVA_MODEL_MCQ    = os.getenv("NOVA_MODEL_MCQ",    "amazon.nova-lite-v1:0")
NOVA_MODEL_EVAL   = os.getenv("NOVA_MODEL_EVAL",   "amazon.nova-lite-v1:0")

# News API
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Exam Configurations
EXAM_CONFIG = {
    "upsc": {
        "name": "UPSC IAS/IPS",
        "topics": ["Polity", "Economy", "Environment", "International Relations", "Science & Technology"],
        "format": "analytical",
        "mcq_style": "4-option, negative marking, statement-based"
    },
    "nda": {
        "name": "NDA (National Defence Academy)",
        "topics": ["Current Events", "Geography", "History", "Defence & Security"],
        "format": "factual",
        "mcq_style": "4-option, direct factual recall"
    },
    "cds": {
        "name": "CDS (Combined Defence Services)",
        "topics": ["Current Affairs", "Indian History", "Geography", "Economy"],
        "format": "factual",
        "mcq_style": "4-option, application-based"
    },
    "afcat": {
        "name": "AFCAT (Air Force Common Admission Test)",
        "topics": ["General Awareness", "Science", "Defence", "Aviation"],
        "format": "factual",
        "mcq_style": "4-option, moderate difficulty"
    },
    "ssc": {
        "name": "SSC CGL/CHSL",
        "topics": ["Current Affairs", "Static GK", "Economy"],
        "format": "one-liner",
        "mcq_style": "4-option, quick recall"
    },
    "gate": {
        "name": "GATE",
        "topics": ["Science & Technology", "Engineering", "Research"],
        "format": "technical",
        "mcq_style": "technical MCQ with numerical answer type"
    }
}