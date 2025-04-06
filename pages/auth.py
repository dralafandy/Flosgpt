# pages/auth.py
import streamlit as st
from finance_manager import FinanceManager

def auth_page():
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
        st.subheader("تسجيل الدخول إلى حسابك")
        login_username = st.text_input("اسم المستخدم", key="login_username")
        login_password = st.text_input("كلمة المرور", type="password", key="login_password")
        if st.button("تسجيل الدخول"):
            if fm.verify_user(login_username, login_password):
                st.session_state.user_id = login_username
                st.session_state.logged_in = True
                st.success(f"مرحبًا بك، {login_username}!")
                st.session_state.current_page = "dashboard"
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_username = st.text_input("اسم المستخدم", key="new_username")
        new_password = st.text_input("كلمة المرور", type="password", key="new_password")
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="confirm_password")
        if st.button("إنشاء الحساب"):
            if new_password == confirm_password:
                if fm.add_user(new_username, new_password):
                    st.success(f"تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول باستخدام {new_username}.")
                else:
                    st.error("اسم المستخدم موجود بالفعل!")
            else:
                st.error("كلمات المرور غير متطابقة!")
