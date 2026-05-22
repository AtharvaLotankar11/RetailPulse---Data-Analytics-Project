"""
RetailPulse - Sales Dashboard
Revenue analytics, trends, and product performance
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    configure_page,
    load_retail_data,
    format_currency,
    format_number,
    add_sidebar_logo,
    add_sidebar_footer,
    create_download_button
)
from styles import COLORS

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

configure_page(title="Sales Dashboard", icon="📈", layout="wide")

# ============================================================================
# SIDEBAR
# ============================================================================

add_sidebar_logo()

st.sidebar.markdown("### 📈 Sales Dashboard")
st.sidebar.markdown("Analyze revenue trends, product performance, and sales metrics.")

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_and_prepare_sales_data():
    """Load and prepare sales data"""
    df = load_retail_data()
    
    if df.empty:
        return None
    
    # Ensure we have required columns
    required_cols = ['InvoiceDate']
    if not all(col in df.columns for col in required_cols):
        return None
    
    # Remove null dates
    df = df.dropna(subset=['InvoiceDate'])
    
    # Add time-based columns
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['MonthName'] = df['InvoiceDate'].dt.strftime('%B')
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['Date'] = df['InvoiceDate'].dt.date
    df['DayOfWeek'] = df['InvoiceDate'].dt.day_name()
    
    return df

df = load_and_prepare_sales_data()

# ============================================================================
# CHECK DATA AVAILABILITY
# ============================================================================

if df is None or df.empty:
    st.error("⚠️ No sales data available. Please ensure cleaned_retail.csv is in the data/ directory.")
    st.stop()

# Determine revenue column
revenue_col = None
for col in ['TotalPrice', 'Revenue', 'Amount', 'Total']:
    if col in df.columns:
        revenue_col = col
        break

if revenue_col is None:
    st.error("⚠️ Could not find revenue column in data.")
    st.stop()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

# Date range filter
min_date = df['InvoiceDate'].min().date()
max_date = df['InvoiceDate'].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle date range
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
else:
    filtered_df = df

# Country filter
if 'Country' in df.columns:
    countries = ['All'] + sorted(df['Country'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Country", countries)
    
    if selected_country != 'All':
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]

# Product filter (top 20 products)
if 'Description' in df.columns:
    top_products = df.groupby('Description')[revenue_col].sum().nlargest(20).index.tolist()
    products = ['All'] + top_products
    selected_product = st.sidebar.selectbox("Product (Top 20)", products, index=0)
    
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['Description'] == selected_product]

# Reset filters button
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

add_sidebar_footer()

# ============================================================================
# HEADER
# ============================================================================

st.markdown(f"""
<h1 style="
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: {COLORS['on_surface']};
    margin-bottom: 0.5rem;
">📈 Sales Dashboard</h1>
<p style="
    font-size: 14px;
    color: {COLORS['on_surface_variant']};
    margin-bottom: 2rem;
">Revenue analytics, trends, and product performance insights</p>
""", unsafe_allow_html=True)

# ============================================================================
# SALES KPI METRICS
# ============================================================================

col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
total_revenue = filtered_df[revenue_col].sum()
total_orders = len(filtered_df['InvoiceNo'].unique()) if 'InvoiceNo' in filtered_df.columns else len(filtered_df)
total_customers = len(filtered_df['CustomerID'].unique()) if 'CustomerID' in filtered_df.columns else 0
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

with col1:
    st.metric(
        label="💰 TOTAL REVENUE",
        value=format_currency(total_revenue),
        delta=None
    )

with col2:
    st.metric(
        label="🛒 TOTAL ORDERS",
        value=format_number(total_orders),
        delta=None
    )

with col3:
    st.metric(
        label="👥 UNIQUE CUSTOMERS",
        value=format_number(total_customers),
        delta=None
    )

with col4:
    st.metric(
        label="📦 AVG ORDER VALUE",
        value=format_currency(avg_order_value),
        delta=None
    )

st.markdown("---")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

# Row 1: Monthly Sales Trend & Top Products
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("### 📊 Monthly Sales Trend")
    
    # Aggregate by month
    monthly_sales = filtered_df.groupby('YearMonth')[revenue_col].sum().reset_index()
    monthly_sales.columns = ['Month', 'Revenue']
    
    if not monthly_sales.empty:
        fig_monthly = px.line(
            monthly_sales,
            x='Month',
            y='Revenue',
            title='',
            markers=True
        )
        
        fig_monthly.update_traces(
            line_color=COLORS['primary'],
            line_width=3,
            marker=dict(size=8, color=COLORS['primary_container'])
        )
        
        fig_monthly.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            xaxis=dict(
                title='Month',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            yaxis=dict(
                title='Revenue ($)',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_monthly, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with col_right:
    st.markdown("### 🏆 Top 10 Products")
    
    if 'Description' in filtered_df.columns:
        top_products_df = (
            filtered_df.groupby('Description')[revenue_col]
            .sum()
            .nlargest(10)
            .reset_index()
        )
        top_products_df.columns = ['Product', 'Revenue']
        
        if not top_products_df.empty:
            fig_top_products = px.bar(
                top_products_df,
                y='Product',
                x='Revenue',
                orientation='h',
                title=''
            )
            
            fig_top_products.update_traces(
                marker_color=COLORS['primary'],
                hovertemplate='<b>%{y}</b><br>Revenue: $%{x:,.2f}<extra></extra>'
            )
            
            fig_top_products.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=11),
                xaxis=dict(title='Revenue ($)', showgrid=True, gridcolor='#eceef0'),
                yaxis=dict(title='', showgrid=False),
                height=400,
                margin=dict(l=0, r=0, t=20, b=0)
            )
            
            st.plotly_chart(fig_top_products, use_container_width=True)
        else:
            st.info("No product data available.")
    else:
        st.info("Product description column not found.")

st.markdown("---")

# Row 2: Country-wise Revenue & Daily Trend
col_left2, col_right2 = st.columns([1, 2])

with col_left2:
    st.markdown("### 🌍 Top 10 Countries by Revenue")
    
    if 'Country' in filtered_df.columns:
        country_sales = (
            filtered_df.groupby('Country')[revenue_col]
            .sum()
            .nlargest(10)
            .reset_index()
        )
        country_sales.columns = ['Country', 'Revenue']
        
        if not country_sales.empty:
            fig_country = px.bar(
                country_sales,
                x='Country',
                y='Revenue',
                title=''
            )
            
            fig_country.update_traces(
                marker_color=COLORS['success'],
                hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>'
            )
            
            fig_country.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=11),
                xaxis=dict(title='Country', showgrid=False),
                yaxis=dict(title='Revenue ($)', showgrid=True, gridcolor='#eceef0'),
                height=400
            )
            
            st.plotly_chart(fig_country, use_container_width=True)
        else:
            st.info("No country data available.")
    else:
        st.info("Country column not found.")

with col_right2:
    st.markdown("### 📅 Daily Revenue Trend")
    
    daily_sales = filtered_df.groupby('Date')[revenue_col].sum().reset_index()
    daily_sales.columns = ['Date', 'Revenue']
    
    if not daily_sales.empty:
        fig_daily = px.area(
            daily_sales,
            x='Date',
            y='Revenue',
            title=''
        )
        
        fig_daily.update_traces(
            line_color=COLORS['primary'],
            fillcolor=f"rgba(0, 74, 198, 0.2)"
        )
        
        fig_daily.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            xaxis=dict(
                title='Date',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            yaxis=dict(
                title='Revenue ($)',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_daily, use_container_width=True)
    else:
        st.info("No daily data available.")

st.markdown("---")

# ============================================================================
# RECENT TRANSACTIONS TABLE
# ============================================================================

st.markdown("### 📋 Recent Transactions")

# Prepare table data
table_cols = ['InvoiceNo', 'InvoiceDate', 'Description', 'Quantity', revenue_col, 'Country']
available_cols = [col for col in table_cols if col in filtered_df.columns]

if available_cols:
    recent_transactions = filtered_df[available_cols].sort_values('InvoiceDate', ascending=False).head(20)
    
    # Format the dataframe
    display_df = recent_transactions.copy()
    if 'InvoiceDate' in display_df.columns:
        display_df['InvoiceDate'] = display_df['InvoiceDate'].dt.strftime('%Y-%m-%d %H:%M')
    if revenue_col in display_df.columns:
        display_df[revenue_col] = display_df[revenue_col].apply(lambda x: f"${x:,.2f}")
    
    # Rename columns for display
    column_config = {
        'InvoiceNo': 'Order ID',
        'InvoiceDate': 'Date',
        'Description': 'Product',
        'Quantity': 'Qty',
        revenue_col: 'Amount',
        'Country': 'Country'
    }
    
    display_df = display_df.rename(columns=column_config)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Download button
    st.markdown("### 📥 Export Data")
    create_download_button(
        filtered_df[available_cols],
        "sales_data_export.csv",
        "📥 Download Filtered Sales Data"
    )
else:
    st.info("Transaction data not available.")

# ============================================================================
# ADDITIONAL INSIGHTS
# ============================================================================

st.markdown("---")
st.markdown("### 💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    if 'DayOfWeek' in filtered_df.columns:
        best_day = filtered_df.groupby('DayOfWeek')[revenue_col].sum().idxmax()
        best_day_revenue = filtered_df.groupby('DayOfWeek')[revenue_col].sum().max()
        
        st.markdown(f"""
        <div style="
            background-color: {COLORS['success_container']};
            border-radius: 0.75rem;
            padding: 1.25rem;
            text-align: center;
        ">
            <p style="font-size: 12px; font-weight: 600; color: {COLORS['on_success_fixed_variant']}; margin: 0;">
                BEST SALES DAY
            </p>
            <h3 style="font-size: 24px; font-weight: 700; color: {COLORS['on_success_fixed_variant']}; margin: 0.5rem 0;">
                {best_day}
            </h3>
            <p style="font-size: 14px; color: {COLORS['on_success_fixed_variant']}; margin: 0;">
                {format_currency(best_day_revenue)}
            </p>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if 'Description' in filtered_df.columns:
        top_product = filtered_df.groupby('Description')[revenue_col].sum().idxmax()
        top_product_revenue = filtered_df.groupby('Description')[revenue_col].sum().max()
        
        st.markdown(f"""
        <div style="
            background-color: {COLORS['info_container']};
            border-radius: 0.75rem;
            padding: 1.25rem;
            text-align: center;
        ">
            <p style="font-size: 12px; font-weight: 600; color: {COLORS['on_info_fixed_variant']}; margin: 0;">
                TOP PRODUCT
            </p>
            <h3 style="font-size: 16px; font-weight: 700; color: {COLORS['on_info_fixed_variant']}; margin: 0.5rem 0;">
                {top_product[:30]}...
            </h3>
            <p style="font-size: 14px; color: {COLORS['on_info_fixed_variant']}; margin: 0;">
                {format_currency(top_product_revenue)}
            </p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    avg_daily_revenue = filtered_df.groupby('Date')[revenue_col].sum().mean()
    
    st.markdown(f"""
    <div style="
        background-color: white;
        border: 1px solid {COLORS['outline_variant']};
        border-radius: 0.75rem;
        padding: 1.25rem;
        text-align: center;
    ">
        <p style="font-size: 12px; font-weight: 600; color: {COLORS['on_surface_variant']}; margin: 0;">
            AVG DAILY REVENUE
        </p>
        <h3 style="font-size: 24px; font-weight: 700; color: {COLORS['on_surface']}; margin: 0.5rem 0;">
            {format_currency(avg_daily_revenue)}
        </h3>
        <p style="font-size: 14px; color: {COLORS['on_surface_variant']}; margin: 0;">
            Per day average
        </p>
    </div>
    """, unsafe_allow_html=True)
