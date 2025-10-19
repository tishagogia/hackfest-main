import streamlit as st
from streamlit_option_menu import option_menu

from src.ui.theme import apply_theme
from src.ui.components import metric_card, alert_box
from src.models.verification_engine import VerificationEngine

# Set page configuration and styles
st.set_page_config(page_title="MisinformX AI", page_icon="🛡️", layout="wide")
apply_theme()

# Initialize verification engine
engine = VerificationEngine()

# Sidebar navigation menu for categories
with st.sidebar:
    selected = option_menu(
        menu_title="Modules",
        options=["News", "Deepfake", "Election", "Climate", "Viral", "Mental Health"],
        icons=["newspaper", "camera-video", "person-badge", "globe", "graph-up", "heart"],
        menu_icon="shield-fill",
        default_index=0
    )

# Page header
st.markdown('<h1 class="main-title">🛡️ MisinformX AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Multi-Modal Misinformation Intelligence Platform</p>', unsafe_allow_html=True)

# Input text area for user content
content = st.text_area(f"Paste the {selected} content to analyze:", height=250)

# Analyze button
if st.button("🔍 Analyze"):
    if content.strip():
        # Show loading spinner during long-running LLM queries
        with st.spinner(f"Analyzing {selected} content with Snowflake Cortex AI..."):
            results = engine.verify(selected.lower(), content)

        # Display consensus analysis
        st.markdown("### Consensus Analysis")
        st.write(results.get("consensus_analysis", "No consensus available."))

        # Display individual model responses
        st.markdown("### Individual Model Responses")
        st.json(results.get("individual_responses", {}))

        # Show simple metric card of number of models used
        metric_card("Models Consulted", str(len(results.get("individual_responses", {}))), delta="+0")

    else:
        alert_box("Please paste the content for analysis before clicking Analyze.", alert_type="warning")
