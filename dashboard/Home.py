"""
RetailPulse Analytics Management Suite - Home Page
Professional dashboard matching Stitch reference design
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
# CUSTOM CSS FOR STITCH DESIGN
# ============================================================================

st.markdown("""
<style>
/* Search bar styling */
.stTextInput > div > div > input {
    background-color: #F8F9FA;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    font-size: 14px;
}

/* KPI Card with icon badge */
.kpi-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.5rem;
    position: relative;
}

.kpi-icon {
    width: 48px;
    height: 48px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;
}

.kpi-label {
    font-size: 11px;
    color: #6B7280;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.5rem;
}

.kpi-value {
    font-size: 32px;
    font-weight: 700;
    color: #1A1A1A;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.kpi-delta {
    font-size: 13px;
    font-weight: 600;
}

.kpi-delta.positive {
    color: #10B981;
}

.kpi-delta.negative {
    color: #EF4444;
}

/* Button styling */
.stButton > button {
    background: #0066FF !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.625rem 1.25rem !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.stButton > button:hover {
    background: #0052CC !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

configure_page(title="Home", icon="📊", layout="wide")

# ============================================================================
# SIDEBAR
# ============================================================================

# Note: Streamlit automatically adds navigation at the top
# Our sidebar content appears AFTER the navigation

st.sidebar.markdown("---")

# Export Report Button
if st.sidebar.button("📥 Export Report", use_container_width=True):
    st.sidebar.success("Report exported successfully!")

st.sidebar.markdown("---")

# Settings and Logout at bottom
st.sidebar.markdown("""
<div style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #E5E7EB;">
    <div style="padding: 0.75rem 1rem; cursor: pointer; color: #6B7280; font-size: 14px; display: flex; align-items: center; gap: 0.5rem; border-radius: 8px; transition: background 0.2s;">
        <span>⚙️</span>
        <span>Settings</span>
    </div>
    <div style="padding: 0.75rem 1rem; cursor: pointer; color: #EF4444; font-size: 14px; display: flex; align-items: center; gap: 0.5rem; border-radius: 8px; transition: background 0.2s;">
        <span>🚪</span>
        <span>Logout</span>
    </div>
</div>
""", unsafe_allow_html=True)

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
# HEADER WITH SEARCH BAR
# ============================================================================

# Top row: Title and User Profile
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
    <div>
        <h1 style="font-size: 28px; font-weight: 700; color: #1A1A1A; margin: 0; white-space: nowrap;">Welcome back, Jacob 👋</h1>
        <p style="font-size: 14px; color: #6B7280; margin: 0.25rem 0 0 0;">Here's your store performance overview for today</p>
    </div>
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="text-align: right;">
            <div style="font-size: 13px; font-weight: 600; color: #1A1A1A; white-space: nowrap;">Jacob Smith</div>
            <div style="font-size: 11px; color: #6B7280; white-space: nowrap;">Store Manager</div>
        </div>
        <div style="
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #0066FF;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 20px;
        ">👤</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Search bar and Advanced Filter
col_search, col_filter = st.columns([4, 1])

with col_search:
    st.text_input("🔍 Search", placeholder="Search orders, products, customers...", label_visibility="collapsed")

with col_filter:
    st.button("⚡ Quick Filters", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# KPI CARDS WITH ICON BADGES (Matching Stitch Design)
# ============================================================================

st.markdown("### 📊 Today's Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #EFF6FF;">
            <span style="font-size: 24px;">💰</span>
        </div>
        <div class="kpi-label">TOTAL REVENUE</div>
        <div class="kpi-value">{format_currency(current_revenue)}</div>
        <div class="kpi-delta {'positive' if revenue_change >= 0 else 'negative'}">
            {'↗' if revenue_change >= 0 else '↘'} {abs(revenue_change):.1f}%
        </div>
        <div style="font-size: 12px; color: #9CA3AF; margin-top: 0.25rem;">vs last period</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #DBEAFE;">
            <span style="font-size: 24px;">🛒</span>
        </div>
        <div class="kpi-label">ORDERS COMPLETED</div>
        <div class="kpi-value">{format_number(current_orders)}</div>
        <div class="kpi-delta {'positive' if orders_change >= 0 else 'negative'}">
            {'↗' if orders_change >= 0 else '↘'} {abs(orders_change):.1f}%
        </div>
        <div style="font-size: 12px; color: #9CA3AF; margin-top: 0.25rem;">vs last period</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #D1FAE5;">
            <span style="font-size: 24px;">💳</span>
        </div>
        <div class="kpi-label">AVG. ORDER VALUE</div>
        <div class="kpi-value">{format_currency(current_avg_order)}</div>
        <div class="kpi-delta {'positive' if avg_order_change >= 0 else 'negative'}">
            {'↗' if avg_order_change >= 0 else '↘'} {abs(avg_order_change):.1f}%
        </div>
        <div style="font-size: 12px; color: #9CA3AF; margin-top: 0.25rem;">vs last period</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #FCE7F3;">
            <span style="font-size: 24px;">📈</span>
        </div>
        <div class="kpi-label">CONVERSION RATE</div>
        <div class="kpi-value">{conversion_rate:.1f}%</div>
        <div class="kpi-delta {'positive' if conversion_change >= 0 else 'negative'}">
            {'↗' if conversion_change >= 0 else '↘'} {abs(conversion_change):.1f}%
        </div>
        <div style="font-size: 12px; color: #9CA3AF; margin-top: 0.25rem;">vs last period</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SALES PERFORMANCE & TOP PRODUCTS
# ============================================================================

st.markdown("---")

col_chart, col_products = st.columns([2, 1])

with col_chart:
    st.markdown("### 📊 Revenue Trends")
    
    # Create sample bar chart data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
    sales = [45000, 52000, 78000, 48000, 62000, 51000, 68000]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=months,
        y=sales,
        marker_color=['#BFDBFE' if i != 2 else '#0066FF' for i in range(len(months))],
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=12),
        xaxis=dict(
            title='',
            showgrid=False,
            showline=True,
            linecolor='#E5E7EB'
        ),
        yaxis=dict(
            title='',
            showgrid=True,
            gridcolor='#F3F4F6',
            showline=False
        ),
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_products:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="margin: 0; font-size: 18px; font-weight: 600;">🏆 Best Sellers</h3>
        <a href="#" style="color: #0066FF; text-decoration: none; font-size: 14px; font-weight: 500;">View All</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Top products list
    products = [
        {"name": "Nike Air Max 270", "category": "Footwear & Apparel", "price": "$1,420", "sold": "14 sold"},
        {"name": "Wireless Headphones", "category": "Electronics", "price": "$980", "sold": "23 sold"},
        {"name": "Smart Watch Pro", "category": "Wearables", "price": "$850", "sold": "18 sold"},
        {"name": "Classic Aviators", "category": "Accessories", "price": "$420", "sold": "30 sold"},
    ]
    
    for product in products:
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            background: white;
            border: 1px solid #E5E7EB;
            border-radius: 8px;
        ">
            <div style="
                width: 48px;
                height: 48px;
                background: #F3F4F6;
                border-radius: 8px;
                margin-right: 1rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
            ">📦</div>
            <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 14px; color: #1A1A1A;">{product['name']}</div>
                <div style="font-size: 12px; color: #6B7280;">{product['category']}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-weight: 700; font-size: 14px; color: #1A1A1A;">{product['price']}</div>
                <div style="font-size: 12px; color: #6B7280;">{product['sold']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# RECENT TRANSACTIONS
# ============================================================================

st.markdown("---")
st.markdown("### 📋 Recent Orders")

# Sample transaction data
transactions = [
    {"id": "#ORD-90210", "customer": "James Sullivan", "initials": "JS", "status": "DELIVERED", "status_color": "#10B981", "date": "Oct 24, 2023", "amount": "$124.50"},
    {"id": "#ORD-90209", "customer": "Maria Williams", "initials": "MW", "status": "PROCESSING", "status_color": "#3B82F6", "date": "Oct 24, 2023", "amount": "$2,104.99"},
    {"id": "#ORD-90208", "customer": "Robert Lee", "initials": "RL", "status": "REFUNDED", "status_color": "#EF4444", "date": "Oct 23, 2023", "amount": "$45.00"},
]

# Create table header
st.markdown("""
<div style="display: grid; grid-template-columns: 1.5fr 2fr 1.5fr 1.5fr 1.5fr; padding: 0.75rem 1rem; background: #F9FAFB; border-radius: 8px 8px 0 0; font-weight: 600; font-size: 12px; color: #6B7280; text-transform: uppercase;">
    <div>ORDER ID</div>
    <div>CUSTOMER</div>
    <div>STATUS</div>
    <div>DATE</div>
    <div style="text-align: right;">AMOUNT</div>
</div>
""", unsafe_allow_html=True)

# Create table rows
for tx in transactions:
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1.5fr 2fr 1.5fr 1.5fr 1.5fr; padding: 1rem; border-bottom: 1px solid #E5E7EB; align-items: center;">
        <div style="color: #0066FF; font-weight: 600; font-size: 14px;">{tx['id']}</div>
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #DBEAFE; display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 12px; color: #0066FF;">{tx['initials']}</div>
            <span style="font-size: 14px; color: #1A1A1A;">{tx['customer']}</span>
        </div>
        <div>
            <span style="background: {tx['status_color']}20; color: {tx['status_color']}; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 11px; font-weight: 700;">{tx['status']}</span>
        </div>
        <div style="font-size: 14px; color: #6B7280;">{tx['date']}</div>
        <div style="text-align: right; font-weight: 700; font-size: 14px; color: #1A1A1A;">{tx['amount']}</div>
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
