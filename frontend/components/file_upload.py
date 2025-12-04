"""File upload component for OCR."""
import streamlit as st
from frontend.api_client import SRMAPIClient


def render_file_upload(api_client: SRMAPIClient):
    """
    Render file upload component for OCR.
    
    Args:
        api_client: API client instance
    """
    st.markdown("### 📤 رفع صورة الفاتورة (اختياري)")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "اختر صورة الفاتورة لاستخراج المعلومات تلقائياً",
            type=["png", "jpg", "jpeg", "pdf"],
            help="قم برفع صورة واضحة للفاتورة تحتوي على رقم CIL والمعلومات الأخرى"
        )
    
    with col2:
        extract_full = st.checkbox(
            "استخراج كامل المعلومات",
            value=True,
            help="استخراج جميع المعلومات من الفاتورة"
        )
    
    if uploaded_file is not None:
        # Display the uploaded image
        if uploaded_file.type.startswith('image'):
            st.image(uploaded_file, caption="الصورة المرفوعة", use_container_width=True)
        
        # Extract information button
        button_label = "🔍 استخراج المعلومات من الفاتورة" if extract_full else "🔍 استخراج رقم CIL فقط"
        
        if st.button(button_label):
            with st.spinner("جاري معالجة الصورة..."):
                try:
                    image_bytes = uploaded_file.getvalue()
                    
                    if extract_full:
                        # Extract all bill information
                        result = api_client.extract_bill_info(image_bytes, uploaded_file.name)
                        
                        if result.get("success"):
                            bill_info = result.get("data", {})
                            
                            # Display extracted information
                            st.success("✅ تم استخراج المعلومات بنجاح!")
                            
                            info_lines = ["📄 **المعلومات المستخرجة من الفاتورة:**\n"]
                            
                            if bill_info.get("cil"):
                                info_lines.append(f"🔢 رقم CIL: **{bill_info['cil']}**")
                            if bill_info.get("name"):
                                info_lines.append(f"👤 الاسم: {bill_info['name']}")
                            if bill_info.get("service_type"):
                                info_lines.append(f"⚡ نوع الخدمة: {bill_info['service_type']}")
                            if bill_info.get("amount_due"):
                                info_lines.append(f"💰 المبلغ المستحق: **{bill_info['amount_due']:.2f} درهم**")
                            if bill_info.get("due_date"):
                                info_lines.append(f"📅 تاريخ الاستحقاق: {bill_info['due_date']}")
                            
                            st.markdown("\n".join(info_lines))
                            
                            # If CIL found, add to chat
                            if bill_info.get("cil"):
                                if "messages" not in st.session_state:
                                    st.session_state.messages = []
                                
                                user_message = f"رقم CIL الخاص بي هو: {bill_info['cil']}"
                                st.session_state.messages.append({
                                    "role": "user",
                                    "content": user_message
                                })
                                
                                # Trigger rerun to process message
                                st.rerun()
                        else:
                            st.error(f"❌ {result.get('error', 'فشل الاستخراج')}")
                    else:
                        # Extract only CIL
                        result = api_client.extract_cil(image_bytes, uploaded_file.name)
                        
                        if result.get("success") and result.get("data", {}).get("cil"):
                            cil = result["data"]["cil"]
                            st.success(f"✅ تم استخراج رقم CIL: {cil}")
                            
                            # Add extracted CIL to chat
                            if "messages" not in st.session_state:
                                st.session_state.messages = []
                            
                            user_message = f"رقم CIL الخاص بي هو: {cil}"
                            st.session_state.messages.append({
                                "role": "user",
                                "content": user_message
                            })
                            
                            # Trigger rerun to process message
                            st.rerun()
                        else:
                            st.error("❌ لم يتم العثور على رقم CIL في الصورة. الرجاء إدخاله يدوياً.")
                            
                except Exception as e:
                    st.error(f"❌ حدث خطأ أثناء معالجة الصورة: {str(e)}")


