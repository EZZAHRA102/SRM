"""Chat interface component."""
import streamlit as st
from frontend.api_client import SRMAPIClient


def render_chat(api_client: SRMAPIClient):
    """
    Render chat interface.
    
    Args:
        api_client: API client instance
    """
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "مرحباً بك في خدمة عملاء SRM! 👋\n\nأنا هنا لمساعدتك في فهم سبب انقطاع الماء أو الكهرباء.\n\nالرجاء تقديم رقم CIL الخاص بك (مثال: 1071324-101) أو رفع صورة الفاتورة."
        })
    
    st.markdown("---")
    st.markdown("### 💬 المحادثة")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("اكتب رسالتك هنا..."):
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("جاري التفكير..."):
                try:
                    # Convert messages to format expected by API
                    history = [
                        {"role": msg["role"], "content": msg["content"]}
                        for msg in st.session_state.messages[:-1]
                    ]
                    
                    response = api_client.chat(prompt, history)
                    assistant_response = response.get("response", "عذراً، حدث خطأ.")
                    
                    st.markdown(assistant_response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                except Exception as e:
                    error_msg = f"عذراً، حدث خطأ: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })


def clear_chat_history():
    """Clear the chat history."""
    if st.sidebar.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()


def display_conversation_stats():
    """Display conversation statistics in sidebar."""
    if "messages" in st.session_state:
        num_messages = len(st.session_state.messages)
        st.sidebar.markdown(f"**عدد الرسائل:** {num_messages}")


