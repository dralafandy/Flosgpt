import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import timedelta, datetime

# تعيين إعدادات الصفحة أولاً
st.set_page_config(page_title="FloosAfandy - المعاملات", layout="wide", initial_sidebar_state="collapsed")

# تهيئة الحالة
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "csrf_token" not in st.session_state:
    st.session_state.csrf_token = str(hash(datetime.now()))
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "إضافة معاملة"
if "from_add_transaction" not in st.session_state:
    st.session_state.from_add_transaction = False

# Apply original sidebar and topbar styles
def apply_sidebar_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f9f9f9;
            font-family: Arial, sans-serif;
            font-size: 15px;
        }
        .horizontal-navbar {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #ffffff;
            padding: 10px 0;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        .horizontal-navbar button {
            background-color: #0066cc;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 15px;
            margin: 0 5px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.2s ease, transform 0.2s ease;
        }
        .horizontal-navbar button:hover {
            background-color: #005bb5;
            transform: scale(1.05);
        }
        .horizontal-navbar img {
            height: 40px;
            margin-right: 20px;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

def apply_topbar_styles():
    st.markdown("""
        <style>
        .topbar {
            background-color: #0066cc;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .topbar a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            font-size: 16px;
            font-weight: bold;
            transition: color 0.3s ease;
        }
        .topbar a:hover {
            color: #ffcc00;
        }
        .topbar .logo {
            font-size: 20px;
            font-weight: bold;
        }
        .card {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        </style>
    """, unsafe_allow_html=True)

apply_sidebar_styles()
apply_topbar_styles()

# التحقق من تسجيل الدخول
if not st.session_state.logged_in or "user_id" not in st.session_state:
    st.error("يرجى تسجيل الدخول أولاً من الصفحة الرئيسية!")
    st.switch_page("app.py")
else:
    fm = FinanceManager(st.session_state.user_id)

    # Page Title and Description
    st.title("💳 إدارة المعاملات")
    st.markdown("<p style='color: #6b7280;'>قم بإدارة وتتبع جميع معاملاتك المالية بسهولة من خلال هذه الصفحة.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Summary Section
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

    # Tabs for Categories, Adding Transactions, and Viewing Transactions
    tab_names = ["📂 إدارة الفئات", "➕ إضافة معاملة", "📋 عرض المعاملات"]
    tab1, tab2, tab3 = st.tabs(tab_names)

    accounts = fm.get_all_accounts()
    account_options = {acc[0]: acc[2] for acc in accounts}

    # Tab 1: Manage Categories
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

    # Tab 2: Add Transactions
    with tab2:
        st.subheader("➕ إضافة معاملة جديدة")
        st.markdown("<p style='color: #6b7280;'>قم بإضافة معاملة جديدة إلى حساباتك.</p>", unsafe_allow_html=True)
        st.markdown("---")

        if accounts:
            account_id = st.selectbox("🏦 الحساب", options=list(account_options.keys()), format_func=lambda x: account_options[x], key="add_account")
            trans_type = st.selectbox("📋 نوع المعاملة", ["وارد", "منصرف"], key="add_type")
            trans_type_db = "IN" if trans_type == "وارد" else "OUT"

            categories = fm.get_custom_categories(account_id, trans_type_db)
            category_options = [cat[0] for cat in categories] if categories else ["غير مصنف"]

            selected_category = st.selectbox("📂 الفئة", options=category_options, key="add_category")
            amount = st.number_input("💵 المبلغ", min_value=0.01, value=0.01, step=0.01, format="%.2f", key="add_amount")
            payment_method = st.selectbox("💳 طريقة الدفع", ["كاش", "بطاقة ائتمان", "تحويل بنكي"], key="add_payment")
            description = st.text_area("📝 الوصف", placeholder="وصف المعاملة (اختياري)", key="add_desc")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 حفظ المعاملة"):
                    with st.spinner("جارٍ الحفظ..."):
                        try:
                            alert = fm.add_transaction(account_id, amount, trans_type_db, description, payment_method, selected_category)
                            if alert and "تنبيه" in alert:
                                st.warning(alert)
                            else:
                                st.success("✅ تم حفظ المعاملة بنجاح!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ: {str(e)}")
            with col2:
                if st.button("🧹 مسح الحقول"):
                    st.session_state.pop("add_amount", None)
                    st.session_state.pop("add_desc", None)
                    st.rerun()
        else:
            st.warning("⚠️ لا توجد حسابات مضافة. يرجى إضافة حساب أولاً.")

    # Tab 3: View Transactions
    with tab3:
        st.subheader("📋 عرض المعاملات")
        st.markdown("<p style='color: #6b7280;'>قم بمراجعة وتصفية معاملاتك المالية.</p>", unsafe_allow_html=True)
        st.markdown("---")

        if transactions:
            df["account"] = df["account_id"].map(account_options)
            col1, col2, col3 = st.columns(3)
            with col1:
                search_query = st.text_input("🔍 البحث", "")
            with col2:
                filter_type = st.selectbox("📋 نوع المعاملة", ["الكل", "وارد", "منصرف"], key="filter_type")
            with col3:
                filter_category = st.selectbox("📂 الفئة", ["الكل"] + list(df["category"].unique()), key="filter_category")

            filtered_df = df
            if search_query:
                filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]
            if filter_type != "الكل":
                filtered_df = filtered_df[filtered_df["type"] == filter_type]
            if filter_category != "الكل":
                filtered_df = filtered_df[filtered_df["category"] == filter_category]

            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button("💾 تحميل CSV", csv, "transactions.csv", "text/csv", key="download_csv")

            st.dataframe(filtered_df[["date", "type", "amount", "account", "category", "description"]], use_container_width=True)
        else:
            st.info("ℹ️ لا توجد معاملات مسجلة.")
