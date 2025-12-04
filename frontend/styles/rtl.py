"""RTL (Right-to-Left) CSS for Arabic support."""
import streamlit as st


def inject_rtl_css():
    """Inject custom CSS for Right-to-Left (RTL) support and Arabic styling."""
    st.markdown("""
    <style>
        /* RTL Support for Arabic */
        .stApp {
            direction: rtl;
            text-align: right;
        }
        
        /* Chat messages */
        .stChatMessage {
            direction: rtl;
            text-align: right;
        }
        
        /* Text inputs */
        .stTextInput > div > div > input {
            direction: rtl;
            text-align: right;
        }
        
        /* Text areas */
        .stTextArea > div > div > textarea {
            direction: rtl;
            text-align: right;
        }
        
        /* Markdown content */
        .stMarkdown {
            direction: rtl;
            text-align: right;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            direction: rtl;
            text-align: right;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            direction: rtl;
            text-align: right;
        }
        
        /* Lists */
        ul, ol {
            direction: rtl;
            text-align: right;
            padding-right: 20px;
            padding-left: 0;
        }
        
        /* Custom styling for better Arabic font rendering */
        * {
            font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
        }
        
        /* Chat input */
        .stChatInputContainer {
            direction: rtl;
        }
        
        /* File uploader */
        [data-testid="stFileUploader"] {
            direction: rtl;
            text-align: right;
        }
        
        /* Success/Error/Warning boxes */
        .stSuccess, .stError, .stWarning, .stInfo {
            direction: rtl;
            text-align: right;
        }
        
        /* Custom header styling */
        .main-header {
            background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: white;
            text-align: center;
        }
        
        .main-header h1 {
            margin: 0;
            color: white;
            text-align: center;
        }
        
        /* Sidebar styling */
        .sidebar-info {
            background-color: #f0f9ff;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-right: 4px solid #3b82f6;
        }
    </style>
    """, unsafe_allow_html=True)


