"""
RetailPulse Design System
Unified design tokens matching reference UI
"""

import streamlit as st

# ============================================================================
# DESIGN TOKENS
# ============================================================================

COLORS = {
    # Primary
    'primary': '#0066FF',
    'primary_hover': '#0052CC',
    'primary_light': '#E6F0FF',
    'primary_container': '#DBEAFE',
    
    # Backgrounds
    'background': '#F8F9FA',
    'surface': '#FFFFFF',
    'surface_hover': '#F5F6F7',
    
    # Borders
    'border': '#E5E7EB',
    'border_light': '#F3F4F6',
    'outline_variant': '#E5E7EB',
    
    # Text
    'text_primary': '#1A1A1A',
    'text_secondary': '#6B7280',
    'text_tertiary': '#9CA3AF',
    'on_surface': '#1A1A1A',
    'on_surface_variant': '#6B7280',
    
    # Status
    'success': '#10B981',
    'success_light': '#D1FAE5',
    'success_container': '#D1FAE5',
    'on_success_fixed_variant': '#065F46',
    'warning': '#F59E0B',
    'warning_light': '#FEF3C7',
    'error': '#EF4444',
    'error_light': '#FEE2E2',
    'error_container': '#FEE2E2',
    'on_error_container': '#991B1B',
    'info': '#3B82F6',
    'info_light': '#DBEAFE',
    'info_container': '#DBEAFE',
    'on_info_fixed_variant': '#1E40AF',
}

TYPOGRAPHY = {
    'font_primary': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'font_display': "'Hanken Grotesk', 'Inter', sans-serif",
}

SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'md': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
    '2xl': '3rem',
}

RADIUS = {
    'sm': '0.375rem',
    'md': '0.5rem',
    'lg': '0.75rem',
    'xl': '1rem',
}

# ============================================================================
# COMPONENT BUILDERS
# ============================================================================

def render_html(html_content, height=None):
    """Render HTML using st.iframe (replacement for deprecated components.html)"""
    st.markdown(html_content, unsafe_allow_html=True)

def create_kpi_card(icon, label, value, delta=None, delta_text="", icon_bg="#E6F0FF", icon_color="#0066FF"):
    """Create a KPI card matching reference design"""
    
    delta_html = ""
    if delta is not None:
        delta_color = COLORS['success'] if delta >= 0 else COLORS['error']
        delta_arrow = "↗" if delta >= 0 else "↘"
        delta_html = f"""
        <div style="font-size: 13px; margin-top: 0.5rem;">
            <span style="color: {delta_color}; font-weight: 600;">
                {delta_arrow} {abs(delta):.1f}%
            </span>
            <span style="color: {COLORS['text_tertiary']}"> {delta_text}</span>
        </div>
        """
    
    return f"""
    <div style="
        background: white;
        border: 1px solid {COLORS['border']};
        border-radius: {RADIUS['lg']};
        padding: 1.5rem;
    ">
        <div style="
            width: 48px;
            height: 48px;
            background: {icon_bg};
            border-radius: {RADIUS['md']};
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
        ">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{icon_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                {icon}
            </svg>
        </div>
        <div style="
            font-size: 11px;
            color: {COLORS['text_secondary']};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        ">{label}</div>
        <div style="
            font-size: 32px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            line-height: 1;
        ">{value}</div>
        {delta_html}
    </div>
    """

def create_section_header(title, subtitle=""):
    """Create a section header"""
    subtitle_html = f'<p style="font-size: 14px; color: {COLORS["text_secondary"]}; margin: 0.25rem 0 0 0;">{subtitle}</p>' if subtitle else ""
    
    return f"""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="
            font-family: {TYPOGRAPHY['font_display']};
            font-size: 20px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 0;
        ">{title}</h2>
        {subtitle_html}
    </div>
    """

def create_stat_badge(label, value, color="primary"):
    """Create a small stat badge"""
    bg_colors = {
        'primary': COLORS['primary_light'],
        'success': COLORS['success_light'],
        'warning': COLORS['warning_light'],
        'error': COLORS['error_light'],
    }
    
    text_colors = {
        'primary': COLORS['primary'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'error': COLORS['error'],
    }
    
    return f"""
    <div style="
        display: inline-block;
        background: {bg_colors.get(color, bg_colors['primary'])};
        color: {text_colors.get(color, text_colors['primary'])};
        padding: 0.375rem 0.75rem;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    ">
        {label}: {value}
    </div>
    """

# ============================================================================
# SVG ICONS
# ============================================================================

ICONS = {
    'dollar': '<line x1="12" y1="2" x2="12" y2="22"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>',
    'cart': '<circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>',
    'card': '<rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line>',
    'users': '<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="8.5" cy="7" r="4"></circle><line x1="20" y1="8" x2="20" y2="14"></line><line x1="23" y1="11" x2="17" y2="11"></line>',
    'trending_up': '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline>',
    'trending_down': '<polyline points="23 18 13.5 8.5 8.5 13.5 1 6"></polyline><polyline points="17 18 23 18 23 12"></polyline>',
    'package': '<line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>',
    'alert': '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>',
    'check': '<polyline points="20 6 9 17 4 12"></polyline>',
    'star': '<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>',
}
