# app.py (بعد التعديلات)
import streamlit as st
from styles import apply_sidebar_styles, apply_topbar_styles
from mobile_styles import apply_mobile_styles

st.set_page_config(page_title="FloosAfandy - إحسبها يا عشوائي !!", layout="wide")

apply_mobile_styles()
apply_sidebar_styles()
apply_topbar_styles()

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "auth"

# التحكم في الصفحات
if not st.session_state.logged_in:
    from pages.auth import auth_page
    auth_page()
else:
    # التنقل الجانبي
    st.sidebar.title("التنقل")
    if st.sidebar.button("🏠 لوحة التحكم"):
        st.session_state.current_page = "dashboard"
    if st.sidebar.button("💳 المعاملات"):
        st.session_state.current_page = "transactions"
    if st.sidebar.button("🏦 الحسابات"):
        st.session_state.current_page = "accounts"
    if st.sidebar.button("📈 التقارير"):
        st.session_state.current_page = "reports"
    if st.sidebar.button("📚 التعليمات"):
        st.session_state.current_page = "instructions"
    if st.sidebar.button("🚪 تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.current_page = "auth"
        st.rerun()

    # عرض الصفحة المناسبة
    if st.session_state.current_page == "dashboard":
        st.experimental_switch_page("pages/dashboard.py")
    elif st.session_state.current_page == "transactions":
        st.experimental_switch_page("pages/transactions.py")
    elif st.session_state.current_page == "accounts":
        st.experimental_switch_page("pages/accounts.py")
    elif st.session_state.current_page == "reports":
        st.experimental_switch_page("pages/reports.py")
    elif st.session_state.current_page == "instructions":
        st.experimental_switch_page("pages/instructions.py")
