"""
RetailPulse Reusable UI Components
Styled according to design.md specifications
"""

import streamlit as st
from styles import COLORS, get_status_badge_style, get_trend_style

# ============================================================================
# METRIC CARD COMPONENT (Bento Framework)
# ============================================================================

def metric_card(label, value, delta=None, delta_color="normal", icon=None):
    """
    Display a KPI metric card with optional trend indicator
    
    Args:
        label (str): Metric label (e.g., "Total Revenue")
        value (str): Metric value (e.g., "$124,592")
        delta (str): Change indicator (e.g., "+12.5%")
        delta_color (str): "normal", "inverse", or "off"
        icon (str): Optional icon name
    """
    st.metric(
        label=label,
        value=value,
        delta=delta,
        delta_color=delta_color
    )

# ============================================================================
# STATUS BADGE COMPONENT
# ============================================================================

def status_badge(status):
    """
    Display a colored status badge
    
    Args:
        status (str): Status text ("success", "pending", "refunded", "warning")
    
    Returns:
        str: HTML for status badge
    """
    style = get_status_badge_style(status)
    
    badge_html = f"""
    <span style="
        display: inline-block;
        padding: 0.25rem 0.625rem;
        border-radius: 9999px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        background-color: {style['background']};
        color: {style['color']};
    ">
        {style['text']}
    </span>
    """
    return badge_html

# ============================================================================
# TREND INDICATOR COMPONENT
# ============================================================================

def trend_indicator(value, show_icon=True):
    """
    Display a trend indicator with color coding
    
    Args:
        value (float): Trend value (positive or negative)
        show_icon (bool): Whether to show arrow icon
    
    Returns:
        str: HTML for trend indicator
    """
    style = get_trend_style(value)
    icon = style['icon'] if show_icon else ''
    
    trend_html = f"""
    <span style="
        color: {style['color']};
        font-weight: 700;
        font-size: 12px;
    ">
        {icon} {value:+.1f}%
    </span>
    """
    return trend_html

# ============================================================================
# SECTION HEADER COMPONENT
# ============================================================================

def section_header(title, subtitle=None, icon=None):
    """
    Display a section header with optional subtitle
    
    Args:
        title (str): Section title
        subtitle (str): Optional subtitle text
        icon (str): Optional icon
    """
    if icon:
        st.markdown(f"### {icon} {title}")
    else:
        st.markdown(f"### {title}")
    
    if subtitle:
        st.markdown(f"<p style='color: {COLORS['on_surface_variant']}; font-size: 14px; margin-top: -10px;'>{subtitle}</p>", 
                   unsafe_allow_html=True)

# ============================================================================
# CARD CONTAINER COMPONENT
# ============================================================================

def card_container(content_func, padding="1rem"):
    """
    Wrap content in a styled card container
    
    Args:
        content_func (callable): Function that renders content
        padding (str): Card padding
    """
    with st.container():
        st.markdown(f"""
        <div style="
            background-color: {COLORS['surface_lowest']};
            border: 1px solid {COLORS['outline_variant']};
            border-radius: 0.75rem;
            padding: {padding};
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        ">
        """, unsafe_allow_html=True)
        
        content_func()
        
        st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# INFO BOX COMPONENT
# ============================================================================

def info_box(message, type="info"):
    """
    Display an information box
    
    Args:
        message (str): Message to display
        type (str): "info", "success", "warning", "error"
    """
    colors = {
        "info": {"bg": COLORS["info_container"], "text": COLORS["on_info_fixed_variant"]},
        "success": {"bg": COLORS["success_container"], "text": COLORS["on_success_fixed_variant"]},
        "warning": {"bg": "#fef3c7", "text": "#92400e"},
        "error": {"bg": COLORS["error_container"], "text": COLORS["on_error_container"]},
    }
    
    color = colors.get(type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background-color: {color['bg']};
        color: {color['text']};
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-size: 14px;
        font-weight: 500;
    ">
        {message}
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# STAT CARD COMPONENT (Alternative to metric)
# ============================================================================

def stat_card(label, value, icon=None, trend=None):
    """
    Display a custom stat card with more control
    
    Args:
        label (str): Stat label
        value (str): Stat value
        icon (str): Optional icon
        trend (float): Optional trend percentage
    """
    trend_html = ""
    if trend is not None:
        trend_html = trend_indicator(trend)
    
    icon_html = f"<span style='font-size: 24px;'>{icon}</span>" if icon else ""
    
    st.markdown(f"""
    <div style="
        background-color: {COLORS['surface_lowest']};
        border: 1px solid {COLORS['outline_variant']};
        border-radius: 0.75rem;
        padding: 1.25rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
            {icon_html}
            {trend_html}
        </div>
        <p style="
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {COLORS['on_surface_variant']};
            margin-bottom: 0.5rem;
        ">{label}</p>
        <h2 style="
            font-family: 'Hanken Grotesk', sans-serif;
            font-size: 32px;
            font-weight: 700;
            color: {COLORS['on_surface']};
            margin: 0;
        ">{value}</h2>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# DIVIDER COMPONENT
# ============================================================================

def divider(margin="1.5rem"):
    """
    Display a styled divider
    
    Args:
        margin (str): Margin around divider
    """
    st.markdown(f"""
    <hr style="
        border: none;
        border-top: 1px solid {COLORS['outline_variant']};
        margin: {margin} 0;
    ">
    """, unsafe_allow_html=True)

# ============================================================================
# EMPTY STATE COMPONENT
# ============================================================================

def empty_state(message, icon="📊"):
    """
    Display an empty state message
    
    Args:
        message (str): Message to display
        icon (str): Icon to show
    """
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 3rem 1rem;
        color: {COLORS['on_surface_variant']};
    ">
        <div style="font-size: 48px; margin-bottom: 1rem;">{icon}</div>
        <p style="font-size: 16px;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
