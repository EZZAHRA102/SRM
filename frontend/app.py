"""Main Streamlit application entry point."""
import streamlit as st
import os
from frontend.api_client import SRMAPIClient
from frontend.styles.rtl import inject_rtl_css
from frontend.components.header import render_header
from frontend.components.sidebar import render_sidebar
from frontend.components.chat import render_chat, clear_chat_history, display_conversation_stats
from frontend.components.file_upload import render_file_upload


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(
        page_title="نظام خدمة العملاء - SRM",
        page_icon="💧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject RTL CSS for Arabic support
    inject_rtl_css()
    
    # Get API URL from environment or use default
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    # Initialize API client
    api_client = SRMAPIClient(base_url=api_url)
    
    # Check backend health
    if not api_client.health_check():
        st.error("❌ لا يمكن الاتصال بالخادم الخلفي. الرجاء التأكد من تشغيل الخادم.")
        st.info(f"محاولة الاتصال بـ: {api_url}")
        st.stop()
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Render file upload
    render_file_upload(api_client)
    
    # Main chat interface
    render_chat(api_client)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("---")
        clear_chat_history()
        display_conversation_stats()
    
    # Cleanup
    api_client.close()


if __name__ == "__main__":
    main()


