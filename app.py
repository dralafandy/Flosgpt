import streamlit as st
import pandas as pd
from finance_manager import FinanceManager
from datetime import timedelta, datetime
import plotly.express as px
from components.navigation import show_navigation, show_menu_button
import re

# Set page configuration
st.set_page_config(page_title="FloosAfandy - إحسبها يا عشوائي !!", layout="wide")

# Initialize session state
def init_session_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if "show_sidebar" not in st.session_state:
        st.session_state.show_sidebar = True
    if "csrf_token" not in st.session_state:
        st.session_state.csrf_token = str(hash(datetime.now()))
    if "collapse_sidebar" not in st.session_state:
        st.session_state.collapse_sidebar = False

init_session_state()

# Show navigation components
show_navigation()
show_menu_button()

# Define a dictionary to map page names to their corresponding Python files
PAGE_MAPPING = {
    "home": None,
    "transactions": "pages/transactions.py",
    "accounts": "pages/accounts.py",
    "reports": "pages/reports.py",
    "instructions": "pages/instructions.py"
}

def handle_page_navigation():
    if st.session_state.current_page in PAGE_MAPPING:
        if PAGE_MAPPING[st.session_state.current_page]:
            st.switch_page(PAGE_MAPPING[st.session_state.current_page])
    else:
        st.error("Invalid page")

def login_form(fm):
    st.subheader("تسجيل الدخول إلى حسابك")
    login_username = st.text_input("اسم المستخدم", key="login_username")
    login_password = st.text_input("كلمة المرور", type="password", key="login_password")
    remember_me = st.checkbox("تذكرني", key="remember_me")
    if st.button("تسجيل الدخول"):
        try:
            if fm.verify_user(login_username, login_password):
                st.session_state.user_id = login_username
                st.session_state.logged_in = True
                if remember_me:
                    st.session_state.remembered_user = login_username
                st.success(f"مرحبًا بك، {login_username}!")
                st.session_state.current_page = "home"
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")
        except Exception as e:
            st.error(f"خطأ: {str(e)}")

def register_form(fm):
    st.subheader("إنشاء حساب جديد")
    new_username = st.text_input("اسم المستخدم", key="new_username")
    new_password = st.text_input("كلمة المرور", type="password", key="new_password")
    confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="confirm_password")
    if st.button("إنشاء الحساب"):
        if len(new_password) < 8 or not re.search(r"[A-Za-z\d]{8,}", new_password):
            st.error("كلمة المرور يجب أن تكون 8 أحرف على الأقل مع أرقام وحروف!")
        elif new_password != confirm_password:
            st.error("كلمات المرور غير متطابقة!")
        else:
            try:
                if fm.add_user(new_username, new_password):
                    st.success(f"تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول باستخدام {new_username}.")
                else:
                    st.error("اسم المستخدم موجود بالفعل!")
            except Exception as e:
                st.error(f"خطأ في الإنشاء: {str(e)}")

def home_page():
    if st.session_state.logged_in:
        st.switch_page("pages/dashboard.py")
    else:
        st.title("مرحبًا بك في FloosAfandy")
        st.markdown(
            f'<div style="display: flex; justify-content: center; margin: 20px 0;">'
            f'<img src="https://i.ibb.co/KpzDy27r/IMG-2998.png" width="300">'
            f'</div>',
            unsafe_allow_html=True
        )
        tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "🆕 إنشاء حساب جديد"])
        fm = FinanceManager()
        with tab1:
            login_form(fm)
        with tab2:
            register_form(fm)

def main():
    handle_page_navigation()
    if st.session_state.current_page == "home":
        home_page()

if __name__ == "__main__":
    main()
