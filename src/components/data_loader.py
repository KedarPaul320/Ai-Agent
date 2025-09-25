"""
Data loading component with basic cleaning techniques
"""
import streamlit as st
import pandas as pd

@st.cache_data
def load_file(uploaded_file):
    """Load and cache data from uploaded CSV file with basic cleaning."""
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Convert date columns to datetime
        for col in df.columns:
            if 'date' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass  # If conversion fails, keep original format
        
        # Clean the data using basic techniques
        df = clean_data(df)
        
        return df
    except Exception as e:
        # Add custom styling for the error message
        st.markdown("""
        <style>
            .stAlert .st-alert {
                font-size: 1.3rem !important;
                padding: 20px !important;
            }
        </style>
        """, unsafe_allow_html=True)
        st.error(f"Error loading data: {str(e)}")
        return None

def clean_data(df):
    """Apply basic data cleaning techniques."""
    # Make a copy to avoid modifying the original
    df_cleaned = df.copy()
    
    # Separate numeric and non-numeric columns
    numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
    categorical_cols = df_cleaned.select_dtypes(exclude=['number', 'datetime']).columns
    
    # Handle missing values
    df_cleaned = handle_missing_values(df_cleaned, numeric_cols, categorical_cols)
    
    # Handle outliers
    df_cleaned = handle_outliers(df_cleaned, numeric_cols)
    
    return df_cleaned

def handle_missing_values(df, numeric_cols, categorical_cols):
    """Handle missing values using median and mode imputation."""
    # For numeric columns: use median (more robust to outliers)
    for col in numeric_cols:
        if df[col].isna().any():
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
    
    # For categorical columns: use mode (most frequent value)
    for col in categorical_cols:
        if df[col].isna().any():
            mode_vals = df[col].mode()
            mode_val = mode_vals[0] if not mode_vals.empty else "Unknown"
            # Use loc to avoid the FutureWarning about downcasting
            missing_mask = df[col].isna()
            df.loc[missing_mask, col] = mode_val
    
    return df

def handle_outliers(df, numeric_cols):
    """Handle outliers using Winsorization."""
    for col in numeric_cols:
        # Skip date-related numeric columns
        if 'date' in col.lower() or 'time' in col.lower() or 'year' in col.lower():
            continue
            
        try:
            # Basic outlier handling - Winsorization at 1% and 99%
            q1 = df[col].quantile(0.01)
            q3 = df[col].quantile(0.99)
            df[col] = df[col].clip(q1, q3)
        except Exception:
            # If outlier handling fails, continue to next column
            continue
    
    return df