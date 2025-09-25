"""
Chart creation component
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ..utils.chart_insights import generate_chart_summary, generate_data_statistics

CHART_TYPES = {
    "Bar Chart": "bar",
    "Line Chart": "line",
    "Scatter Plot": "scatter",
    "Box Plot": "box",
    "Violin Plot": "violin",
    "Histogram": "histogram",
    "Pie Chart": "pie",
    "Area Chart": "area",
    "Heat Map": "heatmap",
    "Bubble Chart": "bubble",
}

def create_chart(df, chart_type, x_column, y_column=None, size_column=None):
    """Create a chart based on user selections."""
    try:
        if chart_type == "bar":
            if y_column:
                fig = px.bar(df, x=x_column, y=y_column)
            else:
                fig = px.bar(df, x=x_column)
                
        elif chart_type == "line":
            fig = px.line(df, x=x_column, y=y_column)
            
        elif chart_type == "scatter":
            fig = px.scatter(df, x=x_column, y=y_column, size=size_column)
            
        elif chart_type == "box":
            fig = px.box(df, x=x_column, y=y_column)
            
        elif chart_type == "violin":
            fig = px.violin(df, x=x_column, y=y_column)
            
        elif chart_type == "histogram":
            fig = px.histogram(df, x=x_column)
            
        elif chart_type == "pie":
            fig = px.pie(df, names=x_column, values=y_column)
            
        elif chart_type == "area":
            fig = px.area(df, x=x_column, y=y_column)
            
        elif chart_type == "heatmap":
            pivot_table = df.pivot_table(values=y_column, index=x_column, aggfunc='mean')
            fig = px.imshow(pivot_table, aspect='auto')
            
        elif chart_type == "bubble":
            fig = px.scatter(df, x=x_column, y=y_column, size=size_column)
            
        else:
            st.error(f"Unsupported chart type: {chart_type}")
            return None

        # Update layout for better visualization with much larger chart height
        fig.update_layout(
            title_x=0.5,
            margin=dict(l=20, r=20, t=40, b=20),
            height=800,  # Increased height from 650 to 800
            template="simple_white",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(
                size=20,  # Increase font size for all text in the chart
                family="Arial, sans-serif"
            )
        )
        
        # Update axes for better appearance with larger fonts
        fig.update_xaxes(
            showline=True,
            linewidth=1,
            linecolor='#e2e8f0',
            gridcolor='#f1f5f9',
            title_font=dict(size=22),  # Even larger axis title
            tickfont=dict(size=16)     # Larger tick labels
        )
        fig.update_yaxes(
            showline=True,
            linewidth=1,
            linecolor='#e2e8f0',
            gridcolor='#f1f5f9',
            title_font=dict(size=22),  # Even larger axis title
            tickfont=dict(size=16)     # Larger tick labels
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        return None

def render_chart_options(df):
    """Render chart options and create visualization."""
    # Get column types
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    all_cols = df.columns.tolist()

    # Chart Configuration
    with st.container():
        st.subheader("Select Chart Type")
        
        # Add custom CSS for selectbox
        st.markdown("""
        <style>
            .stSelectbox > div > div > div > div {
                font-size: 1.2rem !important;
            }
            .stSelectbox > div > div[data-baseweb="select"] > div {
                font-size: 1.2rem !important;
            }
            .stSelectbox label {
                font-size: 1.2rem !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        chart_type = st.selectbox(
            "Chart Type",
            list(CHART_TYPES.keys())
        )

    # Axis selections
    st.subheader("Configure Axes")
    
    # Apply styling for subheader and column labels
    st.markdown("""
    <style>
        /* Style for axis labels */
        .stColumns label {
            font-size: 1.2rem !important;
            font-weight: 500 !important;
        }
        /* Style for expander text */
        .stExpander p {
            font-size: 1.2rem !important;
        }
        /* Style for detailed statistics */
        .stExpander div[data-testid="stExpander"] {
            font-size: 1.2rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if chart_type in ["line", "area"]:
            suggested_x = datetime_cols[0] if datetime_cols else all_cols[0]
        else:
            suggested_x = all_cols[0]
        x_col = st.selectbox(
            "X-axis",
            all_cols,
            index=all_cols.index(suggested_x)
        )

    with col2:
        if chart_type != "histogram":
            if chart_type in ["scatter", "bubble", "box", "violin"]:
                y_options = numeric_cols
                suggested_y = numeric_cols[0] if numeric_cols else None
                y_col = st.selectbox(
                    "Select Y-axis",
                    y_options,
                    index=0 if suggested_y else 0
                )
            else:
                y_options = all_cols
                suggested_y = numeric_cols[0] if numeric_cols else all_cols[0]
                y_col = st.selectbox(
                    "Select Y-axis",
                    y_options,
                    index=all_cols.index(suggested_y)
                )
        else:
            y_col = None

    # Additional options for specific chart types
    if chart_type in ["bubble", "scatter"]:
        size_col = st.selectbox(
            "Size Variable (Optional)",
            ["None"] + numeric_cols
        )
        if size_col == "None":
            size_col = None
    else:
        size_col = None

    # Create and display visualization
    fig = create_chart(df, CHART_TYPES[chart_type], x_col, y_col, size_col)
    if fig:
        # Add CSS for chart container to make it even more prominent
        st.markdown("""
        <style>
            /* Make chart container much more prominent */
            .main .block-container [data-testid="stVerticalBlock"] > div:has([data-testid="stPlotlyChart"]) {
                margin-left: -40px;
                margin-right: -40px;
                width: calc(100% + 80px);
                margin-top: 10px;
                margin-bottom: 20px;
            }
            /* Add subtle shadow to chart for emphasis */
            [data-testid="stPlotlyChart"] > div {
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                border-radius: 8px;
                padding: 10px;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # IMPORTANT: Use a standard dictionary for config to avoid any keyword arguments
        # This should be compatible with both old and new Streamlit APIs
        plotly_config = {"displayModeBar": False}  # Simplified config
        
        # Use only the figure and config parameter - this is standard across Streamlit versions
        st.plotly_chart(fig, config=plotly_config)

        # Chart insights
        st.subheader("Key Insights")
        
        # Add styling with reduced font size for insights (but not for the chart itself)
        st.markdown("""
        <style>
            /* Style for lists in chart insights */
            .chart-insights ul li {
                font-size: 1.05rem !important;
                margin-bottom: 6px;
            }
            /* Style for expander label */
            .stExpander button p {
                font-size: 1rem !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Chart-specific summary
        chart_summary = generate_chart_summary(df, CHART_TYPES[chart_type], x_col, y_col)
        
        # Add class without container styling
        styled_summary = f"""
        <div class="chart-insights">
            {chart_summary}
        </div>
        """
        st.markdown(styled_summary, unsafe_allow_html=True)
        
        # Detailed statistics (expandable) - don't modify the statistics itself as it uses the same styling from chart_insights.py
        with st.expander("View Detailed Statistics"):
            stats_summary = generate_data_statistics(df)
            # Add wrapper with smaller font size
            st.markdown(f"""
            <div style="font-size: 0.95rem;">
                {stats_summary}
            </div>
            """, unsafe_allow_html=True)

