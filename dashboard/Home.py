"""
RetailPulse Analytics Management Suite - Home Page
Main dashboard with KPI overview and navigation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Import custom modules
from utils import (
    configure_page, 
    load_retail_data, 
    format_currency, 
    format_number,
    format_percentage,
    calculate_percentage_change,
    add_sidebar_logo,
    add_sidebar_footer
)
from components import metric_card, section_header, info_box
from styles import COLORS

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

configure_page(title="Home", icon="📊", layout="wide")

# ============================================================================
# SIDEBAR
# ============================================================================

add_sidebar_logo()

st.sidebar.markdown("### 🎯 Navigation")
st.sidebar.info("""
**Welcome to RetailPulse!**

Use the pages in the sidebar to explore:
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
# HEADER SECTION
# ============================================================================

st.markdown(f"""
<div style="margin-bottom: 2rem;">
    <h1 style="
        font-family: 'Hanken Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: {COLORS['on_surface']};
        margin-bottom: 0.5rem;
    ">Good Morning, Amanda 👋</h1>
    <p style="
        font-size: 14px;
        color: {COLORS['on_surface_variant']};
        margin: 0;
    ">Here's your operational data snapshot for today • {datetime.now().strftime('%B %d, %Y')}</p>
</div>
""", unsafe_allow_html=True)

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
    st.error("⚠️ Could not find revenue column in data. Expected columns: TotalPrice, Revenue, Amount, or Total")
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
    
    # Calculate changes
    revenue_change = calculate_percentage_change(current_revenue, previous_revenue)
    orders_change = calculate_percentage_change(current_orders, previous_orders)
    customers_change = calculate_percentage_change(current_customers, previous_customers)
    avg_order_change = calculate_percentage_change(current_avg_order, previous_avg_order)
else:
    revenue_change = orders_change = customers_change = avg_order_change = 0

# ============================================================================
# KPI BENTO GRID
# ============================================================================

st.markdown("### 📊 Key Performance Indicators")
st.markdown("<p style='color: #434655; font-size: 14px; margin-top: -10px; margin-bottom: 1.5rem;'>Last 30 days performance overview</p>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="💰 TOTAL REVENUE",
        value=format_currency(current_revenue),
        delta=f"{revenue_change:+.1f}%",
        delta_color="normal"
    )
    st.caption(f"vs. {format_currency(previous_revenue if not previous_df.empty else 0)} last period")

with col2:
    st.metric(
        label="🛒 ORDERS PLACED",
        value=format_number(current_orders),
        delta=f"{orders_change:+.1f}%",
        delta_color="normal"
    )
    st.caption(f"vs. {format_number(previous_orders if not previous_df.empty else 0)} last period")

with col3:
    st.metric(
        label="📦 AVG. ORDER VALUE",
        value=format_currency(current_avg_order),
        delta=f"{avg_order_change:+.1f}%",
        delta_color="normal"
    )
    st.caption(f"vs. {format_currency(previous_avg_order if not previous_df.empty else 0)} last period")

with col4:
    st.metric(
        label="👥 ACTIVE CUSTOMERS",
        value=format_number(current_customers),
        delta=f"{customers_change:+.1f}%",
        delta_color="normal"
    )
    st.caption(f"vs. {format_number(previous_customers if not previous_df.empty else 0)} last period")

st.markdown("---")

# ============================================================================
# PROJECT OVERVIEW SECTION
# ============================================================================

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 🎯 About RetailPulse")
    
    st.markdown("""
    **RetailPulse** is an AI-powered analytics platform designed for retail enterprise operators 
    and senior administrators. Our suite provides comprehensive insights across four key areas:
    
    #### 📈 Sales Analytics
    Track revenue trends, analyze product performance, and monitor sales metrics across regions 
    and time periods. Identify top-performing products and optimize pricing strategies.
    
    #### 👥 Customer Intelligence
    Understand customer behavior through RFM analysis and segmentation. Identify high-value 
    customers, predict churn risk, and create targeted retention campaigns.
    
    #### 🔮 Demand Forecasting
    Leverage machine learning models (Prophet/ARIMA/LSTM) to predict future demand patterns. 
    Plan inventory and resources based on data-driven forecasts.
    
    #### 📦 Inventory Optimization
    Receive intelligent reorder recommendations, identify low-stock and overstock situations, 
    and maintain optimal inventory levels to reduce costs.
    """)

with col_right:
    st.markdown("### 🚀 Quick Start")
    
    st.markdown("""
    <div style="
        background-color: #f7f9fb;
        border: 1px solid #c3c6d7;
        border-radius: 0.75rem;
        padding: 1.25rem;
        margin-bottom: 1rem;
    ">
        <h4 style="margin-top: 0; color: #004ac6;">📊 Explore Dashboards</h4>
        <p style="font-size: 14px; color: #434655;">
            Navigate using the sidebar to access:
        </p>
        <ul style="font-size: 14px; color: #434655;">
            <li><strong>Sales Dashboard</strong> - Revenue & trends</li>
            <li><strong>Customer Dashboard</strong> - Segmentation</li>
            <li><strong>Forecast Dashboard</strong> - Predictions</li>
            <li><strong>Inventory Dashboard</strong> - Stock alerts</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="
        background-color: #6ffbbe;
        border: 1px solid #005236;
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="margin-top: 0; color: #005236;">✨ Key Features</h4>
        <ul style="font-size: 14px; color: #005236; margin-bottom: 0;">
            <li>Real-time KPI monitoring</li>
            <li>Interactive visualizations</li>
            <li>Advanced filtering options</li>
            <li>Export capabilities</li>
            <li>Mobile-responsive design</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# DATA OVERVIEW SECTION
# ============================================================================

st.markdown("### 📋 Data Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div style="
        background-color: white;
        border: 1px solid #c3c6d7;
        border-radius: 0.75rem;
        padding: 1.25rem;
        text-align: center;
    ">
        <p style="font-size: 12px; font-weight: 600; text-transform: uppercase; color: #434655; margin-bottom: 0.5rem;">
            Total Records
        </p>
        <h2 style="font-family: 'Hanken Grotesk', sans-serif; font-size: 32px; font-weight: 700; color: #191c1e; margin: 0;">
            {format_number(len(df))}
        </h2>
        <p style="font-size: 12px; color: #434655; margin-top: 0.5rem;">
            Transactions in database
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    date_range = "N/A"
    if 'InvoiceDate' in df.columns:
        min_date = df['InvoiceDate'].min().strftime('%b %Y')
        max_date = df['InvoiceDate'].max().strftime('%b %Y')
        date_range = f"{min_date} - {max_date}"
    
    st.markdown(f"""
    <div style="
        background-color: white;
        border: 1px solid #c3c6d7;
        border-radius: 0.75rem;
        padding: 1.25rem;
        text-align: center;
    ">
        <p style="font-size: 12px; font-weight: 600; text-transform: uppercase; color: #434655; margin-bottom: 0.5rem;">
            Date Range
        </p>
        <h3 style="font-family: 'Hanken Grotesk', sans-serif; font-size: 18px; font-weight: 600; color: #191c1e; margin: 0.5rem 0;">
            {date_range}
        </h3>
        <p style="font-size: 12px; color: #434655; margin-top: 0.5rem;">
            Historical data period
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    total_products = len(df['StockCode'].unique()) if 'StockCode' in df.columns else 0
    
    st.markdown(f"""
    <div style="
        background-color: white;
        border: 1px solid #c3c6d7;
        border-radius: 0.75rem;
        padding: 1.25rem;
        text-align: center;
    ">
        <p style="font-size: 12px; font-weight: 600; text-transform: uppercase; color: #434655; margin-bottom: 0.5rem;">
            Unique Products
        </p>
        <h2 style="font-family: 'Hanken Grotesk', sans-serif; font-size: 32px; font-weight: 700; color: #191c1e; margin: 0;">
            {format_number(total_products)}
        </h2>
        <p style="font-size: 12px; color: #434655; margin-top: 0.5rem;">
            SKUs in catalog
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# TEAM INFORMATION
# ============================================================================

st.markdown("### 👥 Project Team")

team_col1, team_col2, team_col3, team_col4 = st.columns(4)

with team_col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 48px; margin-bottom: 0.5rem;">🧹</div>
        <h4 style="margin: 0; color: #191c1e;">Member 1</h4>
        <p style="font-size: 12px; color: #434655; margin: 0.25rem 0;">Data Cleaning & EDA</p>
    </div>
    """, unsafe_allow_html=True)

with team_col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 48px; margin-bottom: 0.5rem;">👥</div>
        <h4 style="margin: 0; color: #191c1e;">Member 2</h4>
        <p style="font-size: 12px; color: #434655; margin: 0.25rem 0;">Customer Analytics</p>
    </div>
    """, unsafe_allow_html=True)

with team_col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 48px; margin-bottom: 0.5rem;">🔮</div>
        <h4 style="margin: 0; color: #191c1e;">Member 3</h4>
        <p style="font-size: 12px; color: #434655; margin: 0.25rem 0;">Demand Forecasting</p>
    </div>
    """, unsafe_allow_html=True)

with team_col4:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 48px; margin-bottom: 0.5rem;">🚀</div>
        <h4 style="margin: 0; color: #191c1e;">Member 4</h4>
        <p style="font-size: 12px; color: #434655; margin: 0.25rem 0;">Dashboard & Deployment</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0; color: #434655; font-size: 12px;">
    <p style="margin: 0;">© 2026 RetailPulse Analytics Management Suite</p>
    <p style="margin: 0.5rem 0 0 0;">AI-Powered Customer Analytics & Demand Forecasting Platform</p>
</div>
""", unsafe_allow_html=True)
