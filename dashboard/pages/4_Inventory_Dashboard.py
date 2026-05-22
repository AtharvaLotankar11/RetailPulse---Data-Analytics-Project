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
from styles import COLORS

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

configure_page(title="Inventory Dashboard", icon="📦", layout="wide")

# ============================================================================
# SIDEBAR
# ============================================================================

add_sidebar_logo()

st.sidebar.markdown("### 📦 Inventory Dashboard")
st.sidebar.markdown("Inventory optimization, stock alerts, and intelligent reorder recommendations.")

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
    st.warning(f"⚠️ Some inventory columns not found. Available columns: {list(inventory_df.columns)}")
    
    # Try to use first few columns as fallback
    if len(inventory_df.columns) >= 3:
        product_col = inventory_df.columns[0]
        current_stock_col = inventory_df.columns[1] if len(inventory_df.columns) > 1 else None
        recommended_stock_col = inventory_df.columns[2] if len(inventory_df.columns) > 2 else None
        st.info(f"Using columns: Product={product_col}, Current={current_stock_col}, Recommended={recommended_stock_col}")

if not all([product_col, current_stock_col, recommended_stock_col]):
    st.error("⚠️ Could not identify required inventory columns.")
    st.stop()

# Calculate inventory status
inventory_df['Difference'] = inventory_df[recommended_stock_col] - inventory_df[current_stock_col]
inventory_df['Status'] = inventory_df['Difference'].apply(
    lambda x: 'Low Stock' if x > 0 else ('Overstock' if x < -10 else 'Optimal')
)
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
# HEADER
# ============================================================================

st.markdown(f"""
<h1 style="
    font-family: 'Hanken Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: {COLORS['on_surface']};
    margin-bottom: 0.5rem;
">📦 Inventory Dashboard</h1>
<p style="
    font-size: 14px;
    color: {COLORS['on_surface_variant']};
    margin-bottom: 2rem;
">Inventory optimization, stock alerts, and intelligent reorder recommendations</p>
""", unsafe_allow_html=True)

# ============================================================================
# INVENTORY KPI METRICS
# ============================================================================

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
    st.metric(
        label="⚠️ LOW STOCK ITEMS",
        value=format_number(low_stock_items),
        delta=f"{(low_stock_items/total_items*100):.1f}% of total" if total_items > 0 else "0%",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="📦 OVERSTOCK ITEMS",
        value=format_number(overstock_items),
        delta=f"{(overstock_items/total_items*100):.1f}% of total" if total_items > 0 else "0%",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="✅ OPTIMAL STOCK",
        value=format_number(optimal_items),
        delta=f"{(optimal_items/total_items*100):.1f}% of total" if total_items > 0 else "0%"
    )

with col4:
    st.metric(
        label="📊 INVENTORY HEALTH",
        value=f"{health_score:.1f}%",
        delta="Good" if health_score >= 70 else ("Fair" if health_score >= 50 else "Poor")
    )

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
        st.dataframe(critical_items, use_container_width=True, hide_index=True)
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
        overstock_items = high_priority_over.nsmallest(5, 'Difference')[[product_col, current_stock_col, recommended_stock_col, 'Difference']]
        st.dataframe(overstock_items, use_container_width=True, hide_index=True)
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
    
    st.plotly_chart(fig_status, use_container_width=True)

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
    
    st.plotly_chart(fig_comparison, use_container_width=True)

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
        
        st.plotly_chart(fig_reorder, use_container_width=True)
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
    
    st.plotly_chart(fig_priority, use_container_width=True)

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
    use_container_width=True,
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
