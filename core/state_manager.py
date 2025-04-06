import streamlit as st

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
        st.session_state.csrf_token = None
    if "collapse_sidebar" not in st.session_state:
        st.session_state.collapse_sidebar = False
    if "target_page" not in st.session_state:
        st.session_state.target_page = None
