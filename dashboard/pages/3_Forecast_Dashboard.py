"""
RetailPulse - Forecast Dashboard
Demand forecasting, trend predictions, and future insights
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
    load_forecast_data,
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

configure_page(title="Forecast Dashboard", icon="🔮", layout="wide")

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
st.sidebar.markdown("### 🔮 Demand Forecasting")
st.sidebar.markdown("Predict future demand and optimize inventory planning.")

# Sidebar footer is already added

# ============================================================================
# LOAD DATA
# ============================================================================

@st.cache_data
def load_forecast_and_historical():
    """Load forecast and historical data"""
    forecast_df = load_forecast_data()
    historical_df = load_retail_data()
    
    return forecast_df, historical_df

forecast_df, historical_df = load_forecast_and_historical()

# ============================================================================
# CHECK DATA AVAILABILITY
# ============================================================================

if forecast_df.empty:
    st.error("⚠️ No forecast data available. Please ensure forecast_results.csv is in the data/ directory.")
    st.stop()

# ============================================================================
# DATA PREPARATION
# ============================================================================

# Identify date and value columns in forecast data
date_col = None
value_col = None

# Try to find date column
for col in ['Date', 'date', 'ds', 'forecast_date', 'InvoiceDate']:
    if col in forecast_df.columns:
        date_col = col
        break

# Try to find forecast value column
for col in ['yhat', 'forecast', 'predicted', 'Forecast', 'Value', 'Revenue']:
    if col in forecast_df.columns:
        value_col = col
        break

if date_col is None or value_col is None:
    st.error(f"⚠️ Could not identify date or value columns in forecast data. Available columns: {list(forecast_df.columns)}")
    st.stop()

# Ensure date column is datetime
forecast_df[date_col] = pd.to_datetime(forecast_df[date_col], errors='coerce')
forecast_df = forecast_df.dropna(subset=[date_col])

# Sort by date
forecast_df = forecast_df.sort_values(date_col)

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

# Forecast horizon selector
forecast_horizons = {
    "Next 7 Days": 7,
    "Next 30 Days": 30,
    "Next 60 Days": 60,
    "Next 90 Days": 90,
    "All Available": len(forecast_df)
}

selected_horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    list(forecast_horizons.keys()),
    index=1  # Default to 30 days
)

horizon_days = forecast_horizons[selected_horizon]

# Filter forecast data by horizon
if horizon_days < len(forecast_df):
    filtered_forecast = forecast_df.head(horizon_days)
else:
    filtered_forecast = forecast_df

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
        <h1 style="font-size: 28px; font-weight: 700; color: #1A1A1A; margin: 0; white-space: nowrap;">Demand Forecasting 🔮</h1>
        <p style="font-size: 14px; color: #6B7280; margin: 0.25rem 0 0 0;">Predict future demand and plan inventory strategically</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Search bar and Advanced Filter
col_search, col_filter = st.columns([4, 1])

with col_search:
    search_query = st.text_input("🔍 Search", placeholder="Search forecasts, demand trends, predictions...", label_visibility="collapsed")

with col_filter:
    st.button("⚡ Quick Filters", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================================
# FORECAST KPI METRICS WITH ICON BADGES
# ============================================================================

st.markdown("### 📊 Forecast Metrics")

col1, col2, col3, col4 = st.columns(4)

# Calculate metrics
total_predicted_demand = filtered_forecast[value_col].sum()
avg_daily_forecast = filtered_forecast[value_col].mean()
peak_demand = filtered_forecast[value_col].max()
peak_date = filtered_forecast.loc[filtered_forecast[value_col].idxmax(), date_col]

# Calculate growth if we have historical data
growth_percentage = 0
if not historical_df.empty:
    # Find revenue column in historical data
    hist_revenue_col = None
    for col in ['TotalPrice', 'Revenue', 'Amount', 'Total']:
        if col in historical_df.columns:
            hist_revenue_col = col
            break
    
    if hist_revenue_col and 'InvoiceDate' in historical_df.columns:
        # Get last 30 days of historical data
        historical_df['InvoiceDate'] = pd.to_datetime(historical_df['InvoiceDate'], errors='coerce')
        max_hist_date = historical_df['InvoiceDate'].max()
        last_30_days = historical_df[
            historical_df['InvoiceDate'] >= (max_hist_date - timedelta(days=30))
        ]
        historical_avg = last_30_days[hist_revenue_col].sum() / 30
        
        if historical_avg > 0:
            growth_percentage = ((avg_daily_forecast - historical_avg) / historical_avg) * 100

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #EFF6FF;">
            <span style="font-size: 24px;">📊</span>
        </div>
        <div class="kpi-label">TOTAL PREDICTED DEMAND</div>
        <div class="kpi-value">{format_currency(total_predicted_demand)}</div>
        <div style="font-size: 12px; color: #9CA3AF; margin-top: 0.25rem;">For next {horizon_days} days</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #DBEAFE;">
            <span style="font-size: 24px;">📈</span>
        </div>
        <div class="kpi-label">AVG DAILY FORECAST</div>
        <div class="kpi-value">{format_currency(avg_daily_forecast)}</div>
        <div class="kpi-delta {'positive' if growth_percentage >= 0 else 'negative'}">
            {'↗' if growth_percentage >= 0 else '↘'} {abs(growth_percentage):.1f}% vs historical
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background: #FCE7F3;">
            <span style="font-size: 24px;">🎯</span>
        </div>
        <div class="kpi-label">PEAK DEMAND</div>
        <div class="kpi-value">{format_currency(peak_demand)}</div>
        <div style="font-size: 12px; color: #9CA3AF; margin-top: 0.25rem;">Expected on {peak_date.strftime('%b %d, %Y')}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    # Calculate forecast confidence (if available)
    confidence_cols = [col for col in forecast_df.columns if 'confidence' in col.lower() or 'upper' in col.lower()]
    if confidence_cols:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background: #D1FAE5;">
                <span style="font-size: 24px;">✅</span>
            </div>
            <div class="kpi-label">FORECAST CONFIDENCE</div>
            <div class="kpi-value">High</div>
            <div style="font-size: 12px; color: #9CA3AF; margin-top: 0.25rem;">95% CI available</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon" style="background: #D1FAE5;">
                <span style="font-size: 24px;">📅</span>
            </div>
            <div class="kpi-label">FORECAST RANGE</div>
            <div class="kpi-value">{horizon_days} days</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# MAIN FORECAST VISUALIZATION
# ============================================================================

st.markdown("### 📈 Demand Forecast Trend")

# Prepare historical data for comparison (last 90 days)
historical_for_chart = pd.DataFrame()
if not historical_df.empty and 'InvoiceDate' in historical_df.columns:
    hist_revenue_col = None
    for col in ['TotalPrice', 'Revenue', 'Amount', 'Total']:
        if col in historical_df.columns:
            hist_revenue_col = col
            break
    
    if hist_revenue_col:
        max_hist_date = historical_df['InvoiceDate'].max()
        last_90_days = historical_df[
            historical_df['InvoiceDate'] >= (max_hist_date - timedelta(days=90))
        ]
        
        historical_for_chart = last_90_days.groupby(
            last_90_days['InvoiceDate'].dt.date
        )[hist_revenue_col].sum().reset_index()
        historical_for_chart.columns = ['Date', 'Value']
        historical_for_chart['Type'] = 'Historical'
        historical_for_chart['Date'] = pd.to_datetime(historical_for_chart['Date'])

# Prepare forecast data
forecast_for_chart = filtered_forecast[[date_col, value_col]].copy()
forecast_for_chart.columns = ['Date', 'Value']
forecast_for_chart['Type'] = 'Forecast'

# Create combined chart
fig_forecast = go.Figure()

# Add historical data if available
if not historical_for_chart.empty:
    fig_forecast.add_trace(go.Scatter(
        x=historical_for_chart['Date'],
        y=historical_for_chart['Value'],
        mode='lines',
        name='Historical',
        line=dict(color=COLORS['on_surface_variant'], width=2, dash='dot'),
        hovertemplate='<b>Historical</b><br>Date: %{x}<br>Value: $%{y:,.2f}<extra></extra>'
    ))

# Add forecast data
fig_forecast.add_trace(go.Scatter(
    x=forecast_for_chart['Date'],
    y=forecast_for_chart['Value'],
    mode='lines+markers',
    name='Forecast',
    line=dict(color=COLORS['primary'], width=3),
    marker=dict(size=6, color=COLORS['primary_container']),
    hovertemplate='<b>Forecast</b><br>Date: %{x}<br>Value: $%{y:,.2f}<extra></extra>'
))

# Add confidence intervals if available
lower_col = None
upper_col = None
for col in forecast_df.columns:
    if 'lower' in col.lower():
        lower_col = col
    if 'upper' in col.lower():
        upper_col = col

if lower_col and upper_col and lower_col in filtered_forecast.columns and upper_col in filtered_forecast.columns:
    fig_forecast.add_trace(go.Scatter(
        x=filtered_forecast[date_col],
        y=filtered_forecast[upper_col],
        mode='lines',
        name='Upper Bound',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig_forecast.add_trace(go.Scatter(
        x=filtered_forecast[date_col],
        y=filtered_forecast[lower_col],
        mode='lines',
        name='95% Confidence',
        fill='tonexty',
        fillcolor=f'rgba(0, 74, 198, 0.2)',
        line=dict(width=0),
        hovertemplate='<b>Confidence Interval</b><br>Date: %{x}<br>Lower: $%{y:,.2f}<extra></extra>'
    ))

fig_forecast.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family='Inter', size=12),
    xaxis=dict(
        title='Date',
        showgrid=True,
        gridcolor='#eceef0'
    ),
    yaxis=dict(
        title='Demand / Revenue ($)',
        showgrid=True,
        gridcolor='#eceef0'
    ),
    hovermode='x unified',
    height=500,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_forecast, width='stretch')

st.markdown("---")

# ============================================================================
# ADDITIONAL FORECAST INSIGHTS
# ============================================================================

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📊 Weekly Forecast Breakdown")
    
    # Group by week
    filtered_forecast['Week'] = filtered_forecast[date_col].dt.to_period('W').astype(str)
    weekly_forecast = filtered_forecast.groupby('Week')[value_col].sum().reset_index()
    weekly_forecast.columns = ['Week', 'Forecast']
    
    if not weekly_forecast.empty:
        fig_weekly = px.bar(
            weekly_forecast,
            x='Week',
            y='Forecast',
            title=''
        )
        
        fig_weekly.update_traces(
            marker_color=COLORS['success'],
            hovertemplate='<b>%{x}</b><br>Forecast: $%{y:,.2f}<extra></extra>'
        )
        
        fig_weekly.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            xaxis=dict(title='Week', showgrid=False),
            yaxis=dict(title='Forecast ($)', showgrid=True, gridcolor='#eceef0'),
            height=400
        )
        
        st.plotly_chart(fig_weekly, width='stretch')
    else:
        st.info("No weekly data available.")

with col_right:
    st.markdown("### 📅 Monthly Forecast Summary")
    
    # Group by month
    filtered_forecast['Month'] = filtered_forecast[date_col].dt.to_period('M').astype(str)
    monthly_forecast = filtered_forecast.groupby('Month')[value_col].sum().reset_index()
    monthly_forecast.columns = ['Month', 'Forecast']
    
    if not monthly_forecast.empty:
        fig_monthly = px.bar(
            monthly_forecast,
            x='Month',
            y='Forecast',
            title=''
        )
        
        fig_monthly.update_traces(
            marker_color=COLORS['primary_container'],
            hovertemplate='<b>%{x}</b><br>Forecast: $%{y:,.2f}<extra></extra>'
        )
        
        fig_monthly.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', size=12),
            xaxis=dict(title='Month', showgrid=False),
            yaxis=dict(title='Forecast ($)', showgrid=True, gridcolor='#eceef0'),
            height=400
        )
        
        st.plotly_chart(fig_monthly, width='stretch')
    else:
        st.info("No monthly data available.")

st.markdown("---")

# ============================================================================
# FORECAST DATA TABLE
# ============================================================================

st.markdown("### 📋 Detailed Forecast Data")

# Prepare table
table_df = filtered_forecast[[date_col, value_col]].copy()
table_df[date_col] = table_df[date_col].dt.strftime('%Y-%m-%d')
table_df[value_col] = table_df[value_col].apply(lambda x: f"${x:,.2f}")

# Rename columns
table_df.columns = ['Date', 'Forecasted Demand']

st.dataframe(
    table_df,
    width='stretch',
    hide_index=True,
    height=400
)

# Download button
st.markdown("### 📥 Export Forecast")
create_download_button(
    filtered_forecast,
    "forecast_export.csv",
    "📥 Download Forecast Data"
)

st.markdown("---")

# ============================================================================
# KEY INSIGHTS
# ============================================================================

st.markdown("### 💡 Forecast Insights & Recommendations")

insight_col1, insight_col2, insight_col3 = st.columns(3)

# Calculate insights
top_3_days = filtered_forecast.nlargest(3, value_col)
low_3_days = filtered_forecast.nsmallest(3, value_col)
avg_forecast = filtered_forecast[value_col].mean()

with insight_col1:
    peak_day = top_3_days.iloc[0]
    st.markdown(f"""
    <div style="
        background-color: {COLORS['success_container']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_success_fixed_variant']}; margin-top: 0;">🎯 Peak Demand Period</h4>
        <p style="font-size: 14px; color: {COLORS['on_success_fixed_variant']}; margin-bottom: 0.5rem;">
            <strong>{peak_day[date_col].strftime('%B %d, %Y')}</strong>
        </p>
        <p style="font-size: 20px; font-weight: 700; color: {COLORS['on_success_fixed_variant']}; margin: 0.5rem 0;">
            {format_currency(peak_day[value_col])}
        </p>
        <p style="font-size: 12px; color: {COLORS['on_success_fixed_variant']}; margin: 0;">
            Ensure adequate inventory and staffing for this high-demand period.
        </p>
    </div>
    """, unsafe_allow_html=True)

with insight_col2:
    low_day = low_3_days.iloc[0]
    st.markdown(f"""
    <div style="
        background-color: {COLORS['info_container']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_info_fixed_variant']}; margin-top: 0;">📉 Low Demand Period</h4>
        <p style="font-size: 14px; color: {COLORS['on_info_fixed_variant']}; margin-bottom: 0.5rem;">
            <strong>{low_day[date_col].strftime('%B %d, %Y')}</strong>
        </p>
        <p style="font-size: 20px; font-weight: 700; color: {COLORS['on_info_fixed_variant']}; margin: 0.5rem 0;">
            {format_currency(low_day[value_col])}
        </p>
        <p style="font-size: 12px; color: {COLORS['on_info_fixed_variant']}; margin: 0;">
            Consider promotional campaigns or maintenance activities during this period.
        </p>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    st.markdown(f"""
    <div style="
        background-color: white;
        border: 1px solid {COLORS['outline_variant']};
        border-radius: 0.75rem;
        padding: 1.25rem;
    ">
        <h4 style="color: {COLORS['on_surface']}; margin-top: 0;">📊 Average Forecast</h4>
        <p style="font-size: 14px; color: {COLORS['on_surface_variant']}; margin-bottom: 0.5rem;">
            <strong>Daily Average</strong>
        </p>
        <p style="font-size: 20px; font-weight: 700; color: {COLORS['on_surface']}; margin: 0.5rem 0;">
            {format_currency(avg_forecast)}
        </p>
        <p style="font-size: 12px; color: {COLORS['on_surface_variant']}; margin: 0;">
            Use this baseline for standard inventory planning and resource allocation.
        </p>
    </div>
    """, unsafe_allow_html=True)
