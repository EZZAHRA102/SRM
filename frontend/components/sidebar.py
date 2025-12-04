"""Sidebar component."""
import streamlit as st


def render_sidebar():
    """Render the sidebar with information and instructions."""
    with st.sidebar:
        st.markdown("### 📋 معلومات النظام")
        
        st.markdown("""
        <div class="sidebar-info">
            <h4>🎯 كيفية الاستخدام</h4>
            <ol>
                <li>ابدأ المحادثة مع المساعد</li>
                <li>قدم رقم CIL الخاص بك (مثال: 1071324-101)</li>
                <li>يمكنك رفع صورة الفاتورة لاستخراج الرقم تلقائياً</li>
                <li>سيساعدك المساعد في فهم سبب الانقطاع</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-info">
            <h4>💡 الخدمات المتوفرة</h4>
            <ul>
                <li>التحقق من حالة الدفع</li>
                <li>معرفة سبب انقطاع الخدمة</li>
                <li>معلومات عن الصيانة في منطقتك</li>
                <li>إرشادات للدفع</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="sidebar-info">
            <h4>📞 للمساعدة</h4>
            <p>رقم الطوارئ: <strong>0800-000-000</strong></p>
            <p>البريد الإلكتروني: <strong>support@srm.ma</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Testing CIL numbers
        with st.expander("🔢 أرقام CIL للاختبار"):
            st.markdown("""
            - **1071324-101** - Abdenbi (مدفوع، صيانة)
            - **1300994-101** - Ahmed (مدفوع)
            - **3095678-303** - محمد (مدفوع، لا صيانة)
            - **4017890-404** - خديجة (مدفوع، لا صيانة)
            - **5029012-505** - يوسف (غير مدفوع)
            """)


