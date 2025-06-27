import streamlit as st
from typing import List, Dict, Any
import time
import pandas as pd
from config.settings import FAQ_DATA_FILE

def render_sidebar_info():
    """Render hospital information in the sidebar."""
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("🏥 Hospital Information")
    
    st.markdown("### Quick Access")
    st.markdown("📍 **Location:** 123 Health Street, City, State")
    st.markdown("📞 **Emergency:** 911")
    st.markdown("🕒 **Visiting Hours:** 9 AM - 8 PM")
    st.markdown("💊 **Pharmacy:** 8 AM - 9 PM")
    st.markdown('</div>', unsafe_allow_html=True)

def get_faq_data() -> Dict[str, str]:
    """Load FAQ data from CSV file."""
    try:
        df = pd.read_csv(str(FAQ_DATA_FILE))
        return dict(zip(df["question"], df["answer"]))
    except Exception as e:
        st.error(f"Error loading FAQ data: {e}")
        return {}

def generate_static_faq_response(faq_question: str, faq_data: Dict[str, str]) -> str:
    """
    Generate a static response for FAQ using the answer directly from CSV.
    """
    static_answer = faq_data.get(faq_question, "I don't have a specific answer for this question.")
    
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
    Context: The user initially asked the FAQ question: "{faq_question}"
    
    Standard FAQ Answer: {static_part}
    
    User's Follow-up Request: {user_followup}
    
    Please provide a detailed and helpful response that builds upon the FAQ answer and addresses the user's specific request. Be practical and actionable in your response.
    """
    return context

def render_services_section():
    """Render hospital services in the sidebar."""
    st.markdown("### Hospital Services")
    services = [
        "🚨 Emergency Care",
        "🔬 Laboratory Services", 
        "📡 Radiology",
        "👶 Pediatrics",
        "🤱 Maternity Ward",
        "💊 Pharmacy",
        "🍽️ Cafeteria",
        "🎁 Gift Shop"
    ]
    
    for service in services:
        st.markdown(f"• {service}")

def render_contact_info():
    """Render contact information in the sidebar."""
    st.markdown("### Contact Information")
    st.markdown("📧 **Email:** info@hospital.com")
    st.markdown("📱 **Phone:** (555) 123-4567")
    st.markdown("🌐 **Website:** www.hospital.com")

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

def render_feedback_buttons(message_id: int) -> str:
    """Render thumbs up/down feedback buttons for a message."""
    col1, col2, col3 = st.columns([1, 1, 8])
    
    with col1:
        if st.button("👍", key=f"thumbs_up_{message_id}", help="Helpful response"):
            st.success("Thank you for your feedback!")
            return "positive"
    
    with col2:
        if st.button("👎", key=f"thumbs_down_{message_id}", help="Needs improvement"):
            st.info("Thank you for your feedback. We'll work to improve!")
            return "negative"
    
    return None

def render_statistics(conversation_count: int, user_feedback: Dict[int, str]):
    """Render conversation statistics."""
    if conversation_count > 0:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Conversations", conversation_count)
        
        with col2:
            positive_feedback = sum(1 for feedback in user_feedback.values() if feedback == "positive")
            st.metric("Positive Feedback", positive_feedback)
        
        with col3:
            total_messages = len(user_feedback)
            satisfaction_rate = f"{(positive_feedback / total_messages * 100):.1f}%" if total_messages > 0 else "N/A"
            st.metric("Satisfaction Rate", satisfaction_rate)

def render_sample_questions() -> str:
    """Render sample questions for users to click."""
    st.markdown("### 💡 Try asking me:")
    sample_questions = [
        "How can I book an appointment?",
        "What are your visiting hours?", 
        "Do you accept my insurance?",
        "Where is the hospital located?",
        "What should I bring to my appointment?"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(sample_questions):
        with cols[i % 3]:
            if st.button(question, key=f"sample_{i}"):
                return question
    return None

def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
    <style>
        .main > div {
            padding: 1.5rem 1rem;
        }
        
        .stChatMessage {
            padding: 1rem;
            border-radius: 10px;
            margin: 0.5rem 0;
            white-space: pre-wrap !important;
        }
        
        .chat-header {
            background: linear-gradient(90deg, #1f77b4, #4a90e2);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .sidebar-content {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        
        .metric-card {
            background-color: white;
            padding: 0.5rem;
            border-radius: 8px;
            border-left: 4px solid #1f77b4;
            margin: 0.25rem 0;
        }
        
        .error-message {
            background-color: #ffe6e6;
            border: 1px solid #ff9999;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        .success-message {
            background-color: #e6ffe6;
            border: 1px solid #99ff99;
            border-radius: 5px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Make feedback buttons smaller and less prominent */
        .stButton > button {
            font-size: 0.8rem;
            padding: 0.25rem 0.5rem;
            margin: 0.1rem;
        }
        
        /* Reduce space around metrics */
        [data-testid="metric-container"] {
            background-color: transparent;
            border: none;
            padding: 0.25rem;
        }
        
        /* Make chat input more prominent */
        .stChatInput {
            border-radius: 15px;
        }
        
        /* Reduce visual noise in sidebar */
        .element-container {
            margin-bottom: 0.5rem;
        }
        
        /* Style the FAQ dropdown */
        .stSelectbox > div > div > select {
            border-radius: 8px;
            border: 2px solid #e9ecef;
            background-color: white;
        }
        
        .stSelectbox > div > div > select:focus {
            border-color: #1f77b4;
            box-shadow: 0 0 5px rgba(31, 119, 180, 0.3);
        }
        
        /* Make main area sample buttons more prominent */
        .main .stButton > button {
            border-radius: 10px;
            border: 2px solid #e9ecef;
            background-color: white;
            transition: all 0.3s ease;
        }
        
        .main .stButton > button:hover {
            border-color: #1f77b4;
            background-color: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True) 