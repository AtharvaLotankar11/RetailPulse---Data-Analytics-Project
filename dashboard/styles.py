"""
RetailPulse Design System Tokens
Modern light mode design with proper contrast
"""

# ============================================================================
# MODERN COLOR PALETTE
# ============================================================================

COLORS = {
    # Primary Brand Tokens
    "primary": "#3b82f6",
    "primary_hover": "#2563eb",
    "primary_light": "#dbeafe",
    "on_primary": "#ffffff",
    
    # Background & Surface
    "background": "#f8fafc",
    "surface": "#ffffff",
    "surface_hover": "#f1f5f9",
    "border": "#e2e8f0",
    "border_light": "#f1f5f9",
    
    # Text Colors (proper contrast)
    "text_primary": "#0f172a",
    "text_secondary": "#475569",
    "text_tertiary": "#94a3b8",
    
    # Semantic Colors
    "success": "#10b981",
    "success_light": "#d1fae5",
    "warning": "#f59e0b",
    "warning_light": "#fef3c7",
    "error": "#ef4444",
    "error_light": "#fee2e2",
    "info": "#3b82f6",
    "info_light": "#dbeafe",
    
    # ALL Backward compatibility aliases
    "surface_lowest": "#ffffff",
    "outline_variant": "#e2e8f0",
    "on_surface": "#0f172a",
    "on_surface_variant": "#475569",
    "primary_container": "#2563eb",
    "success_container": "#d1fae5",
    "error_container": "#fee2e2",
    "warning_container": "#fef3c7",
    "info_container": "#dbeafe",
    "on_success_fixed_variant": "#065f46",
    "on_error_container": "#991b1b",
    "on_info_fixed_variant": "#1e40af",
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
    "background": COLORS["surface"],
    "border": f"1px solid {COLORS['border']}",
    "border_radius": BORDER_RADIUS["xl"],
    "padding": SPACING["stack_md"],
    "shadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1)",
}

# Status Badge Styles
STATUS_BADGES = {
    "success": {
        "background": COLORS["success_light"],
        "color": COLORS["success"],
        "text": "SUCCESS"
    },
    "pending": {
        "background": COLORS["info_light"],
        "color": COLORS["info"],
        "text": "PENDING"
    },
    "refunded": {
        "background": COLORS["error_light"],
        "color": COLORS["error"],
        "text": "REFUNDED"
    },
    "warning": {
        "background": COLORS["warning_light"],
        "color": COLORS["warning"],
        "text": "WARNING"
    },
}

# Trend Indicator Styles
TREND_INDICATORS = {
    "positive": {
        "color": COLORS["success"],
        "icon": "↗",
        "background": COLORS["success_light"],
    },
    "negative": {
        "color": COLORS["error"],
        "icon": "↘",
        "background": COLORS["error_light"],
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
