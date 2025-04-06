import streamlit as st

def init_session_state():
    """تهيئة حالة الجلسة"""
    defaults = {
        "user_id": None,
        "collapse_sidebar": False,
        "target_page": None,
        "logged_in": False,
        "active_tab": "إضافة معاملة",
        "from_add_transaction": False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_session():
    """إعادة تعيين حالة الجلسة"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session_state()
