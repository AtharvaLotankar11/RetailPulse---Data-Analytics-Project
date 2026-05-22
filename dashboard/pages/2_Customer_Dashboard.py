"""
RetailPulse - Customer Dashboard
Customer segmentation, RFM analysis, and churn analytics
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
    load_customer_segments,
    load_retail_data,
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

configure_page(title="Customer Dashboard", icon="👥", layout="wide")

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
st.sidebar.markdown("### 👥 Customer Insights")
st.sidebar.markdown("Understand your customers, segment audiences, and boost loyalty.")

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
def load_customer_data():
    """Load customer segmentation data"""
    segments_df = load_customer_segments()
    retail_df = load_retail_data()
    
    return segments_df, retail_df

segments_df, retail_df = load_customer_data()

# ============================================================================
# CHECK DATA AVAILABILITY
# ============================================================================

if segments_df.empty:
    st.error("⚠️ No customer segmentation data available. Please ensure customer_segments.csv is in the data/ directory.")
    st.stop()

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

# Segment filter - use 'Cluster' column from YOUR data
segment_col = 'Cluster' if 'Cluster' in segments_df.columns else 'Segment'

if segment_col in segments_df.columns:
    segments = ['All'] + sorted(segments_df[segment_col].dropna().unique().tolist())
    selected_segment = st.sidebar.selectbox("Customer Segment", segments)
    
    if selected_segment != 'All':
        filtered_df = segments_df[segments_df[segment_col] == selected_segment]
    else:
        filtered_df = segments_df
else:
    filtered_df = segments_df
    selected_segment = 'All'

# Reset filters button
if st.sidebar.button("🔄 Reset Filters"):
    st.rerun()

add_sidebar_footer()

# ============================================================================
# HEADER WITH SEARCH BAR
# ============================================================================

# Top row: Title and User Profile
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
    <div>
        <h1 style="font-size: 28px; font-weight: 700; color: #1A1A1A; margin: 0; white-space: nowrap;">Customer Insights 👥</h1>
        <p style="font-size: 14px; color: #6B7280; margin: 0.25rem 0 0 0;">Understand your audience and drive customer loyalty</p>
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
    st.text_input("🔍 Search", placeholder="Search customers, segments, purchase history...", label_visibility="collapsed")

with col_filter:
    st.button("⚡ Quick Filters", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# CUSTOMER KPI METRICS WITH ICON BADGES
# ============================================================================

st.markdown("### 📊 Customer Metrics")

col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
total_customers = len(filtered_df)

# Count segments - use Cluster column
segment_col = 'Cluster' if 'Cluster' in filtered_df.columns else 'Segment'

if segment_col in filtered_df.columns:
    segment_counts = filtered_df[segment_col].value_counts()
    
    # For Cluster data (numeric), categorize by cluster number
    if segment_col == 'Cluster':
        # Cluster 0 = At Risk, Cluster 1 = Loyal, Cluster 2 = Premium (example mapping)
        premium_customers = segment_counts.get(2, 0) if 2 in segment_counts.index else 0
        at_risk_customers = segment_counts.get(0, 0) if 0 in segment_counts.index else 0
        loyal_customers = segment_counts.get(1, 0) if 1 in segment_counts.index else 0
    else:
        # Try to identify premium/high-value customers
        premium_keywords = ['Premium', 'Champions', 'Loyal', 'VIP', 'High']
        premium_customers = sum([segment_counts.get(seg, 0) for seg in segment_counts.index 
                                if any(keyword in str(seg) for keyword in premium_keywords)])
        
        # Try to identify at-risk customers
        risk_keywords = ['At Risk', 'Hibernating', 'Lost', 'Churn', 'About to Sleep']
        at_risk_customers = sum([segment_counts.get(seg, 0) for seg in segment_counts.index 
                                if any(keyword in str(seg) for keyword in risk_keywords)])
        
        # Loyal customers
        loyal_keywords = ['Loyal', 'Champions', 'Potential Loyalist']
        loyal_customers = sum([segment_counts.get(seg, 0) for seg in segment_counts.index 
                              if any(keyword in str(seg) for keyword in loyal_keywords)])
else:
    premium_customers = 0
    at_risk_customers = 0
    loyal_customers = 0

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #EFF6FF;">
            <span style="font-size: 24px;">👥</span>
        </div>
        <div class="kpi-label">TOTAL CUSTOMERS</div>
        <div class="kpi-value">{format_number(total_customers)}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #FCE7F3;">
            <span style="font-size: 24px;">⭐</span>
        </div>
        <div class="kpi-label">PREMIUM CUSTOMERS</div>
        <div class="kpi-value">{format_number(premium_customers)}</div>
        <div class="kpi-delta positive">
            {(premium_customers/total_customers*100):.1f}% of total
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #D1FAE5;">
            <span style="font-size: 24px;">💚</span>
        </div>
        <div class="kpi-label">LOYAL CUSTOMERS</div>
        <div class="kpi-value">{format_number(loyal_customers)}</div>
        <div class="kpi-delta positive">
            {(loyal_customers/total_customers*100):.1f}% of total
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #FEE2E2;">
            <span style="font-size: 24px;">⚠️</span>
        </div>
        <div class="kpi-label">AT-RISK CUSTOMERS</div>
        <div class="kpi-value">{format_number(at_risk_customers)}</div>
        <div class="kpi-delta negative">
            {(at_risk_customers/total_customers*100):.1f}% of total
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# VISUALIZATIONS
# ============================================================================

# Row 1: Segment Distribution & RFM Scatter
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 📊 Customer Segment Distribution")
    
    segment_col = 'Cluster' if 'Cluster' in segments_df.columns else 'Segment'
    
    if segment_col in segments_df.columns:
        segment_dist = segments_df[segment_col].value_counts().reset_index()
        segment_dist.columns = [segment_col, 'Count']
        
        if not segment_dist.empty:
            fig_segments = px.pie(
                segment_dist,
                values='Count',
                names=segment_col,
                title='',
                hole=0.4
            )
            
            fig_segments.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            )
            
            fig_segments.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=11),
                height=400,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.05
                )
            )
            
            st.plotly_chart(fig_segments, width='stretch')
        else:
            st.info("No segment data available.")
    else:
        st.info("Segment column not found in data.")

with col_right:
    st.markdown("### 🎯 RFM Analysis Scatter Plot")
    
    # Check for RFM columns
    rfm_cols = []
    for col_set in [
        ['Recency', 'Frequency', 'Monetary'],
        ['R', 'F', 'M'],
        ['recency', 'frequency', 'monetary']
    ]:
        if all(col in filtered_df.columns for col in col_set):
            rfm_cols = col_set
            break
    
    if len(rfm_cols) == 3:
        recency_col, frequency_col, monetary_col = rfm_cols
        
        # Create scatter plot
        fig_rfm = px.scatter(
            filtered_df,
            x=recency_col,
            y=frequency_col,
            size=monetary_col,
            color='Segment' if 'Segment' in filtered_df.columns else None,
            title='',
            hover_data=[monetary_col]
        )
        
        fig_rfm.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            xaxis=dict(
                title='Recency (days)',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            yaxis=dict(
                title='Frequency (orders)',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            height=400
        )
        
        st.plotly_chart(fig_rfm, width='stretch')
    else:
        st.info("RFM columns (Recency, Frequency, Monetary) not found in data.")

st.markdown("---")

# Row 2: Customer Value Distribution & Segment Comparison
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.markdown("### 💰 Customer Lifetime Value Distribution")
    
    # Try to find monetary/value column
    value_col = None
    for col in ['Monetary', 'M', 'monetary', 'TotalSpend', 'Revenue']:
        if col in filtered_df.columns:
            value_col = col
            break
    
    if value_col:
        fig_clv = px.histogram(
            filtered_df,
            x=value_col,
            nbins=30,
            title='',
            color='Segment' if 'Segment' in filtered_df.columns else None
        )
        
        fig_clv.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            xaxis=dict(
                title='Customer Lifetime Value ($)',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            yaxis=dict(
                title='Number of Customers',
                showgrid=True,
                gridcolor='#eceef0'
            ),
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig_clv, width='stretch')
    else:
        st.info("Customer value column not found.")

with col_right2:
    st.markdown("### 📈 Segment Performance Comparison")
    
    if 'Segment' in segments_df.columns and value_col:
        segment_performance = segments_df.groupby('Segment').agg({
            value_col: ['mean', 'sum', 'count']
        }).reset_index()
        
        segment_performance.columns = ['Segment', 'Avg_Value', 'Total_Value', 'Count']
        segment_performance = segment_performance.sort_values('Total_Value', ascending=True)
        
        fig_segment_perf = px.bar(
            segment_performance,
            y='Segment',
            x='Total_Value',
            orientation='h',
            title='',
            text='Total_Value'
        )
        
        fig_segment_perf.update_traces(
            marker_color=COLORS['primary'],
            texttemplate='$%{text:,.0f}',
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Total Value: $%{x:,.2f}<extra></extra>'
        )
        
        fig_segment_perf.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=11),
            xaxis=dict(title='Total Revenue ($)', showgrid=True, gridcolor='#eceef0'),
            yaxis=dict(title='', showgrid=False),
            height=400
        )
        
        st.plotly_chart(fig_segment_perf, width='stretch')
    else:
        st.info("Segment performance data not available.")

st.markdown("---")

# ============================================================================
# CUSTOMER INSIGHTS TABLE
# ============================================================================

st.markdown("### 📋 Customer Segments Details")

# Prepare display columns
display_cols = []
col_mapping = {}

# Standard columns to show
preferred_cols = ['CustomerID', 'Segment', 'Recency', 'Frequency', 'Monetary', 'R', 'F', 'M']
for col in preferred_cols:
    if col in filtered_df.columns:
        display_cols.append(col)
        # Create friendly names
        if col == 'CustomerID':
            col_mapping[col] = 'Customer ID'
        elif col in ['R', 'Recency']:
            col_mapping[col] = 'Recency (days)'
        elif col in ['F', 'Frequency']:
            col_mapping[col] = 'Frequency (orders)'
        elif col in ['M', 'Monetary']:
            col_mapping[col] = 'Monetary ($)'
        else:
            col_mapping[col] = col

if display_cols:
    display_df = filtered_df[display_cols].copy()
    
    # Format monetary columns
    for col in display_cols:
        if col in ['Monetary', 'M'] and col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
    
    # Rename columns
    display_df = display_df.rename(columns=col_mapping)
    
    # Show top 50 customers
    st.dataframe(
        display_df.head(50),
        width='stretch',
        hide_index=True,
        height=400
    )
    
    # Download button
    st.markdown("### 📥 Export Data")
    create_download_button(
        filtered_df,
        "customer_segments_export.csv",
        "📥 Download Customer Segments Data"
    )
else:
    st.info("No customer data columns available for display.")

st.markdown("---")

# ============================================================================
# ACTIONABLE INSIGHTS
# ============================================================================

st.markdown("### 💡 Actionable Customer Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.markdown(f"""
    <div style="
        background-color: {COLORS['success_container']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_success_fixed_variant']}; margin-top: 0;">🎯 Target for Upselling</h4>
        <p style="font-size: 14px; color: {COLORS['on_success_fixed_variant']}; margin-bottom: 0;">
            <strong>{format_number(premium_customers)}</strong> premium customers identified for 
            VIP programs and exclusive offers. These customers represent your highest value segment.
        </p>
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    st.markdown(f"""
    <div style="
        background-color: {COLORS['error_container']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_error_container']}; margin-top: 0;">⚠️ Retention Priority</h4>
        <p style="font-size: 14px; color: {COLORS['on_error_container']}; margin-bottom: 0;">
            <strong>{format_number(at_risk_customers)}</strong> customers at risk of churning. 
            Immediate action needed: personalized re-engagement campaigns and special incentives.
        </p>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    st.markdown(f"""
    <div style="
        background-color: {COLORS['info_container']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_info_fixed_variant']}; margin-top: 0;">💚 Loyalty Program</h4>
        <p style="font-size: 14px; color: {COLORS['on_info_fixed_variant']}; margin-bottom: 0;">
            <strong>{format_number(loyal_customers)}</strong> loyal customers showing consistent 
            engagement. Reward their loyalty with exclusive benefits and early access to new products.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SEGMENT BREAKDOWN TABLE
# ============================================================================

if 'Segment' in segments_df.columns:
    st.markdown("---")
    st.markdown("### 📊 Segment Summary Statistics")
    
    # Calculate segment statistics
    if value_col:
        segment_stats = segments_df.groupby('Segment').agg({
            'CustomerID': 'count',
            value_col: ['mean', 'sum', 'min', 'max']
        }).reset_index()
        
        segment_stats.columns = ['Segment', 'Customer Count', 'Avg Value', 'Total Value', 'Min Value', 'Max Value']
        
        # Format currency columns
        for col in ['Avg Value', 'Total Value', 'Min Value', 'Max Value']:
            segment_stats[col] = segment_stats[col].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            segment_stats,
            width='stretch',
            hide_index=True
        )
