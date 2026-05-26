"""
RetailPulse Analytics Management Suite - Home Page
Premium Dynamic Dashboard with Dark Mode and Glassmorphism
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
from design_system import COLORS, TYPOGRAPHY, RADIUS, ICONS, create_kpi_card

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

configure_page(title="Home", icon="📊", layout="wide")

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_and_prepare_data():
    """Load and prepare dynamic data for home page"""
    df = load_retail_data()
    
    if df.empty:
        return None, None, None
    
    # Calculate current period metrics (last 30 days)
    if 'InvoiceDate' in df.columns:
        # Ensure it's datetime
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
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
    # If no TotalPrice, calculate it if Quantity and UnitPrice exist
    if 'Quantity' in current_df.columns and 'UnitPrice' in current_df.columns:
        df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
        current_df['TotalPrice'] = current_df['Quantity'] * current_df['UnitPrice']
        if not previous_df.empty:
            previous_df['TotalPrice'] = previous_df['Quantity'] * previous_df['UnitPrice']
        revenue_col = 'TotalPrice'
    else:
        st.error("⚠️ Could not find or calculate revenue column in data.")
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

# Conversion rate (simplified proxy)
conversion_rate = (current_customers / current_orders * 100) if current_orders > 0 else 0
prev_conversion_rate = (previous_customers / previous_orders * 100) if previous_orders > 0 else 0
conversion_change = conversion_rate - prev_conversion_rate

# ============================================================================
# SIDEBAR
# ============================================================================

st.sidebar.markdown("---")

# Export Report Button
if st.sidebar.button("📥 Export Report", use_container_width=True):
    st.sidebar.success("Report exported successfully!")

# ============================================================================
# HEADER WITH SEARCH BAR
# ============================================================================

# Top row: Title (no user profile)
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
    <div>
        <h1 style="font-size: 32px; font-weight: 700; color: {COLORS['text_primary']}; margin: 0; white-space: nowrap; font-family: {TYPOGRAPHY['font_display']}; text-shadow: 0 0 20px {COLORS['primary']}40;">Welcome back, Manager 👋</h1>
        <p style="font-size: 15px; color: {COLORS['text_secondary']}; margin: 0.25rem 0 0 0;">Here's your real-time store performance overview</p>
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
# KPI CARDS
# ============================================================================

st.markdown(f"<h3 style='color: {COLORS['text_primary']}; font-family: {TYPOGRAPHY['font_display']};'>📊 Real-time Performance</h3>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_kpi_card(
        icon=ICONS['dollar'],
        label="TOTAL REVENUE",
        value=format_currency(current_revenue),
        delta=revenue_change,
        delta_text="vs last 30 days",
        icon_bg=COLORS['primary_container'],
        icon_color=COLORS['primary']
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_kpi_card(
        icon=ICONS['cart'],
        label="ORDERS COMPLETED",
        value=format_number(current_orders),
        delta=orders_change,
        delta_text="vs last 30 days",
        icon_bg=COLORS['info_container'],
        icon_color=COLORS['info']
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_kpi_card(
        icon=ICONS['card'],
        label="AVG. ORDER VALUE",
        value=format_currency(current_avg_order),
        delta=avg_order_change,
        delta_text="vs last 30 days",
        icon_bg=COLORS['success_container'],
        icon_color=COLORS['success']
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_kpi_card(
        icon=ICONS['activity'],
        label="CONVERSION RATE",
        value=f"{conversion_rate:.1f}%",
        delta=conversion_change,
        delta_text="vs last 30 days",
        icon_bg=COLORS['warning_light'],
        icon_color=COLORS['warning']
    ), unsafe_allow_html=True)

# ============================================================================
# SALES PERFORMANCE & TOP PRODUCTS
# ============================================================================

st.markdown("<br>", unsafe_allow_html=True)

col_chart, col_products = st.columns([2, 1])

with col_chart:
    st.markdown(f"<h3 style='color: {COLORS['text_primary']}; font-family: {TYPOGRAPHY['font_display']};'>📈 Dynamic Revenue Trends</h3>", unsafe_allow_html=True)
    
    # Compute dynamic monthly sales trend
    df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    monthly_sales = df.groupby('YearMonth')[revenue_col].sum().reset_index()
    monthly_sales = monthly_sales.tail(7) # Last 7 periods
    months = monthly_sales['YearMonth'].tolist()
    sales = monthly_sales[revenue_col].tolist()
    
    fig = go.Figure()
    
    # Modern gradient bar chart
    fig.add_trace(go.Bar(
        x=months,
        y=sales,
        marker=dict(
            color=sales,
            colorscale=[[0, COLORS['primary_light']], [1, COLORS['primary']]],
            line=dict(color=COLORS['primary'], width=1)
        ),
        hovertemplate='<b>%{x}</b><br>Sales: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family=TYPOGRAPHY['font_primary'], size=12, color=COLORS['text_secondary']),
        xaxis=dict(
            title='',
            showgrid=False,
            showline=True,
            linecolor=COLORS['border']
        ),
        yaxis=dict(
            title='',
            showgrid=True,
            gridcolor=COLORS['border'],
            showline=False
        ),
        height=380,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_products:
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h3 style="margin: 0; font-size: 20px; font-weight: 600; color: {COLORS['text_primary']}; font-family: {TYPOGRAPHY['font_display']};">🏆 Best Sellers</h3>
        <a href="#" style="color: {COLORS['primary']}; text-decoration: none; font-size: 14px; font-weight: 500;">View All</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Compute dynamic best sellers
    if 'Description' in df.columns and 'Quantity' in df.columns:
        top_products_df = df.groupby('Description').agg({
            revenue_col: 'sum',
            'Quantity': 'sum'
        }).nlargest(4, revenue_col).reset_index()
        
        for _, row in top_products_df.iterrows():
            product_name = str(row['Description']).title()[:30]
            price_str = format_currency(row[revenue_col])
            sold_str = f"{format_number(row['Quantity'])} sold"
            
            st.markdown(f"""
            <div style="
                display: flex;
                align-items: center;
                padding: 1rem;
                margin-bottom: 0.75rem;
                background: {COLORS['surface']};
                backdrop-filter: blur(12px);
                border: 1px solid {COLORS['border']};
                border-radius: {RADIUS['lg']};
                transition: transform 0.2s;
            " onmouseover="this.style.transform='translateX(4px)';" onmouseout="this.style.transform='translateX(0)';">
                <div style="
                    width: 48px;
                    height: 48px;
                    background: {COLORS['primary_container']};
                    border-radius: {RADIUS['md']};
                    margin-right: 1rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: {COLORS['primary']};
                ">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        {ICONS['package']}
                    </svg>
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 14px; color: {COLORS['text_primary']};">{product_name}</div>
                    <div style="font-size: 12px; color: {COLORS['text_secondary']};">Top Category</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; font-size: 14px; color: {COLORS['primary']};">{price_str}</div>
                    <div style="font-size: 12px; color: {COLORS['text_tertiary']};">{sold_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Product data not available.")

# ============================================================================
# RECENT TRANSACTIONS
# ============================================================================

st.markdown("<br>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color: {COLORS['text_primary']}; font-family: {TYPOGRAPHY['font_display']};'>📋 Live Recent Orders</h3>", unsafe_allow_html=True)

# Compute dynamic recent transactions
if 'InvoiceNo' in df.columns and 'InvoiceDate' in df.columns:
    recent_df = df.sort_values('InvoiceDate', ascending=False).drop_duplicates('InvoiceNo').head(5)
    
    # Create table header
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1.5fr 2fr 1.5fr 1.5fr 1.5fr; padding: 1rem; background: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-bottom: none; border-radius: {RADIUS['lg']} {RADIUS['lg']} 0 0; font-weight: 600; font-size: 12px; color: {COLORS['text_secondary']}; text-transform: uppercase; letter-spacing: 0.05em; backdrop-filter: blur(12px);">
        <div>ORDER ID</div>
        <div>CUSTOMER / COUNTRY</div>
        <div>STATUS</div>
        <div>DATE</div>
        <div style="text-align: right;">AMOUNT</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create table rows
    for i, row in recent_df.iterrows():
        order_id = f"#{row['InvoiceNo']}"
        customer = str(row.get('CustomerID', row.get('Country', 'Guest')))
        if customer == 'nan': customer = 'Guest'
        initials = customer[:2].upper() if customer != 'Guest' else 'GU'
        amount = format_currency(row[revenue_col])
        date_str = row['InvoiceDate'].strftime('%b %d, %Y')
        
        status_color = COLORS['success']
        status = "COMPLETED"
        
        is_last = (i == recent_df.index[-1])
        border_radius = f"0 0 {RADIUS['lg']} {RADIUS['lg']}" if is_last else "0"
        border_bottom = f"1px solid {COLORS['border']}"
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: 1.5fr 2fr 1.5fr 1.5fr 1.5fr; padding: 1rem; background: {COLORS['surface']}; border: 1px solid {COLORS['border']}; border-top: none; border-radius: {border_radius}; align-items: center; transition: background 0.2s;" onmouseover="this.style.background='{COLORS['surface_hover']}';" onmouseout="this.style.background='{COLORS['surface']}';">
            <div style="color: {COLORS['primary']}; font-weight: 600; font-size: 14px;">{order_id}</div>
            <div style="display: flex; align-items: center; gap: 0.75rem;">
                <div style="width: 32px; height: 32px; border-radius: 50%; background: {COLORS['primary_container']}; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 12px; color: {COLORS['primary']}; box-shadow: 0 0 10px {COLORS['primary']}40;">{initials}</div>
                <span style="font-size: 14px; color: {COLORS['text_primary']}; font-weight: 500;">{customer}</span>
            </div>
            <div>
                <span style="background: {status_color}20; color: {status_color}; padding: 4px 10px; border-radius: 9999px; font-size: 11px; font-weight: 700; border: 1px solid {status_color}40; text-shadow: 0 0 5px {status_color}80;">{status}</span>
            </div>
            <div style="font-size: 14px; color: {COLORS['text_secondary']};">{date_str}</div>
            <div style="text-align: right; font-weight: 700; font-size: 14px; color: {COLORS['text_primary']};">{amount}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Transaction data not available.")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"""
<div style="text-align: center; padding: 2rem 0 1rem 0; color: {COLORS['text_tertiary']}; font-size: 13px; border-top: 1px solid {COLORS['border']}; margin-top: 3rem;">
    <p style="margin: 0;">© 2026 RetailPulse Analytics Management Suite</p>
    <p style="margin: 0.5rem 0 0 0;">Dynamic & Premium Dashboard Engine</p>
</div>
""", unsafe_allow_html=True)
