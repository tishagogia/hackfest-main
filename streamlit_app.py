import streamlit as st
from streamlit_option_menu import option_menu
import time

from src.ui.theme import apply_theme
from src.ui.components import metric_card, alert_box
from src.models.verification_engine import VerificationEngine

# Page configuration
st.set_page_config(
    page_title="TruthGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'last_content' not in st.session_state:
    st.session_state.last_content = ""

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/200x80?text=TruthGuard+AI", use_container_width=True)
    
    st.markdown("---")
    
    selected = option_menu(
        menu_title="📋 Analysis Modules",
        options=["News", "Deepfake", "Election", "Climate", "Viral", "Mental Health"],
        icons=["newspaper", "camera-video", "person-badge", "globe", "graph-up", "heart"],
        menu_icon="shield-fill",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#0f2027"},
            "icon": {"color": "#00C9A7", "font-size": "20px"},
            "nav-link": {"color": "#fff", "font-size": "16px", "margin": "5px 0"},
            "nav-link-selected": {"background-color": "#00C9A7", "color": "#000"}
        }
    )
    
    st.markdown("---")
    st.markdown("""
    **About TruthGuard AI**
    
    Multi-modal misinformation detection using:
    - 🤖 Mistral Large 2
    - 🧠 Claude 3.5 Sonnet
    - 🦙 Llama 3.1 70B
    """)
    
    st.markdown("---")
    if st.button("🔄 Reset Analysis", use_container_width=True):
        st.session_state.results = None
        st.session_state.last_content = ""
        st.rerun()

# Main content area
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<h1 class="main-title">🛡️ TruthGuard AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Multi-Modal Misinformation Intelligence Platform</p>', unsafe_allow_html=True)

with col2:
    st.markdown("")
    st.markdown("")
    st.markdown(f'<p style="text-align:right; color:#00C9A7; font-weight:bold;">Module: {selected}</p>', unsafe_allow_html=True)

st.markdown("---")

# Two-column layout for input and preview
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 Enter Content to Analyze")
    content = st.text_area(
        f"Paste {selected.lower()} content here:",
        height=250,
        placeholder="Enter the content you want to verify for misinformation...",
        key="content_input"
    )

with col2:
    st.markdown("### 📊 Analysis Settings")
    
    # Model selection
    use_all_models = st.checkbox("Use all models", value=True, help="Compare results across multiple models")
    
    temperature = st.slider(
        "Temperature (creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Lower = more deterministic, Higher = more creative"
    )
    
    max_tokens = st.slider(
        "Max tokens",
        min_value=256,
        max_value=2048,
        value=512,
        step=256,
        help="Maximum length of response"
    )

st.markdown("---")

# Analyze button
if st.button("🔍 Analyze Content", use_container_width=True, key="analyze_btn"):
    if content.strip():
        st.session_state.last_content = content
        
        with st.spinner(f"🔄 Analyzing {selected} content with Snowflake Cortex AI..."):
            try:
                engine = VerificationEngine()
                results = engine.verify(selected.lower(), content)
                st.session_state.results = results
                
            except Exception as e:
                alert_box(f"❌ Analysis failed: {str(e)}", alert_type="error")
                st.session_state.results = None
    else:
        alert_box("⚠️ Please paste content for analysis before clicking Analyze.", alert_type="warning")

# Display results if available
if st.session_state.results:
    results = st.session_state.results
    
    st.markdown("---")
    st.markdown("## 📊 Analysis Results")
    
    # Consensus analysis - prominent display
    with st.container():
        st.markdown("### 🎯 Consensus Verdict")
        consensus = results.get("consensus_analysis", "No consensus available.")
        
        # Color code based on keywords
        if "credible" in consensus.lower() or "true" in consensus.lower():
            st.success(consensus)
        elif "misinformation" in consensus.lower() or "false" in consensus.lower():
            st.error(consensus)
        else:
            st.info(consensus)
    
    st.markdown("---")
    
    # Individual model responses
    st.markdown("### 🤖 Individual Model Analyses")
    
    individual = results.get("individual_responses", {})
    
    cols = st.columns(len(individual))
    
    for idx, (model, response) in enumerate(individual.items()):
        with cols[idx]:
            with st.container():
                st.markdown(f"**{model}**")
                
                if "Error" in response:
                    st.error(response)
                else:
                    # Truncate long responses
                    display_text = response[:300] + "..." if len(response) > 300 else response
                    st.write(display_text)
                    
                    if len(response) > 300:
                        with st.expander("Read full response"):
                            st.write(response)
    
    st.markdown("---")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_card("Analysis Category", selected, color="#00C9A7")
    
    with col2:
        metric_card("Models Used", str(len(individual)), color="#FF6B6B")
    
    with col3:
        error_count = sum(1 for r in individual.values() if "Error" in r)
        metric_card("Successful", str(len(individual) - error_count), color="#4ECDC4")
    
    with col4:
        metric_card("Status", "✅ Complete", color="#95E1D3")
    
    # Export options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Results as JSON", use_container_width=True):
            import json
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_str,
                file_name=f"analysis_{selected.lower()}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.success("Results formatted for clipboard!")
            st.code(str(results), language="python")