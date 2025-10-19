import streamlit as st

def metric_card(title, value, delta="", color="#00C9A7"):
    """Display an enhanced metric card with animations"""
    st.markdown(f"""
        <div class="metric-card" style="border-left-color: {color};">
            <div class="metric-label">{title}</div>
            <div class="metric-value" style="color: {color};">{value}</div>
            {f'<div style="color: #888; font-size: 12px; margin-top: 5px;">{delta}</div>' if delta else ''}
        </div>
    """, unsafe_allow_html=True)

def alert_box(message, alert_type="info"):
    """Display an enhanced alert box"""
    icons = {
        "info": "ℹ️",
        "warning": "⚠️",
        "error": "❌",
        "success": "✅"
    }
    icon = icons.get(alert_type, "ℹ️")
    
    st.markdown(f"""
        <div class="alert-box alert-{alert_type}">
            {icon} {message}
        </div>
    """, unsafe_allow_html=True)

def progress_bar(current, total, label="Progress"):
    """Display a custom progress bar"""
    percentage = (current / total) * 100
    st.markdown(f"""
        <div style="margin: 20px 0;">
            <p style="color: #aaa; font-size: 0.9rem;">{label}</p>
            <div style="background-color: rgba(255,255,255,0.1); border-radius: 10px; overflow: hidden; height: 30px;">
                <div style="background: linear-gradient(90deg, #00C9A7 0%, #00FFD9 100%); 
                            width: {percentage}%; height: 100%; 
                            display: flex; align-items: center; justify-content: center;
                            color: #000; font-weight: bold;">
                    {int(percentage)}%
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)