import streamlit as st
from typing import Dict, Any
import time
from dotenv import load_dotenv
from src.graph import app
from src.utils.ui_components import (
    apply_custom_css, 
    stream_response, 
    get_faq_data, 
    generate_static_faq_response,
    is_follow_up_to_faq,
    create_pipeline_context
)
from config.settings import (
    STREAMLIT_CONFIG,
    HOSPITAL_INFO,
    HOSPITAL_SERVICES,
    SAMPLE_FAQ_QUESTIONS,
    POPULAR_QUESTIONS,
    LLM_CONFIG
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(**STREAMLIT_CONFIG)

# Apply custom CSS styling
apply_custom_css()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0
if "user_feedback" not in st.session_state:
    st.session_state.user_feedback = {}
if "message_counter" not in st.session_state:
    st.session_state.message_counter = 0
if "faq_data" not in st.session_state:
    st.session_state.faq_data = get_faq_data()
if "pending_faq_response" not in st.session_state:
    st.session_state.pending_faq_response = None
if "user_has_interacted" not in st.session_state:
    st.session_state.user_has_interacted = False
if "last_processed_faq" not in st.session_state:
    st.session_state.last_processed_faq = None


# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    # Quick Access Information - Always visible
    st.header("🏥 معلومات المستشفى")
    
    st.markdown("### وصول سريع")
    st.markdown(f"📍 **الموقع:** {HOSPITAL_INFO['location']}")
    st.markdown(f"📞 **الطوارئ:** {HOSPITAL_INFO['emergency_number']}")
    st.markdown(f"🕒 **الزيارات:** {HOSPITAL_INFO['visiting_hours']}")
    st.markdown(f"💊 **الصيدلية:** {HOSPITAL_INFO['pharmacy_hours']}")
    
    # FAQ Section - Collapsible
    with st.expander("📋 الأسئلة الشائعة", expanded=True):
        faqs = SAMPLE_FAQ_QUESTIONS
        
        # FAQ dropdown menu
        dropdown_label = "اختر سؤالاً:" if not st.session_state.messages else "ابدأ محادثة جديدة بسؤال شائع:"
        
        selected_faq = st.selectbox(
            dropdown_label,
            options=[""] + faqs,
            index=0,
            key="faq_dropdown",
            help="اختر سؤالاً من الأسئلة الشائعة" + (" (سيبدأ محادثة جديدة)" if st.session_state.messages else "")
        )
        
        # Handle FAQ selection directly
        if selected_faq and selected_faq != "":
            # Check if this is a different FAQ than the last processed one
            if not hasattr(st.session_state, 'last_processed_faq') or st.session_state.last_processed_faq != selected_faq:
                # Always clear everything and start fresh when FAQ is selected
                st.session_state.messages = []
                st.session_state.conversation_count = 0
                st.session_state.user_feedback = {}
                st.session_state.message_counter = 0
                st.session_state.pending_faq_response = None
                st.session_state.user_has_interacted = True
                st.session_state.last_processed_faq = selected_faq
                
                # Add FAQ as user message
                st.session_state.message_counter += 1
                st.session_state.messages.append({"role": "user", "content": selected_faq, "id": st.session_state.message_counter})
                
                # Generate static response
                static_response = generate_static_faq_response(selected_faq, st.session_state.faq_data)
                st.session_state.pending_faq_response = static_response
                
                # Rerun to update the UI
                st.rerun()
    
    # Hospital Services - Collapsible
    with st.expander("🏥 خدمات المستشفى", expanded=False):
        for service in HOSPITAL_SERVICES:
            st.markdown(f"• {service}")
    
    # Contact Information - Collapsible
    with st.expander("📞 معلومات الاتصال", expanded=False):
        st.markdown(f"📧 **البريد الإلكتروني:** {HOSPITAL_INFO['email']}")
        st.markdown(f"📱 **الهاتف:** {HOSPITAL_INFO['phone']}")
        st.markdown(f"🌐 **الموقع الإلكتروني:** {HOSPITAL_INFO['website']}")
    
    # Small statistics section in sidebar (only if there are conversations)
    if st.session_state.conversation_count > 0:
        with st.expander("📊 إحصائيات المحادثة", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("المحادثات", st.session_state.conversation_count, label_visibility="collapsed")
                st.caption("عدد الرسائل")
            
            with col2:
                positive_feedback = sum(1 for feedback in st.session_state.user_feedback.values() if feedback == "positive")
                st.metric("👍", positive_feedback, label_visibility="collapsed")
                st.caption("إجابات مفيدة")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area with compact header
st.markdown('''
<div class="chat-header">
    <h1>🏥 Hospital AI Assistant Chatbot</h1>
    <p>اسألني أي شيء عن خدمات المستشفى أو المواعيد أو المعلومات العامة!</p>
</div>
''', unsafe_allow_html=True)

# Sample questions (only show if user hasn't interacted yet)
if not st.session_state.user_has_interacted and not st.session_state.messages and not st.session_state.pending_faq_response:
    st.markdown("### 💡 أسئلة شائعة")
    sample_questions = POPULAR_QUESTIONS
    
    # Create more compact button layout
    cols = st.columns(len(sample_questions))
    for i, question in enumerate(sample_questions):
        with cols[i]:
            if st.button(question, key=f"sample_{i}", use_container_width=True):
                # Mark that user has interacted
                st.session_state.user_has_interacted = True
                
                # Add FAQ as user message
                st.session_state.message_counter += 1
                st.session_state.messages.append({"role": "user", "content": question, "id": st.session_state.message_counter})
                
                # Generate static response
                static_response = generate_static_faq_response(question, st.session_state.faq_data)
                st.session_state.pending_faq_response = static_response
                st.rerun()
    
    st.markdown("---")
    st.markdown("*💬 أو اكتب سؤالك في المربع أدناه...*", help="يمكنك أيضاً استخدام الأسئلة الشائعة من الشريط الجانبي")

# Handle pending FAQ response
if st.session_state.pending_faq_response:
    # Add static response to messages
    st.session_state.message_counter += 1
    st.session_state.messages.append({
        "role": "assistant", 
        "content": st.session_state.pending_faq_response, 
        "id": st.session_state.message_counter
    })
    st.session_state.conversation_count += 1
    st.session_state.pending_faq_response = None
    st.rerun()

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"], avatar="🏥" if message["role"] == "assistant" else "👤"):
        # Convert newlines to HTML breaks while preserving markdown formatting
        content_with_breaks = message["content"].replace("\n", "<br>")
        st.markdown(content_with_breaks, unsafe_allow_html=True)
        
        # Add small feedback buttons for assistant messages (only show for last message)
        if message["role"] == "assistant" and idx == len(st.session_state.messages) - 1:
            # Use message ID if available, otherwise use index
            msg_id = message.get("id", idx)
            
            # Small, less prominent feedback section
            st.markdown("---")
            col1, col2, col3, col4 = st.columns([1, 1, 1, 9])
            
            with col1:
                if st.button("👍", key=f"thumbs_up_{msg_id}", help="مفيد", use_container_width=False):
                    st.session_state.user_feedback[msg_id] = "positive"
            
            with col2:
                if st.button("👎", key=f"thumbs_down_{msg_id}", help="يحتاج تحسين", use_container_width=False):
                    st.session_state.user_feedback[msg_id] = "negative"


# Chat input
if prompt := st.chat_input("اسألني أي شيء عن المستشفى..."):
    # Mark that user has interacted
    st.session_state.user_has_interacted = True
    
    # Check if this is a follow-up to an FAQ
    faq_context = is_follow_up_to_faq(st.session_state.messages, prompt)
    
    # Add user message to chat history
    st.session_state.message_counter += 1
    st.session_state.messages.append({"role": "user", "content": prompt, "id": st.session_state.message_counter})
    
    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # Generate assistant response
    with st.chat_message("assistant", avatar="🏥"):
        with st.spinner("جاري التفكير..."):
            try:
                # Prepare input for the pipeline
                if faq_context:
                    # This is a follow-up to an FAQ, use context
                    pipeline_input = create_pipeline_context(
                        faq_context["faq_question"],
                        faq_context["faq_answer"],
                        faq_context["user_followup"]
                    )
                else:
                    # Regular question
                    pipeline_input = prompt
                
                # Prepare conversation history (exclude current message)
                conversation_history = [msg for msg in st.session_state.messages[:-1] if msg.get("content")]
                
                # Invoke the chatbot
                result = app.invoke(input={
                    "question": pipeline_input,
                    "conversation_history": conversation_history,
                    "generation_retry_count": 0,  # Initialize retry counter
                    "max_generation_retries": 3   # Set max retries (configurable)
                })
                
                response = result.get("generation", "I'm sorry, I couldn't generate a response. Please try again.")
                

                
                # Stream the response
                message_placeholder = st.empty()
                full_response = stream_response(response, message_placeholder)
                
                # Add assistant response to chat history
                st.session_state.message_counter += 1
                st.session_state.messages.append({"role": "assistant", "content": full_response, "id": st.session_state.message_counter})
                st.session_state.conversation_count += 1
                
            except Exception as e:
                error_message = "أعتذر، أواجه صعوبات تقنية. يرجى المحاولة لاحقاً أو الاتصال بالمستشفى مباشرة."
                st.error(f"خطأ: {str(e)}")
                st.markdown(error_message)
                st.session_state.message_counter += 1
                st.session_state.messages.append({"role": "assistant", "content": error_message, "id": st.session_state.message_counter})

# Statistics now moved to sidebar for cleaner interface

# Clear chat button - More compact and better positioned
if st.session_state.messages:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ مسح سجل المحادثة", key="clear_chat", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_count = 0
            st.session_state.user_feedback = {}
            st.session_state.message_counter = 0
            st.session_state.pending_faq_response = None
            st.session_state.user_has_interacted = False
            st.session_state.last_processed_faq = None
            st.rerun() 