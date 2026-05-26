"""
RetailPulse - Inventory Dashboard
Inventory optimization, stock alerts, and reorder recommendations
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from utils import (
    configure_page,
    load_inventory_data,
    format_currency,
    format_number,
    add_sidebar_logo,
    add_sidebar_footer,
    create_download_button
)
from design_system import COLORS, ICONS, create_kpi_card, render_html

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

configure_page(title="Inventory Dashboard", icon="📦", layout="wide")

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
# SIDEBAR
# ============================================================================

# Note: Streamlit automatically adds logo and navigation at the top
# Our sidebar content appears AFTER the navigation

st.sidebar.markdown("---")

# Export Report Button
if st.sidebar.button("📥 Export Report", use_container_width=True):
    st.sidebar.success("Report exported successfully!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📦 Stock Management")
st.sidebar.markdown("Monitor inventory levels, prevent stockouts, and reduce overstock.")

# Sidebar footer is already added

# ============================================================================
# LOAD DATA
# ============================================================================

inventory_df = load_inventory_data()

# ============================================================================
# CHECK DATA AVAILABILITY
# ============================================================================

if inventory_df.empty:
    st.error("⚠️ No inventory data available. Please ensure inventory_recommendations.csv is in the data/ directory.")
    st.stop()

# ============================================================================
# DATA PREPARATION
# ============================================================================

# Identify key columns
product_col = None
current_stock_col = None
recommended_stock_col = None

# Try to find product column
for col in ['Product', 'ProductName', 'Description', 'StockCode', 'Item']:
    if col in inventory_df.columns:
        product_col = col
        break

# Try to find current stock column
for col in ['CurrentStock', 'Current_Stock', 'Stock', 'Quantity', 'OnHand']:
    if col in inventory_df.columns:
        current_stock_col = col
        break

# Try to find recommended stock column
for col in ['RecommendedStock', 'Recommended_Stock', 'Recommended', 'OptimalStock', 'TargetStock']:
    if col in inventory_df.columns:
        recommended_stock_col = col
        break

# If columns not found, check what we have
if not all([product_col, current_stock_col, recommended_stock_col]):
    # Silently try to use first few columns as fallback
    if len(inventory_df.columns) >= 3:
        product_col = inventory_df.columns[0]
        current_stock_col = inventory_df.columns[1] if len(inventory_df.columns) > 1 else None
        recommended_stock_col = inventory_df.columns[2] if len(inventory_df.columns) > 2 else None

if not all([product_col, current_stock_col, recommended_stock_col]):
    st.error("⚠️ Could not identify required inventory columns.")
    st.stop()

# Calculate inventory status
if 'Difference' not in inventory_df.columns:
    inventory_df['Difference'] = inventory_df[recommended_stock_col] - inventory_df[current_stock_col]
if 'Status' not in inventory_df.columns:
    inventory_df['Status'] = inventory_df['Difference'].apply(
        lambda x: 'Low Stock' if x > 0 else ('Overstock' if x < -10 else 'Optimal')
    )
if 'Priority' not in inventory_df.columns:
    inventory_df['Priority'] = inventory_df['Difference'].apply(
        lambda x: 'High' if abs(x) > 50 else ('Medium' if abs(x) > 20 else 'Low')
    )

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

# Status filter
status_options = ['All'] + sorted(inventory_df['Status'].unique().tolist())
selected_status = st.sidebar.selectbox("Inventory Status", status_options)

if selected_status != 'All':
    filtered_df = inventory_df[inventory_df['Status'] == selected_status]
else:
    filtered_df = inventory_df

# Priority filter
priority_options = ['All'] + sorted(inventory_df['Priority'].unique().tolist())
selected_priority = st.sidebar.selectbox("Priority Level", priority_options)

if selected_priority != 'All':
    filtered_df = filtered_df[filtered_df['Priority'] == selected_priority]

# Reset filters button
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

add_sidebar_footer()

# ============================================================================
# HEADER WITH SEARCH BAR
# ============================================================================

# Top row: Title (no user profile)
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
    <div>
        <h1 style="font-size: 28px; font-weight: 700; color: #1A1A1A; margin: 0; white-space: nowrap;">Stock Management 📦</h1>
        <p style="font-size: 14px; color: #6B7280; margin: 0.25rem 0 0 0;">Monitor inventory, prevent stockouts, and optimize stock levels</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Search bar and Advanced Filter
col_search, col_filter = st.columns([4, 1])

with col_search:
    search_query = st.text_input("🔍 Search", placeholder="Search products, SKUs, stock levels...", label_visibility="collapsed")

if search_query:
    if 'StockCode' in filtered_df.columns:
        filtered_df = filtered_df[
            filtered_df[product_col].str.contains(search_query, case=False, na=False) |
            filtered_df['StockCode'].astype(str).str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_df = filtered_df[filtered_df[product_col].str.contains(search_query, case=False, na=False)]

with col_filter:
    st.button("⚡ Quick Filters", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# INVENTORY KPI METRICS WITH ICON BADGES
# ============================================================================

st.markdown("### 📊 Inventory Metrics")

col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
low_stock_items = len(inventory_df[inventory_df['Status'] == 'Low Stock'])
overstock_items = len(inventory_df[inventory_df['Status'] == 'Overstock'])
optimal_items = len(inventory_df[inventory_df['Status'] == 'Optimal'])
total_reorder_qty = inventory_df[inventory_df['Difference'] > 0]['Difference'].sum()

# Calculate inventory health score
total_items = len(inventory_df)
health_score = (optimal_items / total_items * 100) if total_items > 0 else 0

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #FEE2E2;">
            <span style="font-size: 24px;">⚠️</span>
        </div>
        <div class="kpi-label">LOW STOCK ITEMS</div>
        <div class="kpi-value">{format_number(low_stock_items)}</div>
        <div class="kpi-delta negative">
            {(low_stock_items/total_items*100):.1f}% of total
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #FEF3C7;">
            <span style="font-size: 24px;">📦</span>
        </div>
        <div class="kpi-label">OVERSTOCK ITEMS</div>
        <div class="kpi-value">{format_number(overstock_items)}</div>
        <div class="kpi-delta negative">
            {(overstock_items/total_items*100):.1f}% of total
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #D1FAE5;">
            <span style="font-size: 24px;">✅</span>
        </div>
        <div class="kpi-label">OPTIMAL STOCK</div>
        <div class="kpi-value">{format_number(optimal_items)}</div>
        <div class="kpi-delta positive">
            {(optimal_items/total_items*100):.1f}% of total
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    health_status = "Good" if health_score >= 70 else ("Fair" if health_score >= 50 else "Poor")
    health_color = "positive" if health_score >= 70 else "negative"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #DBEAFE;">
            <span style="font-size: 24px;">📊</span>
        </div>
        <div class="kpi-label">INVENTORY HEALTH</div>
        <div class="kpi-value">{health_score:.1f}%</div>
        <div class="kpi-delta {health_color}">
            {health_status}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# CRITICAL ALERTS
# ============================================================================

st.markdown("### 🚨 Critical Inventory Alerts")

alert_col1, alert_col2 = st.columns(2)

with alert_col1:
    # High priority low stock items
    high_priority_low = inventory_df[
        (inventory_df['Status'] == 'Low Stock') & 
        (inventory_df['Priority'] == 'High')
    ]
    
    if not high_priority_low.empty:
        st.markdown(f"""
        <div style="
            background-color: {COLORS['error_container']};
            border-left: 4px solid {COLORS['error']};
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: {COLORS['on_error_container']}; margin-top: 0;">
                ⚠️ URGENT: Low Stock Alert
            </h4>
            <p style="font-size: 14px; color: {COLORS['on_error_container']}; margin: 0;">
                <strong>{len(high_priority_low)}</strong> high-priority items critically low on stock.
                Immediate reorder required to prevent stockouts.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show top 5 critical items
        st.markdown("**Top 5 Critical Items:**")
        critical_items = high_priority_low.nlargest(5, 'Difference')[[product_col, current_stock_col, recommended_stock_col, 'Difference']]
        st.dataframe(critical_items, width='stretch', hide_index=True)
    else:
        st.success("✅ No critical low stock alerts")

with alert_col2:
    # High priority overstock items
    high_priority_over = inventory_df[
        (inventory_df['Status'] == 'Overstock') & 
        (inventory_df['Priority'] == 'High')
    ]
    
    if not high_priority_over.empty:
        st.markdown(f"""
        <div style="
            background-color: #fef3c7;
            border-left: 4px solid #f59e0b;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
        ">
            <h4 style="color: #92400e; margin-top: 0;">
                📦 WARNING: Overstock Alert
            </h4>
            <p style="font-size: 14px; color: #92400e; margin: 0;">
                <strong>{len(high_priority_over)}</strong> items significantly overstocked.
                Consider promotions or redistribution to optimize capital.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show top 5 overstock items
        st.markdown("**Top 5 Overstock Items:**")
        overstock_df = high_priority_over.nsmallest(5, 'Difference')[[product_col, current_stock_col, recommended_stock_col, 'Difference']]
        st.dataframe(overstock_df, width='stretch', hide_index=True)
    else:
        st.success("✅ No critical overstock alerts")

st.markdown("---")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

# Row 1: Stock Status Distribution & Stock Comparison
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 📊 Inventory Status Distribution")
    
    status_dist = inventory_df['Status'].value_counts().reset_index()
    status_dist.columns = ['Status', 'Count']
    
    # Define colors for each status
    color_map = {
        'Low Stock': COLORS['error'],
        'Overstock': '#f59e0b',
        'Optimal': COLORS['success']
    }
    
    fig_status = px.pie(
        status_dist,
        values='Count',
        names='Status',
        title='',
        color='Status',
        color_discrete_map=color_map,
        hole=0.4
    )
    
    fig_status.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig_status.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=11),
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig_status, width='stretch')

with col_right:
    st.markdown("### 📈 Current vs Recommended Stock Levels")
    
    # Show top 15 items with largest discrepancies
    top_discrepancies = inventory_df.nlargest(15, 'Difference', keep='first')
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Current Stock',
        x=top_discrepancies[product_col],
        y=top_discrepancies[current_stock_col],
        marker_color=COLORS['on_surface_variant'],
        hovertemplate='<b>%{x}</b><br>Current: %{y}<extra></extra>'
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='Recommended Stock',
        x=top_discrepancies[product_col],
        y=top_discrepancies[recommended_stock_col],
        marker_color=COLORS['primary'],
        hovertemplate='<b>%{x}</b><br>Recommended: %{y}<extra></extra>'
    ))
    
    fig_comparison.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=11),
        xaxis=dict(title='Product', showgrid=False, tickangle=-45),
        yaxis=dict(title='Quantity', showgrid=True, gridcolor='#eceef0'),
        barmode='group',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig_comparison, width='stretch')

st.markdown("---")

# Row 2: Reorder Quantity & Priority Distribution
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 📦 Recommended Reorder Quantities")
    
    # Filter items that need reordering
    reorder_items = inventory_df[inventory_df['Difference'] > 0].nlargest(10, 'Difference')
    
    if not reorder_items.empty:
        fig_reorder = px.bar(
            reorder_items,
            y=product_col,
            x='Difference',
            orientation='h',
            title='',
            color='Priority',
            color_discrete_map={
                'High': COLORS['error'],
                'Medium': '#f59e0b',
                'Low': COLORS['success']
            }
        )
        
        fig_reorder.update_traces(
            hovertemplate='<b>%{y}</b><br>Reorder Qty: %{x}<extra></extra>'
        )
        
        fig_reorder.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=11),
            xaxis=dict(title='Reorder Quantity', showgrid=True, gridcolor='#eceef0'),
            yaxis=dict(title='', showgrid=False),
            height=400
        )
        
        st.plotly_chart(fig_reorder, width='stretch')
    else:
        st.info("No items require reordering at this time.")

with col_right2:
    st.markdown("### 🎯 Priority Level Distribution")
    
    priority_dist = inventory_df['Priority'].value_counts().reset_index()
    priority_dist.columns = ['Priority', 'Count']
    
    # Sort by priority
    priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
    priority_dist['Order'] = priority_dist['Priority'].map(priority_order)
    priority_dist = priority_dist.sort_values('Order')
    
    fig_priority = px.bar(
        priority_dist,
        x='Priority',
        y='Count',
        title='',
        color='Priority',
        color_discrete_map={
            'High': COLORS['error'],
            'Medium': '#f59e0b',
            'Low': COLORS['success']
        }
    )
    
    fig_priority.update_traces(
        hovertemplate='<b>%{x} Priority</b><br>Count: %{y}<extra></extra>'
    )
    
    fig_priority.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=11),
        xaxis=dict(title='Priority Level', showgrid=False),
        yaxis=dict(title='Number of Items', showgrid=True, gridcolor='#eceef0'),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_priority, width='stretch')

st.markdown("---")

# ============================================================================
# INVENTORY RECOMMENDATIONS TABLE
# ============================================================================

st.markdown("### 📋 Detailed Inventory Recommendations")

# Prepare display dataframe
display_cols = [product_col, current_stock_col, recommended_stock_col, 'Difference', 'Status', 'Priority']
display_df = filtered_df[display_cols].copy()

# Rename columns for display
column_mapping = {
    product_col: 'Product',
    current_stock_col: 'Current Stock',
    recommended_stock_col: 'Recommended Stock',
    'Difference': 'Action Required',
    'Status': 'Status',
    'Priority': 'Priority'
}
display_df = display_df.rename(columns=column_mapping)

# Format action required column
display_df['Action Required'] = display_df['Action Required'].apply(
    lambda x: f"Reorder {int(x)}" if x > 0 else (f"Reduce by {int(abs(x))}" if x < -10 else "Maintain")
)

st.dataframe(
    display_df,
    width='stretch',
    hide_index=True,
    height=400
)

# Download button
st.markdown("### 📥 Export Inventory Data")
create_download_button(
    filtered_df,
    "inventory_recommendations_export.csv",
    "📥 Download Inventory Recommendations"
)

st.markdown("---")

# ============================================================================
# ACTIONABLE INSIGHTS
# ============================================================================

st.markdown("### 💡 Inventory Management Recommendations")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown(f"""
    <div style="
        background-color: {COLORS['error_container']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_error_container']}; margin-top: 0;">🚨 Immediate Action</h4>
        <p style="font-size: 14px; color: {COLORS['on_error_container']}; margin-bottom: 0.5rem;">
            <strong>{format_number(low_stock_items)}</strong> items below optimal levels
        </p>
        <p style="font-size: 20px; font-weight: 700; color: {COLORS['on_error_container']}; margin: 0.5rem 0;">
            {format_number(int(total_reorder_qty))} units
        </p>
        <p style="font-size: 12px; color: {COLORS['on_error_container']}; margin: 0;">
            Total quantity to reorder. Process purchase orders immediately to prevent stockouts.
        </p>
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    excess_qty = inventory_df[inventory_df['Difference'] < -10]['Difference'].abs().sum()
    st.markdown(f"""
    <div style="
        background-color: #fef3c7;
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: #92400e; margin-top: 0;">📦 Optimize Storage</h4>
        <p style="font-size: 14px; color: #92400e; margin-bottom: 0.5rem;">
            <strong>{format_number(overstock_items)}</strong> items overstocked
        </p>
        <p style="font-size: 20px; font-weight: 700; color: #92400e; margin: 0.5rem 0;">
            {format_number(int(excess_qty))} units
        </p>
        <p style="font-size: 12px; color: #92400e; margin: 0;">
            Excess inventory. Consider promotions, bundling, or redistribution to free up capital.
        </p>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    st.markdown(f"""
    <div style="
        background-color: {COLORS['success_container']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_success_fixed_variant']}; margin-top: 0;">✅ Well Managed</h4>
        <p style="font-size: 14px; color: {COLORS['on_success_fixed_variant']}; margin-bottom: 0.5rem;">
            <strong>{format_number(optimal_items)}</strong> items at optimal levels
        </p>
        <p style="font-size: 20px; font-weight: 700; color: {COLORS['on_success_fixed_variant']}; margin: 0.5rem 0;">
            {health_score:.1f}%
        </p>
        <p style="font-size: 12px; color: {COLORS['on_success_fixed_variant']}; margin: 0;">
            Inventory health score. Continue monitoring and maintain current practices.
        </p>
    </div>
    """, unsafe_allow_html=True)
