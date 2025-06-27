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
    "name": "🏥 Hospital Assistant",
    "location": "Maadi, Cairo",
    "emergency_number": "123",
    "phone": "02 25256289",
    "email": "info@hospital.com",
    "website": "www.hospital.com",
    "visiting_hours": "9 AM - 8 PM",
    "pharmacy_hours": "8 AM - 9 PM"
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "🏥 Hospital Assistant",
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
    "🚨 Emergency Care",
    "🔬 Laboratory Services", 
    "📡 Radiology",
    "👶 Pediatrics",
    "🤱 Maternity Ward",
    "💊 Pharmacy",
    "🍽️ Cafeteria",
    "🎁 Gift Shop"
]

# Sample FAQ Questions for UI
SAMPLE_FAQ_QUESTIONS = [
    "كيف يمكنني حجز موعد؟ - How can I book an appointment?",
    "ما هي مواعيد الزيارة؟ - What are your visiting hours?",
    "هل لديكم صيدلية؟ - Do you have a pharmacy?",
    "ما هي التأمينات التي تقبلونها؟ - What insurance do you accept?",
    "أين تقع المستشفى؟ - Where is the hospital located?",
    "ما هي أوقات العمل؟ - What are your operating hours?",
    "ما هي العيادات المتوفرة؟ - What are the available clinics?",
    "أريد طلب سيارة إسعاف - I want to request an ambulance"
]

# Popular Questions for Main Interface
POPULAR_QUESTIONS = [
    "ما هي العيادات المتوفرة؟ - What are the available clinics?",
    "ما هي أوقات العمل؟ - What are your operating hours?",
    "أريد طلب سيارة إسعاف - I want to request an ambulance"
] 