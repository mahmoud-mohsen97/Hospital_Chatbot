"""
Hospital Chatbot Configuration Settings
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / ".chroma"

# Data files
FAQ_DATA_FILE = DATA_DIR / "hospital_faq.csv"
KNOWLEDGE_BASE_FILE = DATA_DIR / "hospital_knowledge_base.csv"

# Hospital Information
HOSPITAL_INFO = {
    "name": "🏥 Hospital Assistant AI Chatbot",
    "location": "القاهرة",
    "emergency_number": "123",
    "phone": "02 25256289",
    "email": "info@hospital.com",
    "website": "www.hospital.com",
    "visiting_hours": "9 صباحاً - 8 مساءً",
    "pharmacy_hours": "8 صباحاً - 9 مساءً"
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "🏥 Hospital Assistant AI Chatbot",
    "page_icon": "🏥",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# LLM Configuration
LLM_CONFIG = {
    "model": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    "temperature": float(os.getenv("TEMPERATURE", "0")),
    "max_tokens": int(os.getenv("MAX_TOKENS", "500")),
    "max_generation_retries": 3
}

# Hospital Services
HOSPITAL_SERVICES = [
    "🚨 الرعاية الطارئة",
    "🔬 خدمات المختبر", 
    "📡 الأشعة",
    "👶 طب الأطفال",
    "🤱 قسم الولادة",
    "💊 الصيدلية",
    "🍽️ الكافتيريا",
    "🎁 متجر الهدايا"
]

# Sample FAQ Questions for UI
SAMPLE_FAQ_QUESTIONS = [
    "كيف يمكنني حجز موعد؟",
    "ما هي مواعيد الزيارة؟",
    "هل لديكم صيدلية؟",
    "ما هي التأمينات التي تقبلونها؟",
    "أين تقع المستشفى؟",
    "ما هي أوقات العمل؟",
    "ما هي العيادات المتوفرة؟",
    "أريد طلب سيارة إسعاف"
]

# Popular Questions for Main Interface
POPULAR_QUESTIONS = [
    "ما هي العيادات المتوفرة؟",
    "ما هي أوقات العمل؟",
    "أريد طلب سيارة إسعاف"
] 