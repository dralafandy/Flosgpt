import streamlit as st

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

        /* Responsive navbar */
        @media (max-width: 768px) {
            .horizontal-navbar {
                flex-direction: column;
                padding: 5px 0;
            }
            .horizontal-navbar button {
                margin: 5px 0;
                width: 80%;
            }
            .horizontal-navbar img {
                display: none;
            }
        }

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            .horizontal-navbar {
                background-color: #2a2a2a;
                box-shadow: 0 2px 5px rgba(255, 255, 255, 0.1);
            }
            .horizontal-navbar button {
                background-color: #004d99;
            }
            .horizontal-navbar button:hover {
                background-color: #003366;
            }
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

        /* Responsive topbar */
        @media (max-width: 768px) {
            .topbar {
                flex-direction: column;
                padding: 10px;
            }
            .topbar a {
                margin: 5px 0;
                font-size: 14px;
            }
        }

        /* Dark mode support */
        @media (prefers-color-scheme: dark) {
            .topbar {
                background-color: #004d99;
            }
            .card {
                background-color: #2a2a2a;
                color: #ffffff;
            }
            .card:hover {
                box-shadow: 0 4px 8px rgba(255, 255, 255, 0.2);
            }
        }
        </style>
    """, unsafe_allow_html=True)
