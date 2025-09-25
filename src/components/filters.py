"""
Data filtering component
"""
import streamlit as st
from datetime import datetime
import pandas as pd

def render_filters(df):
    """Render filter options and return filtered dataframe."""
    # Apply custom CSS for extremely small sidebar font size
    st.sidebar.markdown("""
    <style>
        .sidebar .sidebar-content {
            font-size: 0.65rem !important;
        }
        .sidebar .stSlider label {
            font-size: 0.65rem !important;
        }
        .sidebar .stSlider div[data-baseweb="slider"] {
            font-size: 0.65rem !important;
        }
        .sidebar .stMultiSelect label {
            font-size: 0.65rem !important;
        }
        .sidebar .stMultiSelect span[data-baseweb="tag"] {
            font-size: 0.65rem !important;
        }
        .sidebar .stDateInput label {
            font-size: 0.65rem !important;
        }
        .sidebar .stSubheader {
            font-size: 0.8rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a copy of the dataframe
    filtered_df = df.copy()
    
    # Date range filters for datetime columns
    datetime_columns = df.select_dtypes(include=['datetime64']).columns
    for col in datetime_columns:
        st.sidebar.subheader(f"{col} Range")
        min_date = df[col].min()
        max_date = df[col].max()
        date_range = st.sidebar.date_input(
            f"Select {col} range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
        # Check if date_range has both start and end dates before filtering
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (filtered_df[col].dt.date >= date_range[0]) & 
                (filtered_df[col].dt.date <= date_range[1])
            ]
    
    # Numeric range filters
    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
    for col in numeric_columns:
        st.sidebar.subheader(f"{col} Range")
        min_val = float(df[col].min())
        max_val = float(df[col].max())
        range_val = st.sidebar.slider(
            f"Select {col} range",
            min_val, max_val,
            (min_val, max_val)
        )
        filtered_df = filtered_df[
            (filtered_df[col] >= range_val[0]) & 
            (filtered_df[col] <= range_val[1])
        ]
    
    # Categorical filters
    categorical_columns = df.select_dtypes(include=['object']).columns
    for col in categorical_columns:
        unique_values = df[col].unique()
        if len(unique_values) < 50:  # Only show filter for columns with reasonable number of unique values
            st.sidebar.subheader(f"{col} Selection")
            selected_values = st.sidebar.multiselect(
                f"Select {col} values",
                options=unique_values,
                default=unique_values
            )
            filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
    
    # Display filter summary
    with st.sidebar:
        st.markdown("---")
        st.subheader("Filter Summary")
        
        # Use custom HTML formatting with a larger font size to match other content
        summary_html = f"""
        <div style="font-size: 0.85rem; margin-bottom: 3px;">
            <b>Original rows:</b> {len(df)}
        </div>
        <div style="font-size: 0.85rem; margin-bottom: 3px;">
            <b>Filtered rows:</b> {len(filtered_df)}
        </div>
        <div style="font-size: 0.85rem; margin-bottom: 3px;">
            <b>Rows removed:</b> {len(df) - len(filtered_df)}
        </div>
        """
        st.markdown(summary_html, unsafe_allow_html=True)
    
    return filtered_df