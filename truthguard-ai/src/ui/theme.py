import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    /* General styling for background and text */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(145deg, #0F2027, #203A43, #2C5364);
        color: #f8f9fa;
    }
    /* Glassmorphism card style */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
        margin-bottom: 1rem;
        transition: box-shadow 0.3s ease-in-out;
    }
    /* Card hover effect */
    .glass-card:hover {
        box-shadow: 0 0 30px #00C9A7;
    }
    /* Page title */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #00C9A7;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    /* Subtitle text */
    .sub-title {
        text-align: center;
        color: #ccc;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    /* Sidebar customization */
    .sidebar .sidebar-content {
        background: #16222a;
        color: #eee;
    }
    /* Make buttons look nicer */
    .stButton>button {
        background-color: #00C9A7;
        color: #fff;
        border-radius: 5px;
        border: none;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        transition: background-color 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #028f78;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
