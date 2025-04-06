import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import timedelta, datetime
from mobile_styles import apply_mobile_styles

def create_nav_bar():
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    pages = {
        "🏠 الرئيسية": "app.py",
        "📊 لوحة التحكم": "pages/dashboard.py",
        "💳 المعاملات": "pages/transactions.py",
        "🏦 الحسابات": "pages/accounts.py",
        "💰 الميزانيات": "pages/budgets.py",
        "📈 التقارير": "pages/reports.py",
        "📚 التعليمات": "pages/instructions.py"
    }
    for col, (label, page) in zip([col1, col2, col3, col4, col5, col6, col7], pages.items()):
        with col:
            if st.button(label, key=f"nav_{label}"):
                st.switch_page(page)

def main():
    st.set_page_config(page_title="FloosAfandy - المعاملات", layout="wide", initial_sidebar_state="collapsed")
    apply_mobile_styles()
    create_nav_bar()

    if "user_id" not in st.session_state or "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("يرجى تسجيل الدخول أولاً من الصفحة الرئيسية!")
        st.switch_page("app.py")
    else:
        fm = FinanceManager(st.session_state.user_id)

        st.title("💳 إدارة المعاملات")
        st.markdown("<p style='color: #6b7280;'>قم بإدارة وتتبع جميع معاملاتك المالية بسهولة من خلال هذه الصفحة.</p>", unsafe_allow_html=True)
        st.markdown("---")

        st.subheader("📊 ملخص المعاملات")
        transactions = fm.get_all_transactions()
        if transactions:
            df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
            df["type"] = df["type"].replace({"IN": "وارد", "OUT": "منصرف"})
            total_income = df[df["type"] == "وارد"]["amount"].sum()
            total_expenses = df[df["type"] == "منصرف"]["amount"].sum()
            net_balance = total_income - total_expenses

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📥 إجمالي الوارد", f"{total_income:,.2f} جنيه")
            with col2:
                st.metric("📤 إجمالي المصروفات", f"{total_expenses:,.2f} جنيه")
            with col3:
                st.metric("📊 صافي الرصيد", f"{net_balance:,.2f} جنيه")
        else:
            st.info("ℹ️ لا توجد معاملات مسجلة حتى الآن.")

        st.markdown("---")

        tab_names = ["📂 إدارة الفئات", "➕ إضافة معاملة", "📋 عرض المعاملات"]
        tab1, tab2, tab3 = st.tabs(tab_names)

        accounts = fm.get_all_accounts()
        account_options = {acc[0]: acc[2] for acc in accounts}

        with tab1:
            st.subheader("📂 إدارة الفئات")
            st.markdown("<p style='color: #6b7280;'>قم بإضافة أو حذف الفئات المخصصة لمعاملاتك.</p>", unsafe_allow_html=True)
            st.markdown("---")

            cat_account_id = st.selectbox("🏦 اختر الحساب", options=list(account_options.keys()), format_func=lambda x: account_options[x], key="cat_account")
            cat_trans_type = st.selectbox("📋 نوع المعاملة", ["وارد", "منصرف"], key="cat_type")
            cat_trans_type_db = "IN" if cat_trans_type == "وارد" else "OUT"
            new_category_name = st.text_input("📛 اسم الفئة الجديدة", placeholder="مثال: مكافأة", key="new_category_name")

            if st.button("➕ إضافة فئة", key="add_category_button"):
                if new_category_name.strip():
                    with st.spinner("جارٍ الإضافة..."):
                        try:
                            fm.add_custom_category(cat_account_id, cat_trans_type_db, new_category_name)
                            st.success(f"✅ تمت إضافة الفئة: {new_category_name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ: {str(e)}")
                else:
                    st.warning("⚠️ أدخل اسمًا للفئة!")

            categories = fm.get_custom_categories(cat_account_id, cat_trans_type_db)
            if categories:
                st.write("📋 الفئات الحالية:")
                for cat in categories:
                    cat_name = cat[0]
                    col1, col2 = st.columns([3, 1])
                    col1.write(f"{'📥' if cat_trans_type_db == 'IN' else '📤'} {cat_name}")
                    if col2.button("🗑️ حذف", key=f"del_cat_{cat_name}_{cat_account_id}_{cat_trans_type_db}"):
                        with st.spinner("جارٍ الحذف..."):
                            try:
                                fm.delete_custom_category_by_name(cat_account_id, cat_trans_type_db, cat_name)
                                st.success(f"🗑️ تم حذف الفئة: {cat_name}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ خطأ: {str(e)}")
            else:
                st.info("ℹ️ لا توجد فئات.")

        with tab2:
            st.subheader("➕ إضافة معاملة جديدة")
            st.markdown("<p style='color: #6b7280;'>قم بإضافة معاملة جديدة إلى حساباتك.</p>", unsafe_allow_html=True)
            st.markdown("---")

            if accounts:
                st.session_state.account_id = st.selectbox("🏦 الحساب", options=list(account_options.keys()), format_func=lambda x: account_options[x], key="add_account")
                st.session_state.trans_type = st.selectbox("📋 نوع المعاملة", ["وارد", "منصرف"], key="add_type")
                trans_type_db = "IN" if st.session_state.trans_type == "وارد
