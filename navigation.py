import streamlit as st
from core.state_manager import init_session_state

def create_nav_bar():
    """شريط التنقل الأفقي"""
    init_session_state()
    
    pages = {
        "🏠 الرئيسية": "app.py",
        "📊 لوحة التحكم": "pages/dashboard.py",
        "💳 المعاملات": "pages/transactions.py",
        "🏦 الحسابات": "pages/accounts.py",
        "💰 الميزانيات": "pages/budgets.py",
        "📈 التقارير": "pages/reports.py",
        "📚 التعليمات": "pages/instructions.py"
    }
    
    cols = st.columns(len(pages))
    for col, (label, page) in zip(cols, pages.items()):
        with col:
            if st.button(label, key=f"nav_{label}", use_container_width=True):
                st.session_state.target_page = page
                st.switch_page(page)

def check_auth():
    """التح, التحقق من مصادقة المستخدم"""
    if not st.session_state.get("logged_in", False):
        st.error("يرجى تسجيل الدخول أولاً من الصفحة الرئيسية!")
        st.session_state.target_page = "app.py"
        st.switch_page("app.py")
