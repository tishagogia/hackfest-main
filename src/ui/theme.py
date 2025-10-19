import streamlit as st

def apply_theme():
    """Apply modern glassmorphism theme to Streamlit app"""
    st.markdown("""
    <style>
    /* Root variables and overall styling */
    :root {
        --primary-color: #00C9A7;
        --secondary-color: #FF6B6B;
        --bg-dark: #0F2027;
        --bg-darker: #16222A;
        --text-light: #f8f9fa;
        --text-muted: #aaa;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(145deg, #0F2027, #203A43, #2C5364);
    }
    
    /* Main title styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00C9A7 0%, #00FFD9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(0, 201, 167, 0.3);
    }
    
    /* Subtitle styling */
    .sub-title {
        text-align: center;
        color: #bbb;
        margin-bottom: 2rem;
        font-weight: 400;
        font-size: 1.1rem;
    }
    
    /* Glass card effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease-in-out;
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.12);
        box-shadow: 0 8px 40px 0 rgba(0, 201, 167, 0.3);
        transform: translateY(-2px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #00C9A7 0%, #00FFD9 100%);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 201, 167, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #00FFD9 0%, #00C9A7 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 201, 167, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input fields */
    .stTextArea textarea {
        background-color: #1a1a2e !important;
        color: #fff !important;
        border-color: rgba(0, 201, 167, 0.3) !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #00C9A7 !important;
        box-shadow: 0 0 10px rgba(0, 201, 167, 0.3) !important;
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        color: #00C9A7;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: rgba(0, 201, 167, 0.1);
        border-radius: 8px;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: rgba(0, 201, 167, 0.2);
    }
    
    /* Checkboxes */
    .stCheckbox {
        color: #fff;
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateY(-3px);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #aaa;
        font-weight: 500;
    }
    
    /* Alerts */
    .alert-box {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid;
        font-weight: 500;
    }
    
    .alert-warning {
        background-color: rgba(255, 193, 7, 0.1);
        border-left-color: #FFC107;
        color: #FFD700;
    }
    
    .alert-error {
        background-color: rgba(220, 53, 69, 0.1);
        border-left-color: #DC3545;
        color: #FF6B7A;
    }
    
    .alert-success {
        background-color: rgba(40, 167, 69, 0.1);
        border-left-color: #28A745;
        color: #5FD27D;
    }
    
    .alert-info {
        background-color: rgba(23, 162, 184, 0.1);
        border-left-color: #17A2B8;
        color: #5FD3E0;
    }
    
    /* Code blocks */
    .stCode {
        background-color: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        border: 1px solid rgba(0, 201, 167, 0.2);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #fff;
    }
    
    /* Text */
    p, span, label {
        color: #e0e0e0;
    }
    
    /* Dividers */
    hr {
        border-color: rgba(0, 201, 167, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)