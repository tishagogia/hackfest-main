import streamlit as st

def metric_card(title, value, delta=None, color="#00C9A7"):
    """
    Renders a glass-style metric card with title, value, and optional delta.
    """
    delta_text = f"<span style='font-size:16px; color:#ccc;'>{delta}</span>" if delta else ""
    st.markdown(f"""
        <div class="glass-card" style="border-left: 5px solid {color};">
            <h4 style="margin:0;">{title}</h4>
            <h2 style="margin:0; color:{color};">{value}</h2>
            {delta_text}
        </div>
    """, unsafe_allow_html=True)

def alert_box(message, alert_type="info"):
    """
    Displays an alert box with message. alert_type can be: info, warning, error, success.
    """
    colors = {
        "info": "#17a2b8",
        "warning": "#ffc107",
        "error": "#dc3545",
        "success": "#28a745"
    }
    color = colors.get(alert_type, "#17a2b8")
    st.markdown(f"""
        <div style="
            background-color: {color};
            color: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            font-weight: bold;
            text-align: center;">
            {message}
        </div>
    """, unsafe_allow_html=True)

def loading_spinner(message="Loading..."):
    """
    Displays a simple loading spinner text placeholder.
    """
    with st.spinner(text=message):
        pass  # The function user adds the long running task after calling this
