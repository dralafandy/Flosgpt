import streamlit as st

def apply_mobile_styles():
    st.markdown("""
        <style>
            /* Basic mobile adjustments */
            @media (max-width: 768px) {
                /* Hide sidebar completely on mobile */
                section[data-testid="stSidebar"] {
                    display: none !important;
                }
                
                /* Make content full width on mobile with better spacing */
                .main .block-container {
                    padding: 1rem 1rem 10rem;
                    width: 100% !important;
                    margin-bottom: 1rem;
                }
                
                /* Adjust font sizes for mobile */
                h1 {
                    font-size: 1.5rem !important;
                }
                
                h2 {
                    font-size: 1.3rem !important;
                }
                
                /* Make buttons more touch-friendly */
                .stButton button {
                    min-width: 150px;
                    padding: 0.75rem;
                    font-size: 1rem;
                }
            }

            /* Dark mode support */
            @media (prefers-color-scheme: dark) {
                .stApp {
                    background-color: #1a1a1a;
                    color: #ffffff;
                }
                .stButton button {
                    background-color: #004d99;
                    color: white;
                }
                .stButton button:hover {
                    background-color: #003366;
                }
            }
        </style>
    """, unsafe_allow_html=True)
