import streamlit as st
from typing import List, Dict, Any
import time
import pandas as pd
from config.settings import FAQ_DATA_FILE

def get_faq_data() -> Dict[str, str]:
    """Load FAQ data from CSV file."""
    try:
        df = pd.read_csv(str(FAQ_DATA_FILE))
        return dict(zip(df["question"], df["answer"]))
    except Exception as e:
        st.error(f"خطأ في تحميل بيانات الأسئلة الشائعة: {e}")
        return {}

def generate_static_faq_response(faq_question: str, faq_data: Dict[str, str]) -> str:
    """
    Generate a static response for FAQ using the answer directly from CSV.
    """
    static_answer = faq_data.get(faq_question, "ليس لدي إجابة محددة لهذا السؤال.")
    
    # Return the answer directly from CSV without adding extra prompts
    return static_answer

def is_follow_up_to_faq(messages: List[Dict], current_message: str) -> Dict[str, Any]:
    """
    Check if the current message is a follow-up to a recent FAQ.
    Returns FAQ context if it's a follow-up, None otherwise.
    """
    if len(messages) < 2:
        return None
    
    # Check last few messages for FAQ pattern
    for i in range(len(messages) - 1, max(len(messages) - 4, -1), -1):
        if i >= 1:  # Need at least user question and assistant response
            user_msg = messages[i-1]
            assistant_msg = messages[i]
            
            if (user_msg.get("role") == "user" and 
                assistant_msg.get("role") == "assistant" and
                any(faq in user_msg.get("content", "") for faq in [
                    "كيف يمكنني حجز موعد؟", "ما هي مواعيد الزيارة؟", "هل لديكم صيدلية؟",
                    "ما هي التأمينات التي تقبلونها؟", "أين يقع المستشفى؟", "ما هي أوقات العمل؟",
                    "ما هي العيادات المتوفرة؟", "أريد طلب سيارة إسعاف"
                ])):
                
                return {
                    "faq_question": user_msg.get("content"),
                    "faq_answer": assistant_msg.get("content"),
                    "user_followup": current_message
                }
    
    return None

def create_pipeline_context(faq_question: str, faq_answer: str, user_followup: str) -> str:
    """
    Create a context string for the pipeline that includes FAQ information and user's follow-up.
    """
    # Extract just the static answer part (before the action prompt)
    static_part = faq_answer.split("\n\n🔹")[0] if "\n\n🔹" in faq_answer else faq_answer
    
    context = f"""
    السياق: المستخدم سأل في البداية السؤال الشائع: "{faq_question}"
    
    الإجابة المعيارية للسؤال الشائع: {static_part}
    
    طلب المتابعة من المستخدم: {user_followup}
    
    يرجى تقديم إجابة مفصلة ومفيدة تبني على إجابة السؤال الشائع وتعالج طلب المستخدم المحدد. كن عملياً وقابلاً للتطبيق في إجابتك.
    """
    return context



def stream_response(response: str, placeholder) -> str:
    """Stream the response text to simulate real-time typing."""
    

    
    # Split into lines first to preserve line breaks
    lines = response.split('\n')
    full_response = ""
    
    # Stream line by line instead of word by word to preserve formatting
    for line_idx, line in enumerate(lines):
        for chunk in line.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Show current progress with preserved line structure and markdown
            display_content = full_response.replace("\n", "<br>")
            placeholder.markdown(display_content + "▌", unsafe_allow_html=True)
        
        # Add newline after each line (except the last one)
        if line_idx < len(lines) - 1:
            full_response += "\n"
    
    # Final response without cursor, preserving both newlines and markdown formatting
    final_text = full_response.strip()
    
    # Convert newlines to HTML breaks and use markdown for formatting
    content_with_breaks = final_text.replace("\n", "<br>")
    placeholder.empty()
    placeholder.markdown(content_with_breaks, unsafe_allow_html=True)
    
    return final_text



def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
    <style>
        /* Import compact, professional font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        
        /* Fix Streamlit sidebar collapse icon - Replace Material Icons with SVG */
        [data-testid="collapsedControl"] {
            position: relative !important;
            width: 40px !important;
            height: 40px !important;
            overflow: hidden !important;
        }
        
        /* Hide all text content */
        [data-testid="collapsedControl"] * {
            opacity: 0 !important;
            font-size: 0 !important;
        }
        
        /* Add custom SVG arrow icon */
        [data-testid="collapsedControl"]::before {
            content: "" !important;
            position: absolute !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            width: 20px !important;
            height: 20px !important;
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23666'%3E%3Cpath d='M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z'/%3E%3C/svg%3E") !important;
            background-size: contain !important;
            background-repeat: no-repeat !important;
            background-position: center !important;
            display: block !important;
            z-index: 1000 !important;
        }
        
        [data-testid="collapsedControl"]:hover::before {
            background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23333'%3E%3Cpath d='M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6-1.41-1.41z'/%3E%3C/svg%3E") !important;
        }
        
        /* RTL layout and base font */
        .stApp {
            direction: rtl !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-size: 14px !important;
        }
        
        /* Compact sidebar width when expanded */
        section[data-testid="stSidebar"]:not([aria-expanded="false"]) {
            width: 250px !important;
            min-width: 250px !important;
        }
        
        /* Main content area */
        .main {
            padding: 1rem !important;
            direction: rtl;
        }
        
        /* Compact Header Banner */
        .chat-header {
            background: linear-gradient(135deg, #1f77b4, #4a90e2) !important;
            color: white !important;
            padding: 1rem 1.5rem !important;
            border-radius: 12px !important;
            margin-bottom: 1rem !important;
            text-align: center;
            direction: rtl;
            box-shadow: 0 4px 12px rgba(31, 119, 180, 0.2) !important;
        }
        
        .chat-header h1 {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
            margin: 0 0 0.25rem 0 !important;
            color: white !important;
        }
        
        .chat-header p {
            font-size: 0.9rem !important;
            opacity: 0.9 !important;
            margin: 0 !important;
            color: white !important;
        }
        
        /* Chat Message Styling */
        .stChatMessage {
            padding: 0.75rem 1rem !important;
            border-radius: 18px !important;
            margin: 0.5rem 0 !important;
            direction: rtl;
            text-align: right;
            max-width: 85% !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
            font-size: 14px !important;
            line-height: 1.4 !important;
        }
        
        /* Sidebar Content */
        .sidebar-content {
            background-color: #f8f9fa !important;
            padding: 0.75rem !important;
            border-radius: 8px !important;
            margin-bottom: 0.75rem !important;
            direction: rtl;
            text-align: right;
            border: 1px solid #e9ecef !important;
        }
        
        .sidebar-content h2, .sidebar-content h3 {
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin: 0 0 0.5rem 0 !important;
            color: #2c3e50 !important;
        }
        
        .sidebar-content p, .sidebar-content li {
            font-size: 0.85rem !important;
            line-height: 1.3 !important;
            margin: 0.25rem 0 !important;
        }
        
        /* Compact Button Styling */
        .stButton > button {
            font-size: 0.85rem !important;
            padding: 0.5rem 1rem !important;
            margin: 0.25rem !important;
            border-radius: 8px !important;
            border: 1.5px solid #e9ecef !important;
            background-color: white !important;
            color: #495057 !important;
            transition: all 0.2s ease !important;
            font-weight: 500 !important;
            min-height: 38px !important;
        }
        
        .stButton > button:hover {
            border-color: #1f77b4 !important;
            background-color: #f8f9fa !important;
            color: #1f77b4 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 2px 8px rgba(31, 119, 180, 0.15) !important;
        }
        
        /* Sample Questions Buttons */
        .main .stButton > button {
            border-radius: 10px !important;
            border: 2px solid #e9ecef !important;
            background-color: white !important;
            transition: all 0.3s ease !important;
            direction: rtl;
            padding: 0.75rem 1rem !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }
        
        .main .stButton > button:hover {
            border-color: #1f77b4 !important;
            background-color: #f8f9fa !important;
            color: #1f77b4 !important;
            box-shadow: 0 4px 12px rgba(31, 119, 180, 0.15) !important;
        }
        
        /* Feedback Buttons */
        .stButton[key*="thumbs"] > button {
            font-size: 0.75rem !important;
            padding: 0.25rem 0.5rem !important;
            margin: 0.1rem 0.25rem !important;
            min-height: 28px !important;
            background-color: transparent !important;
            border: 1px solid #dee2e6 !important;
            border-radius: 6px !important;
        }
        
        .stButton[key*="thumbs"] > button:hover {
            background-color: #f8f9fa !important;
            border-color: #adb5bd !important;
        }
        
        /* Compact Metrics */
        [data-testid="metric-container"] {
            background-color: white !important;
            border: 1px solid #e9ecef !important;
            border-radius: 8px !important;
            padding: 0.5rem !important;
            margin: 0.25rem 0 !important;
            direction: rtl;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }
        
        [data-testid="metric-container"] > div {
            font-size: 0.8rem !important;
        }
        
        [data-testid="metric-container"] [data-testid="metric-value"] {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }
        
        /* Chat Input - Fixed overlap */
        .stChatInput {
            border-radius: 12px !important;
            direction: rtl;
            margin-top: 0.5rem !important;
        }
        
        .stChatInput textarea {
            font-size: 0.9rem !important;
            padding: 0.75rem 3.5rem 0.75rem 1rem !important;
            border-radius: 12px !important;
            border: 2px solid #e9ecef !important;
            min-height: 50px !important;
            max-height: 120px !important;
            resize: vertical !important;
        }
        
        .stChatInput textarea:focus {
            border-color: #1f77b4 !important;
            box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.1) !important;
        }
        
        /* FAQ Dropdown */
        .stSelectbox > div > div > select {
            border-radius: 8px !important;
            border: 2px solid #e9ecef !important;
            background-color: white !important;
            direction: rtl;
            text-align: right;
            font-size: 0.85rem !important;
            padding: 0.5rem !important;
        }
        
        .stSelectbox > div > div > select:focus {
            border-color: #1f77b4 !important;
            box-shadow: 0 0 5px rgba(31, 119, 180, 0.3) !important;
        }
        
        /* Reduce spacing */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        hr {
            margin: 0.75rem 0 !important;
            border: none !important;
            border-top: 1px solid #e9ecef !important;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            color: #2c3e50 !important;
            line-height: 1.3 !important;
        }
        
        p, span, div {
            font-family: 'Inter', sans-serif !important;
            color: #495057 !important;
            line-height: 1.4 !important;
        }
        
        .main h3 {
            font-size: 1.1rem !important;
            margin: 0.5rem 0 !important;
            color: #2c3e50 !important;
        }
        
        /* Collapsible Sections */
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            padding: 0.5rem !important;
            background-color: #f8f9fa !important;
            border-radius: 6px !important;
            border: 1px solid #e9ecef !important;
        }
        
        .streamlit-expanderContent {
            padding: 0.5rem !important;
            border: 1px solid #e9ecef !important;
            border-top: none !important;
            border-radius: 0 0 6px 6px !important;
        }
        
        /* Clear Chat Button */
        .stButton[key*="clear"] > button,
        .stButton[key*="مسح"] > button {
            background-color: #dc3545 !important;
            color: white !important;
            border: 2px solid #dc3545 !important;
            font-weight: 500 !important;
        }
        
        .stButton[key*="clear"] > button:hover,
        .stButton[key*="مسح"] > button:hover {
            background-color: #c82333 !important;
            border-color: #c82333 !important;
        }
        
        /* Emergency Button Emphasis */
        .stButton[key*="ambulance"] > button,
        .stButton[key*="إسعاف"] > button,
        .stButton[key*="emergency"] > button,
        .stButton[key*="طوارئ"] > button {
            background: linear-gradient(135deg, #dc3545, #c82333) !important;
            color: white !important;
            border: none !important;
            font-weight: 600 !important;
            box-shadow: 0 3px 10px rgba(220, 53, 69, 0.3) !important;
        }
        
        .stButton[key*="ambulance"] > button:hover,
        .stButton[key*="إسعاف"] > button:hover,
        .stButton[key*="emergency"] > button:hover,
        .stButton[key*="طوارئ"] > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4) !important;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            section[data-testid="stSidebar"]:not([aria-expanded="false"]) {
                width: 100% !important;
                min-width: 100% !important;
            }
            
            .main {
                padding: 0.5rem !important;
            }
            
            .chat-header {
                padding: 0.75rem 1rem !important;
                margin-bottom: 0.75rem !important;
            }
            
            .chat-header h1 {
                font-size: 1.25rem !important;
            }
            
            .stChatMessage {
                max-width: 95% !important;
                font-size: 0.85rem !important;
                padding: 0.5rem 0.75rem !important;
            }
            
            .stButton > button {
                font-size: 0.8rem !important;
                padding: 0.5rem 0.75rem !important;
            }
            
            .stChatInput textarea {
                padding: 0.5rem 3rem 0.5rem 0.75rem !important;
                min-height: 45px !important;
            }
        }
        
        @media (max-width: 480px) {
            .main {
                padding: 0.25rem !important;
            }
            
            .chat-header {
                padding: 0.5rem !important;
            }
            
            .chat-header h1 {
                font-size: 1.1rem !important;
            }
            
            .sidebar-content {
                padding: 0.5rem !important;
            }
            
            .stChatMessage {
                padding: 0.5rem !important;
                font-size: 0.8rem !important;
            }
            
            .stChatInput textarea {
                padding: 0.5rem 2.5rem 0.5rem 0.5rem !important;
            }
        }
    </style>
    """, unsafe_allow_html=True) 