"""
RetailPulse Design System
Unified design tokens matching premium dark/glassmorphic UI
"""

import streamlit as st

# ============================================================================
# DESIGN TOKENS
# ============================================================================

COLORS = {
    # Primary (Royal Blue)
    'primary': '#0066FF',
    'primary_hover': '#0052CC',
    'primary_light': 'rgba(0, 102, 255, 0.1)',
    'primary_container': 'rgba(0, 102, 255, 0.08)',
    
    # Backgrounds (Slate Light Theme)
    'background': '#F8FAFC',
    'surface': '#FFFFFF', 
    'surface_hover': '#F1F5F9',
    
    # Borders
    'border': '#E2E8F0',
    'border_light': '#F1F5F9',
    'outline_variant': '#E2E8F0',
    
    # Text (Slate Dark)
    'text_primary': '#0F172A',
    'text_secondary': '#475569',
    'text_tertiary': '#64748B',
    'on_surface': '#0F172A',
    'on_surface_variant': '#475569',
    
    # Status (Vibrant Variants)
    'success': '#00FFA3',
    'success_light': 'rgba(0, 255, 163, 0.1)',
    'success_container': 'rgba(0, 255, 163, 0.15)',
    'on_success_fixed_variant': '#00FFA3',
    'warning': '#FFD600',
    'warning_light': 'rgba(255, 214, 0, 0.1)',
    'error': '#FF0055',
    'error_light': 'rgba(255, 0, 85, 0.1)',
    'error_container': 'rgba(255, 0, 85, 0.15)',
    'on_error_container': '#FF0055',
    'info': '#00F0FF',
    'info_light': 'rgba(0, 240, 255, 0.1)',
    'info_container': 'rgba(0, 240, 255, 0.15)',
    'on_info_fixed_variant': '#00F0FF',
}

TYPOGRAPHY = {
    'font_primary': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    'font_display': "'Outfit', 'Inter', sans-serif",
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
    '2xl': '1.5rem',
}

# ============================================================================
# COMPONENT BUILDERS
# ============================================================================

def render_html(html_content, height=None):
    """Render HTML using st.markdown"""
    st.markdown(html_content, unsafe_allow_html=True)

def create_kpi_card(icon, label, value, delta=None, delta_text="", icon_bg=COLORS['primary_container'], icon_color=COLORS['primary']):
    """Create a premium glassmorphic KPI card"""
    
    delta_html = ""
    if delta is not None:
        delta_color = COLORS['success'] if delta >= 0 else COLORS['error']
        delta_arrow = "↗" if delta >= 0 else "↘"
        delta_html = f'<div style="font-size: 13px; margin-top: 0.75rem; display: flex; align-items: center; gap: 0.5rem;"><span style="color: {delta_color}; font-weight: 600; background: {delta_color}20; padding: 2px 6px; border-radius: 4px;">{delta_arrow} {abs(delta):.1f}%</span><span style="color: {COLORS["text_tertiary"]}; font-size: 12px;"> {delta_text}</span></div>'
    
    return f"""
    <div style="
        background: {COLORS['surface']};
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid {COLORS['border']};
        border-radius: {RADIUS['xl']};
        padding: 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 24px -8px rgba(0,0,0,0.5);
    " onmouseover="this.style.transform='translateY(-4px)'; this.style.borderColor='{icon_color}80'; this.style.boxShadow='0 12px 32px -8px {icon_color}40';" 
       onmouseout="this.style.transform='translateY(0)'; this.style.borderColor='{COLORS['border']}'; this.style.boxShadow='0 4px 24px -8px rgba(0,0,0,0.5)';">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div style="
                font-size: 12px;
                color: {COLORS['text_secondary']};
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                font-family: {TYPOGRAPHY['font_display']};
            ">{label}</div>
            <div style="
                width: 42px;
                height: 42px;
                background: {icon_bg};
                border-radius: {RADIUS['md']};
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: inset 0 0 12px rgba(255,255,255,0.1);
            ">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="{icon_color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="filter: drop-shadow(0 0 4px {icon_color}80);">
                    {icon}
                </svg>
            </div>
        </div>
        <div style="
            font-size: 34px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            line-height: 1;
            font-family: {TYPOGRAPHY['font_display']};
            text-shadow: 0 2px 10px rgba(255,255,255,0.1);
        ">{value}</div>
        {delta_html}
    </div>
    """

def create_section_header(title, subtitle=""):
    """Create a premium section header"""
    subtitle_html = f'<p style="font-size: 14px; color: {COLORS["text_secondary"]}; margin: 0.5rem 0 0 0; font-family: {TYPOGRAPHY["font_primary"]};">{subtitle}</p>' if subtitle else ""
    
    return f"""
    <div style="margin-bottom: 1.5rem; position: relative;">
        <h2 style="
            font-family: {TYPOGRAPHY['font_display']};
            font-size: 24px;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin: 0;
            letter-spacing: -0.02em;
        ">{title}</h2>
        {subtitle_html}
        <div style="position: absolute; left: 0; bottom: -12px; width: 40px; height: 3px; background: linear-gradient(90deg, {COLORS['primary']}, transparent); border-radius: 2px;"></div>
    </div>
    """

def create_stat_badge(label, value, color="primary"):
    """Create a sleek stat badge"""
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
        display: inline-flex;
        align-items: center;
        background: {bg_colors.get(color, bg_colors['primary'])};
        color: {text_colors.get(color, text_colors['primary'])};
        padding: 0.375rem 0.875rem;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
        border: 1px solid {text_colors.get(color, text_colors['primary'])}30;
        backdrop-filter: blur(4px);
    ">
        <span style="opacity: 0.8; margin-right: 4px;">{label}:</span> {value}
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
    'activity': '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>',
}

