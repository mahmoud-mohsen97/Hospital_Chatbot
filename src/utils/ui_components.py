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

def is_follow_up_to_faq(messages: List[Dict], current_message: str) -> Dict[str, Any] | None:
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
    Context: The user initially asked the common question: "{faq_question}"

    Standard answer to the common question: {static_part}

    User's follow-up request: {user_followup}

    Please provide a detailed and helpful answer that builds on the common question's answer and addresses the user's specific request. Be practical and actionable in your response.
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
        
        /* Hide the hamburger menu (three dots) completely */
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        #MainMenu {
            visibility: hidden !important;
            display: none !important;
        }
        
        .stApp [data-testid="stToolbar"] {
            display: none !important;
        }
        
        /* Fix scrollbar position for RTL layout */
        html {
            direction: rtl !important;
        }
        
        body {
            direction: rtl !important;
        }
        
        .stApp {
            direction: rtl !important;
        }
        
        /* Move scrollbar to left side */
        ::-webkit-scrollbar {
            width: 8px !important;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1 !important;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1 !important;
            border-radius: 4px !important;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8 !important;
        }
        
        /* For Firefox scrollbar positioning */
        * {
            scrollbar-width: thin !important;
            scrollbar-color: #c1c1c1 #f1f1f1 !important;
        }
        
        /* RTL layout and base font */
        .stApp {
            direction: rtl !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-size: 14px !important;
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
        
        /* Resize main content to make room for sidebar */
        .main {
            margin-right: 280px !important;
            transition: margin-right 0.3s ease !important;
            width: calc(100% - 280px) !important;
        }
        
        /* Adjust the app container */
        .stApp > div {
            margin-right: 280px !important;
            transition: margin-right 0.3s ease !important;
        }
        
        /* Ensure content containers resize properly */
        section.main > div,
        .block-container {
            max-width: 100% !important;
            padding-right: 1rem !important;
            transition: all 0.3s ease !important;
        }
    </style>
    """, unsafe_allow_html=True)


def show_custom_sidebar():
    """Display a custom sidebar using Streamlit's native components."""
    # Initialize sidebar state
    if "show_custom_sidebar" not in st.session_state:
        st.session_state.show_custom_sidebar = False
    
    # Create sidebar toggle button in top-left
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("☰", key="sidebar_toggle", help="افتح/أغلق القائمة الجانبية"):
            st.session_state.show_custom_sidebar = not st.session_state.show_custom_sidebar
    
    # Show/hide sidebar based on state
    if st.session_state.show_custom_sidebar:
        # Style the native Streamlit sidebar
        st.markdown("""
        <style>
        /* Show and style the Streamlit sidebar */
        section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            background-color: #ffffff !important;
            border-left: 3px solid #1f77b4 !important;
            box-shadow: -5px 0 20px rgba(0,0,0,0.4) !important;
            z-index: 999999 !important;
            position: fixed !important;
            top: 0 !important;
            right: 0 !important;
            height: 100vh !important;
            direction: rtl !important;
            padding: 8px !important;
            transform: translateX(0) !important;
            transition: none !important;
        }
        
        /* Force sidebar to expanded state */
        section[data-testid="stSidebar"]:not([aria-expanded="false"]) {
            width: 280px !important;
            min-width: 280px !important;
        }
        
        /* Override any collapsed styles */
        section[data-testid="stSidebar"][aria-expanded="true"] {
            width: 280px !important;
            min-width: 280px !important;
        }
        
        /* Hide the keyboard_double_arrow text and sidebar button */
        section[data-testid="stSidebar"] button[data-testid="collapsedControl"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .css-1cypcdb {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .css-1d391kg .css-1cypcdb {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="collapsedControl"] * {
            display: none !important;
        }
        
        /* Hide any text containing keyboard_double_arrow */
        section[data-testid="stSidebar"] *:contains("keyboard_double_arrow") {
            display: none !important;
        }
        
        /* More aggressive hiding of collapse control elements */
        section[data-testid="stSidebar"] .css-1544g2n {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .css-1lcbmhc .css-1cypcdb {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] .css-17ziqus .css-1cypcdb {
            display: none !important;
        }
        
        /* Hide any element containing keyboard text */
        section[data-testid="stSidebar"] span[data-testid*="keyboard"] {
            display: none !important;
        }
        
        section[data-testid="stSidebar"] div[data-testid*="keyboard"] {
            display: none !important;
        }
        
        /* Hide collapse button and its container */
        section[data-testid="stSidebar"] > div > div:first-child {
            display: none !important;
        }
        
        /* Alternative approach - hide by content */
        section[data-testid="stSidebar"] span:contains("keyboard") {
            display: none !important;
        }
        
        /* Hide the sidebar header area that contains the collapse button */
        section[data-testid="stSidebar"] .css-1544g2n,
        section[data-testid="stSidebar"] .css-1y4p8pa,
        section[data-testid="stSidebar"] .css-1v3fvcr {
            display: none !important;
        }
        
        /* Ensure sidebar content is visible */
        section[data-testid="stSidebar"] > div {
            background-color: #ffffff !important;
            height: 100% !important;
            padding: 12px !important;
            overflow-y: auto !important;
            width: 100% !important;
            min-width: 100% !important;
        }
        
        /* Force the sidebar container to full width */
        section[data-testid="stSidebar"] .css-1d391kg {
            width: 280px !important;
            min-width: 280px !important;
        }
        
        section[data-testid="stSidebar"] .css-1lcbmhc {
            width: 280px !important;
            min-width: 280px !important;
        }
        
        section[data-testid="stSidebar"] .css-17ziqus {
            width: 280px !important;
            min-width: 280px !important;
        }
        
        /* Style sidebar content */
        section[data-testid="stSidebar"] .stMarkdown {
            direction: rtl !important;
            text-align: right !important;
            color: #333333 !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        section[data-testid="stSidebar"] .stMarkdown p {
            color: #333333 !important;
            font-size: 13px !important;
            line-height: 1.3 !important;
            margin: 6px 0 !important;
        }
        
        section[data-testid="stSidebar"] .stButton {
            visibility: visible !important;
            opacity: 1 !important;
        }
        
        section[data-testid="stSidebar"] .stButton button {
            width: 100% !important;
            text-align: right !important;
            direction: rtl !important;
            margin: 4px 0 !important;
            background-color: #ffffff !important;
            border: 2px solid #e9ecef !important;
            color: #333333 !important;
            padding: 6px 10px !important;
            border-radius: 5px !important;
            font-size: 0.8rem !important;
        }
        
        section[data-testid="stSidebar"] .stButton button:hover {
            border-color: #1f77b4 !important;
            background-color: #f8f9fa !important;
            color: #1f77b4 !important;
        }
        
        section[data-testid="stSidebar"] h1, 
        section[data-testid="stSidebar"] h2, 
        section[data-testid="stSidebar"] h3 {
            color: #1f77b4 !important;
            border-bottom: 2px solid #e9ecef !important;
            padding-bottom: 6px !important;
            margin: 12px 0 8px 0 !important;
            font-weight: 600 !important;
        }
        
        section[data-testid="stSidebar"] h1 {
            font-size: 1.2rem !important;
            text-align: center !important;
        }
        
        section[data-testid="stSidebar"] h2 {
            font-size: 1.0rem !important;
        }
        
        /* Style expanders for RTL layout */
        section[data-testid="stSidebar"] .streamlit-expanderHeader {
            direction: rtl !important;
            text-align: right !important;
            background-color: #f8f9fa !important;
            border: 1px solid #e9ecef !important;
            border-radius: 5px !important;
            padding: 6px 10px !important;
            margin: 6px 0 !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            color: #1f77b4 !important;
        }
        
        section[data-testid="stSidebar"] .streamlit-expanderHeader:hover {
            background-color: #e9ecef !important;
            border-color: #1f77b4 !important;
        }
        
        section[data-testid="stSidebar"] .streamlit-expanderContent {
            direction: rtl !important;
            text-align: right !important;
            border: 1px solid #e9ecef !important;
            border-top: none !important;
            border-radius: 0 0 5px 5px !important;
            padding: 8px !important;
            background-color: #ffffff !important;
            margin-bottom: 6px !important;
        }
        
        section[data-testid="stSidebar"] .streamlit-expanderContent .stButton button {
            font-size: 0.8rem !important;
            padding: 5px 8px !important;
            margin: 2px 0 !important;
        }
        
        /* Add backdrop */
        .main::before {
            content: '' !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background-color: rgba(0,0,0,0.3) !important;
            z-index: 999998 !important;
        }
        
        /* Ensure main content is pushed/dimmed when sidebar is open */
        .main {
            margin-right: 0 !important;
            opacity: 0.7 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # JavaScript to force sidebar expansion
        st.markdown("""
        <script>
        // Force sidebar to expanded state
        setTimeout(function() {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (sidebar) {
                // Force expanded state
                sidebar.setAttribute('aria-expanded', 'true');
                sidebar.style.width = '280px';
                sidebar.style.minWidth = '280px';
                sidebar.style.maxWidth = '280px';
                
                // Force inner content to full width
                const sidebarContent = sidebar.querySelector('div');
                if (sidebarContent) {
                    sidebarContent.style.width = '100%';
                    sidebarContent.style.minWidth = '100%';
                }
                
                // Hide any collapse buttons
                const collapseBtn = sidebar.querySelector('button[data-testid="collapsedControl"]');
                if (collapseBtn) {
                    collapseBtn.style.display = 'none';
                }
                
                // Hide keyboard_double_arrow text more aggressively
                const hideKeyboardText = function() {
                    // Find and hide any element containing keyboard text
                    const allElements = sidebar.querySelectorAll('*');
                    allElements.forEach(function(element) {
                        if (element.textContent && element.textContent.includes('keyboard')) {
                            element.style.display = 'none';
                        }
                        if (element.innerHTML && element.innerHTML.includes('keyboard')) {
                            element.style.display = 'none';
                        }
                    });
                    
                    // Specific selectors for keyboard elements
                    const keyboardElements = sidebar.querySelectorAll('[data-testid*="keyboard"], [class*="keyboard"], span:contains("keyboard")');
                    keyboardElements.forEach(function(element) {
                        element.style.display = 'none';
                    });
                    
                    // Hide the first div that typically contains the collapse button
                    const firstDiv = sidebar.querySelector('div > div:first-child');
                    if (firstDiv && firstDiv.querySelector('button')) {
                        firstDiv.style.display = 'none';
                    }
                };
                
                // Run immediately and repeatedly
                hideKeyboardText();
                setInterval(hideKeyboardText, 500);
            }
        }, 100);
        
        // Also force expansion on any state changes
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'attributes' && mutation.attributeName === 'aria-expanded') {
                    const sidebar = mutation.target;
                    if (sidebar && sidebar.getAttribute('data-testid') === 'stSidebar') {
                        sidebar.style.width = '280px';
                        sidebar.style.minWidth = '280px';
                        sidebar.style.maxWidth = '280px';
                    }
                }
            });
        });
        
        // Start observing
        setTimeout(function() {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (sidebar) {
                observer.observe(sidebar, { attributes: true, attributeFilter: ['aria-expanded'] });
            }
        }, 200);
        </script>
        """, unsafe_allow_html=True)
        
        # Use Streamlit's native sidebar
        with st.sidebar:
            # Close button at the top
            col_close1, col_close2, col_close3 = st.columns([1, 7, 2])
            with col_close3:
                if st.button("✖", key="close_sidebar_top", help="إغلاق القائمة", type="secondary"):
                    st.session_state.show_custom_sidebar = False
                    st.rerun()
            
            # Sidebar title
            st.markdown("# 🏥 معلومات المستشفى")
            
            # Quick access section (always visible)
            st.markdown("## 💫 وصول سريع")
            st.markdown("**📍 الموقع:** القاهرة")
            st.markdown("**🚨 الطوارئ:** 123")
            st.markdown("**🕒 الزيارات:** 9 صباحاً - 8 مساءً")
            st.markdown("**💊 الصيدلية:** 8 صباحاً - 9 مساءً")
            
            st.markdown("---")
            
            # FAQ section as dropdown
            with st.expander("📋 الأسئلة الشائعة", expanded=False):
                faq_questions = [
                    "كيف يمكنني حجز موعد؟",
                    "ما هي مواعيد الزيارة؟", 
                    "هل لديكم صيدلية؟",
                    "أين تقع المستشفى؟",
                    "ما هي التأمينات التي تقبلونها؟",
                    "ما هي أوقات العمل؟",
                    "ما هي العيادات المتوفرة؟",
                    "أريد طلب سيارة إسعاف"
                ]
                
                for question in faq_questions:
                    if st.button(question, key=f"sidebar_faq_{question}", use_container_width=True):
                        # Add the question to chat
                        st.session_state.messages.append({
                            "role": "user", 
                            "content": question,
                            "id": st.session_state.get("message_counter", 0) + 1
                        })
                        st.session_state.message_counter = st.session_state.get("message_counter", 0) + 1
                        st.session_state.show_custom_sidebar = False  # Close sidebar
                        st.rerun()
            
            # Hospital services as dropdown
            with st.expander("🏥 خدمات المستشفى", expanded=False):
                services = [
                    "🚨 الرعاية الطارئة",
                    "🔬 خدمات المختبر", 
                    "📡 الأشعة",
                    "👶 طب الأطفال",
                    "🤱 قسم الولادة",
                    "💊 الصيدلية",
                    "🍽️ الكافتيريا"
                ]
                
                for service in services:
                    st.markdown(f"• {service}")
            
            # Contact information as dropdown
            with st.expander("📞 معلومات الاتصال", expanded=False):
                st.markdown("**📧 البريد:** info@hospital.com")
                st.markdown("**📱 الهاتف:** 02 25256289")
                st.markdown("**🌐 الموقع:** www.hospital.com")
    else:
        # Hide the sidebar when not needed
        st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        /* Return main content to full width when sidebar is closed */
        .main {
            margin-right: 0 !important;
            transition: margin-right 0.3s ease !important;
            width: 100% !important;
        }
        
        /* Reset app container */
        .stApp > div {
            margin-right: 0 !important;
            transition: margin-right 0.3s ease !important;
        }
        
        /* Reset content containers */
        section.main > div,
        .block-container {
            max-width: 100% !important;
            padding-right: 1rem !important;
            transition: all 0.3s ease !important;
        }
        </style>
        """, unsafe_allow_html=True) 