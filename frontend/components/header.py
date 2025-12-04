"""Header component."""
import streamlit as st


def render_header():
    """Render the main application header with branding."""
    st.markdown("""
    <div class="main-header">
        <h1>💧 نظام خدمة العملاء - SRM</h1>
        <p style="margin: 5px 0 0 0; font-size: 14px;">مساعدك الذكي لخدمات المياه والكهرباء</p>
    </div>
    """, unsafe_allow_html=True)


