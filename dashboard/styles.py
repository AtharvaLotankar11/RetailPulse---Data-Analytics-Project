"""
RetailPulse Design System Tokens
Based on design.md specifications for enterprise-grade UI/UX
"""

# ============================================================================
# COLOR PALETTE & SEMANTIC ASSIGNMENT
# ============================================================================

COLORS = {
    # Primary Brand Tokens
    "primary": "#004ac6",
    "primary_container": "#2563eb",
    "on_primary": "#ffffff",
    
    # Secondary Neutral Tokens
    "background_light": "#f7f9fb",
    "surface_container": "#eceef0",
    "surface_lowest": "#ffffff",
    "surface_bright": "#f7f9fb",
    "surface_container_low": "#f2f4f6",
    "outline_variant": "#c3c6d7",
    
    # Text Colors
    "on_surface": "#191c1e",
    "on_surface_variant": "#434655",
    
    # Semantic Telemetry Tokens
    "success": "#006242",
    "success_container": "#6ffbbe",
    "on_success_fixed_variant": "#005236",
    
    "error": "#ba1a1a",
    "error_container": "#ffdad6",
    "on_error_container": "#93000a",
    
    "warning": "#f59e0b",
    "warning_container": "#fef3c7",
    
    "info": "#2563eb",
    "info_container": "#d3e4fe",
    "on_info_fixed_variant": "#38485d",
}

# ============================================================================
# TYPOGRAPHY SCALE & HIERARCHY
# ============================================================================

TYPOGRAPHY = {
    # Display (Hanken Grotesk) - For high-impact data values
    "display_lg": {
        "font_family": "Hanken Grotesk",
        "size": "36px",
        "line_height": "44px",
        "weight": "700",
        "usage": "High-impact data values, Metric totals"
    },
    
    # Headline (Hanken Grotesk) - For page-level greetings
    "headline_md": {
        "font_family": "Hanken Grotesk",
        "size": "24px",
        "line_height": "32px",
        "weight": "600",
        "usage": "Page-level greetings, Panel definitions"
    },
    
    # Title (Inter) - For section headers
    "title_sm": {
        "font_family": "Inter",
        "size": "18px",
        "line_height": "24px",
        "weight": "600",
        "usage": "Section headers, Sub-component contexts"
    },
    
    # Body (Inter) - For primary text
    "body_md": {
        "font_family": "Inter",
        "size": "16px",
        "line_height": "24px",
        "weight": "400",
        "usage": "Explanatory labels, Primary text data"
    },
    
    # Body Small (Inter) - For form controls and tables
    "body_sm": {
        "font_family": "Inter",
        "size": "14px",
        "line_height": "20px",
        "weight": "400",
        "usage": "Form controls, Table cells, Meta descriptive logs"
    },
    
    # Label (Inter) - For navigation and actions
    "label_caps": {
        "font_family": "Inter",
        "size": "12px",
        "line_height": "16px",
        "weight": "600",
        "usage": "Navigation titles, Action triggers, Uppercase tokens"
    },
}

# ============================================================================
# STRUCTURAL GEOMETRY & SPACING VALUES
# ============================================================================

SPACING = {
    "gutter": "1.5rem",      # 24px - padding between distinct modular elements
    "stack_lg": "2rem",      # 32px - separating macro semantic layouts
    "stack_md": "1rem",      # 16px - standard container internal padding
    "stack_sm": "0.5rem",    # 8px - structural group binding or text separation
}

BORDER_RADIUS = {
    "default": "0.25rem",    # 4px - subtle inputs or semantic badges
    "xl": "0.75rem",         # 12px - structural bento grid metric wrapper blocks
    "lg": "0.5rem",          # 8px - cards and containers
}

# ============================================================================
# COMPONENT-SPECIFIC STYLES
# ============================================================================

# KPI Bento Card Styles
BENTO_CARD = {
    "background": COLORS["surface_lowest"],
    "border": f"1px solid {COLORS['outline_variant']}",
    "border_radius": BORDER_RADIUS["xl"],
    "padding": SPACING["stack_md"],
    "shadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
}

# Status Badge Styles
STATUS_BADGES = {
    "success": {
        "background": COLORS["success_container"],
        "color": COLORS["on_success_fixed_variant"],
        "text": "SUCCESS"
    },
    "pending": {
        "background": COLORS["info_container"],
        "color": COLORS["on_info_fixed_variant"],
        "text": "PENDING"
    },
    "refunded": {
        "background": COLORS["error_container"],
        "color": COLORS["on_error_container"],
        "text": "REFUNDED"
    },
    "warning": {
        "background": COLORS["warning_container"],
        "color": "#92400e",
        "text": "WARNING"
    },
}

# Trend Indicator Styles
TREND_INDICATORS = {
    "positive": {
        "color": COLORS["success"],
        "icon": "↗",
        "background": COLORS["success_container"],
    },
    "negative": {
        "color": COLORS["error"],
        "icon": "↘",
        "background": COLORS["error_container"],
    },
}

# ============================================================================
# LAYOUT CONSTANTS
# ============================================================================

LAYOUT = {
    "sidebar_width": "16rem",        # 256px (w-64)
    "header_height": "4rem",         # 64px (h-16)
    "max_content_width": "1440px",   # Maximum content width
    "mobile_breakpoint": "1024px",   # Collapse sidebar below this
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_color(color_name):
    """Get color value by name"""
    return COLORS.get(color_name, COLORS["primary"])

def get_status_badge_style(status):
    """Get status badge styling"""
    status_lower = status.lower()
    return STATUS_BADGES.get(status_lower, STATUS_BADGES["pending"])

def get_trend_style(value):
    """Get trend indicator style based on value"""
    if value >= 0:
        return TREND_INDICATORS["positive"]
    else:
        return TREND_INDICATORS["negative"]
