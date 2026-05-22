"""
RetailPulse Analytics Management Suite - Home Page
Clean professional design matching reference
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import custom modules
from utils import (
    configure_page, 
    load_retail_data, 
    format_currency, 
    format_number,
    add_sidebar_logo,
    add_sidebar_footer
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

configure_page(title="Home", icon="📊", layout="wide")

# ============================================================================
# SIDEBAR - CLEAN PROFESSIONAL DESIGN
# ============================================================================

add_sidebar_logo()

st.sidebar.markdown("""
<div style="margin-bottom: 1.5rem;">
    <div style="
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #9ca3af;
        margin-bottom: 0.75rem;
    ">Navigation</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.info("""
**Quick Access**

Navigate to different sections:
- 📈 Sales Dashboard
- 👥 Customer Analytics  
- 🔮 Demand Forecasting
- 📦 Inventory Management
""")

add_sidebar_footer()

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_and_prepare_data():
    """Load and prepare data for home page"""
    df = load_retail_data()
    
    if df.empty:
        return None, None, None
    
    # Calculate current period metrics (last 30 days)
    if 'InvoiceDate' in df.columns:
        max_date = df['InvoiceDate'].max()
        current_period_start = max_date - timedelta(days=30)
        previous_period_start = current_period_start - timedelta(days=30)
        
        current_df = df[df['InvoiceDate'] >= current_period_start]
        previous_df = df[(df['InvoiceDate'] >= previous_period_start) & 
                        (df['InvoiceDate'] < current_period_start)]
    else:
        current_df = df
        previous_df = pd.DataFrame()
    
    return df, current_df, previous_df

df, current_df, previous_df = load_and_prepare_data()

# ============================================================================
# CHECK DATA AVAILABILITY
# ============================================================================

if df is None or df.empty:
    st.error("⚠️ No data available. Please ensure data files are in the `data/` directory.")
    st.stop()

# ============================================================================
# CALCULATE KPIs
# ============================================================================

# Determine revenue column
revenue_col = None
for col in ['TotalPrice', 'Revenue', 'Amount', 'Total']:
    if col in current_df.columns:
        revenue_col = col
        break

if revenue_col is None:
    st.error("⚠️ Could not find revenue column in data.")
    st.stop()

# Current period metrics
current_revenue = current_df[revenue_col].sum()
current_orders = len(current_df['InvoiceNo'].unique()) if 'InvoiceNo' in current_df.columns else len(current_df)
current_customers = len(current_df['CustomerID'].unique()) if 'CustomerID' in current_df.columns else 0
current_avg_order = current_revenue / current_orders if current_orders > 0 else 0

# Previous period metrics
if not previous_df.empty:
    previous_revenue = previous_df[revenue_col].sum()
    previous_orders = len(previous_df['InvoiceNo'].unique()) if 'InvoiceNo' in previous_df.columns else len(previous_df)
    previous_customers = len(previous_df['CustomerID'].unique()) if 'CustomerID' in previous_df.columns else 0
    previous_avg_order = previous_revenue / previous_orders if previous_orders > 0 else 0
    
    revenue_change = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
    orders_change = ((current_orders - previous_orders) / previous_orders * 100) if previous_orders > 0 else 0
    customers_change = ((current_customers - previous_customers) / previous_customers * 100) if previous_customers > 0 else 0
    avg_order_change = ((current_avg_order - previous_avg_order) / previous_avg_order * 100) if previous_avg_order > 0 else 0
else:
    previous_revenue = previous_orders = previous_customers = previous_avg_order = 0
    revenue_change = orders_change = customers_change = avg_order_change = 0

# Conversion rate
conversion_rate = (current_customers / current_orders * 100) if current_orders > 0 else 0
prev_conversion_rate = (previous_customers / previous_orders * 100) if previous_orders > 0 else 0
conversion_change = conversion_rate - prev_conversion_rate

# ============================================================================
# HEADER - PURE HTML
# ============================================================================

st.markdown(f"""
<div style="
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
">
    <div>
        <h1 style="
            font-family: 'Inter', sans-serif;
            font-size: 28px;
            font-weight: 700;
            color: #1a1a1a;
            margin: 0 0 0.25rem 0;
        ">Good Morning, Jacob</h1>
        <p style="
            font-size: 14px;
            color: #6b7280;
            margin: 0;
        ">Here's what's happening in RetailPulse today.</p>
    </div>
    <div style="
        display: flex;
        align-items: center;
        gap: 0.75rem;
        background: #f9fafb;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    ">
        <div style="text-align: right;">
            <div style="font-size: 13px; font-weight: 600; color: #1a1a1a;">Jacob Smith</div>
            <div style="font-size: 11px; color: #6b7280;">Senior Admin</div>
        </div>
        <div style="
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 14px;
        ">JS</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# KPI CARDS - Using Streamlit Metrics
# ============================================================================

st.markdown("### 📊 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 TOTAL REVENUE",
        value=format_currency(current_revenue),
        delta=f"{revenue_change:+.1f}% vs last month" if revenue_change != 0 else None
    )

with col2:
    st.metric(
        label="🛒 ORDERS PLACED",
        value=format_number(current_orders),
        delta=f"{orders_change:+.1f}% vs last month" if orders_change != 0 else None
    )

with col3:
    st.metric(
        label="💳 AVG. ORDER VALUE",
        value=format_currency(current_avg_order),
        delta=f"{avg_order_change:+.1f}% vs last month" if avg_order_change != 0 else None
    )

with col4:
    st.metric(
        label="👥 CONVERSION RATE",
        value=f"{conversion_rate:.1f}%",
        delta=f"{conversion_change:+.1f}% vs last month" if conversion_change != 0 else None
    )

# ============================================================================
# PROJECT OVERVIEW
# ============================================================================

st.markdown("---")

st.markdown("""
<div style="margin: 2rem 0;">
    <h2 style="
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 1rem;
    ">🎯 About RetailPulse</h2>
    <p style="font-size: 14px; color: #6b7280; line-height: 1.6;">
        RetailPulse is an AI-powered analytics platform designed for retail enterprise operators.
        Our suite provides comprehensive insights across sales analytics, customer intelligence,
        demand forecasting, and inventory optimization.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0; color: #9ca3af; font-size: 13px; border-top: 1px solid #e5e7eb; margin-top: 3rem;">
    <p style="margin: 0;">© 2026 RetailPulse Analytics Management Suite</p>
    <p style="margin: 0.5rem 0 0 0;">Built by Het Patel, Ved Zala, Parth Shah & Atharva Lotankar</p>
</div>
""", unsafe_allow_html=True)
