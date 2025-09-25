import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
from src.components.data_loader import load_file
from src.components.chart_creator import render_chart_options, create_chart
from src.components.filters import render_filters

def main():
    st.set_page_config(page_title="Data Storyteller", page_icon="", layout="wide")
    
    # Apply custom CSS with reduced font size throughout the app
    st.markdown("""
    <style>
        html, body, [class*="st-"] {
            font-size: 1rem !important;
        }
        .stMarkdown p, .stMarkdown li {
            font-size: 1rem !important;
        }
        h1 {
            font-size: 2.1rem !important;
        }
        h2 {
            font-size: 1.7rem !important;
        }
        h3 {
            font-size: 1.5rem !important;
        }
        h4 {
            font-size: 1.3rem !important;
        }
        .stButton button {
            font-size: 1rem !important;
        }
        .stSelectbox div [data-baseweb="select"] {
            font-size: 1rem !important;
        }
        div[data-testid="stDataFrameResizable"] table {
            font-size: 1rem !important;
        }
        .stDataFrame div [data-testid="stTable"] {
            font-size: 1rem !important;
        }
        .stCheckbox label {
            font-size: 1rem !important;
        }
        /* Sidebar specific styling with ultra-small font */
        .sidebar .sidebar-content {
            font-size: 0.65rem !important;
        }
        /* Make sidebar initially narrow but still resizable */
        [data-testid="stSidebar"] {
            width: 14rem;
            min-width: 14rem;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 0.8rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        section[data-testid="stSidebar"] h1 {
            font-size: 0.95rem !important;
        }
        section[data-testid="stSidebar"] h2 {
            font-size: 0.8rem !important;
        }
        /* Compress sidebar spacing further */
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
            margin-bottom: 0.3rem !important;
            padding-bottom: 0.2rem !important;
        }
        /* Make sidebar label-input pairs ultra-compact */
        section[data-testid="stSidebar"] .stSelectbox, 
        section[data-testid="stSidebar"] .stMultiSelect, 
        section[data-testid="stSidebar"] .stSlider,
        section[data-testid="stSidebar"] .stDateInput {
            margin-bottom: 0.5rem !important;
        }
        /* Reduce padding in sidebar widgets */
        section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
            height: 1.8rem !important;
            min-height: 1.8rem !important;
        }
        section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
            min-height: 1.8rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Title and Description
    st.title("Interactive Data Visualization")
    st.markdown("""
    <p style="font-size: 1.15rem; margin-bottom: 15px;">
        Create custom visualizations from your data. Upload a CSV file, select columns, and create various types of charts.
    </p>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    st.header("Upload Data")
    
    # Add styling for the file uploader label
    st.markdown("""
    <style>
        .stFileUploader label {
            font-size: 1rem !important;
        }
        /* Style the file uploader button */
        .stFileUploader button {
            font-size: 1rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = load_file(uploaded_file)
        if df is not None:
            # Filter Section
            st.sidebar.header("Data Filters")
            filtered_df = render_filters(df)
            
            # Visualization Section
            st.header("Create Visualization")
            render_chart_options(filtered_df)
            
            # Data View Section
            st.header("Data Management")
            
            # Create two columns for data controls
            data_col1, data_col2 = st.columns([1, 1])
            
            # Show raw data option in the first column
            with data_col1:
                show_data = st.checkbox("Show Raw Data")
            
            # Download button in the second column
            with data_col2:
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download Filtered Data",
                    data=csv,
                    file_name="filtered_data.csv",
                    mime="text/csv"
                )
            
            # Use full width for data display when shown
            if show_data:
                # Custom styling for the dataframe with smaller font size and increased height
                st.markdown("""
                <style>
                    .dataframe {
                        font-size: 0.95rem !important;
                    }
                    .dataframe th {
                        font-size: 1.05rem !important;
                        font-weight: bold !important;
                    }
                    .dataframe td {
                        font-size: 0.95rem !important;
                    }
                    /* Make dataframe container taller */
                    [data-testid="stDataFrame"] > div {
                        max-height: 650px !important;
                    }
                    div[data-testid="stDataFrameResizable"] {
                        min-height: 650px !important;
                        height: 650px !important;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                # Display dataframe with more rows visible - using full available width
                st.dataframe(filtered_df, height=650, width='stretch')
    else:
        # Style the info message
        st.markdown("""
        <style>
            .stAlert .st-alert {
                font-size: 1.3rem !important;
                padding: 20px !important;
            }
        </style>
        """, unsafe_allow_html=True)
        st.info("Please upload a CSV file to get started!")

if __name__ == "__main__":
    main()
