"""
RetailPulse Utility Functions
Helper functions for data loading, CSS injection, and common operations
"""

import streamlit as st
import pandas as pd
import os
from pathlib import Path

# ============================================================================
# PATH HELPERS
# ============================================================================

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent

def get_data_path(filename):
    """Get full path to a data file"""
    return get_project_root() / "data" / filename

def get_asset_path(filename):
    """Get full path to an asset file"""
    return get_project_root() / "dashboard" / "assets" / filename

# ============================================================================
# CSS INJECTION
# ============================================================================

def load_css():
    """Load and inject custom CSS into Streamlit app"""
    css_file = get_asset_path("custom.css")
    
    if css_file.exists():
        with open(css_file, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Try alternative path
        alt_css_path = Path(__file__).parent / "assets" / "custom.css"
        if alt_css_path.exists():
            with open(alt_css_path, encoding='utf-8') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Custom CSS file not found. Using default Streamlit styling.")

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

@st.cache_data
def load_retail_data():
    """
    Load the main cleaned retail dataset
    
    Returns:
        pd.DataFrame: Cleaned retail data
    """
    try:
        df = pd.read_csv(get_data_path("cleaned_retail.csv"))
        
        # Convert date columns with flexible parsing
        if 'InvoiceDate' in df.columns:
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='mixed', errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error("❌ cleaned_retail.csv not found in data/ directory")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading retail data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_customer_segments():
    """
    Load customer segmentation data
    
    Returns:
        pd.DataFrame: Customer segments data
    """
    try:
        df = pd.read_csv(get_data_path("customer_segments.csv"))
        return df
    except FileNotFoundError:
        st.error("❌ customer_segments.csv not found in data/ directory")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading customer segments: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_forecast_data():
    """
    Load demand forecast data
    
    Returns:
        pd.DataFrame: Forecast data
    """
    try:
        df = pd.read_csv(get_data_path("forecast_results.csv"))
        
        # Convert date columns if present
        date_columns = ['Date', 'date', 'ds', 'forecast_date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
                break
        
        return df
    except FileNotFoundError:
        st.error("❌ forecast_results.csv not found in data/ directory")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading forecast data: {str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_inventory_data():
    """
    Load inventory recommendations data
    
    Returns:
        pd.DataFrame: Inventory data
    """
    try:
        df = pd.read_csv(get_data_path("inventory_recommendations.csv"))
        return df
    except FileNotFoundError:
        st.error("❌ inventory_recommendations.csv not found in data/ directory")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading inventory data: {str(e)}")
        return pd.DataFrame()

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

def configure_page(title, icon="📊", layout="wide"):
    """
    Configure Streamlit page settings
    
    Args:
        title (str): Page title
        icon (str): Page icon
        layout (str): Page layout ("wide" or "centered")
    """
    st.set_page_config(
        page_title=f"RetailPulse | {title}",
        page_icon=icon,
        layout=layout,
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_css()

# ============================================================================
# DATA FORMATTING HELPERS
# ============================================================================

def format_currency(value):
    """Format number as currency"""
    if pd.isna(value):
        return "N/A"
    return f"${value:,.2f}"

def format_number(value, decimals=0):
    """Format number with thousands separator"""
    if pd.isna(value):
        return "N/A"
    if decimals == 0:
        return f"{int(value):,}"
    return f"{value:,.{decimals}f}"

def format_percentage(value, decimals=1):
    """Format number as percentage"""
    if pd.isna(value):
        return "N/A"
    return f"{value:.{decimals}f}%"

def calculate_percentage_change(current, previous):
    """Calculate percentage change between two values"""
    if previous == 0 or pd.isna(previous) or pd.isna(current):
        return 0
    return ((current - previous) / previous) * 100

# ============================================================================
# DATE HELPERS
# ============================================================================

def get_date_range_filter():
    """
    Create a date range filter in sidebar
    
    Returns:
        tuple: (start_date, end_date)
    """
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date")
    
    with col2:
        end_date = st.date_input("End Date")
    
    return start_date, end_date

# ============================================================================
# SIDEBAR HELPERS
# ============================================================================

def add_sidebar_logo():
    """Add RetailPulse logo to sidebar"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <div style="
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #004ac6 0%, #2563eb 100%);
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 0.5rem;
        ">
            <span style="color: white; font-size: 24px;">📊</span>
        </div>
        <h2 style="
            font-family: 'Hanken Grotesk', sans-serif;
            font-weight: 700;
            font-size: 20px;
            color: #004ac6;
            margin: 0;
        ">RetailPulse</h2>
        <p style="
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #434655;
            margin: 0;
        ">Analytics Suite</p>
    </div>
    """, unsafe_allow_html=True)

def add_sidebar_footer():
    """Add footer to sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 11px; color: #434655; padding: 1rem 0;">
        <p>© 2026 RetailPulse</p>
        <p>Data Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# EXPORT HELPERS
# ============================================================================

def create_download_button(df, filename, label="📥 Download CSV"):
    """
    Create a download button for DataFrame
    
    Args:
        df (pd.DataFrame): DataFrame to download
        filename (str): Output filename
        label (str): Button label
    """
    csv = df.to_csv(index=False)
    st.download_button(
        label=label,
        data=csv,
        file_name=filename,
        mime="text/csv"
    )

# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_dataframe(df, required_columns):
    """
    Validate that DataFrame has required columns
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        required_columns (list): List of required column names
    
    Returns:
        bool: True if valid, False otherwise
    """
    if df.empty:
        st.error("❌ DataFrame is empty")
        return False
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
        return False
    
    return True
