"""
Chart insights generator for providing natural language summaries of visualizations.
"""
import pandas as pd
import numpy as np

def generate_data_statistics(df):
    """
    Generate a clean, readable summary of the DataFrame's statistics.
    
    Args:
        df (pd.DataFrame): Input DataFrame to analyze
        
    Returns:
        str: Formatted string containing key statistics about the data
    """
    # Get summary statistics
    stats = df.describe()
    
    # Initialize the summary string
    summary = "## 📊 Dataset Statistical Summary\n\n"
    
    # Add basic DataFrame info with HTML formatting (reduced font size)
    summary += f"<div style='font-size: 0.95rem; margin-bottom: 15px;'>\n"
    summary += f"<h3 style='font-size: 1.3rem;'>Dataset Overview:</h3>\n"
    summary += f"<ul>\n"
    summary += f"  <li><b>Records:</b> {len(df):,} rows</li>\n"
    summary += f"  <li><b>Fields:</b> {len(df.columns):,} columns</li>\n"
    
    # Add missing value information
    missing = df.isnull().sum()
    if missing.any():
        missing_cols = missing[missing > 0]
        summary += f"  <li><b>Fields with Missing Values:</b> {len(missing_cols):,} columns</li>\n"
        summary += f"  <li><b>Total Missing Values:</b> {missing.sum():,} entries</li>\n"
    else:
        summary += f"  <li><b>Missing Values:</b> None detected</li>\n"
    
    summary += f"</ul>\n"
    summary += f"</div>\n"
    
    # For each numeric column with HTML formatting (smaller font)
    summary += "<h3 style='font-size: 1.3rem;'>📈 Numerical Variables</h3>\n\n"
    
    for column in stats.columns:
        summary += f"<h4 style='font-size: 1.1rem; margin-top: 15px;'>{column}</h4>\n"
        summary += f"<ul style='font-size: 0.95rem;'>\n"
        summary += f"  <li><b>Central Tendency:</b> Mean = {stats[column]['mean']:.2f}, Median = {stats[column]['50%']:.2f}</li>\n"
        summary += f"  <li><b>Variability:</b> Std Dev = {stats[column]['std']:.2f}, Range = {stats[column]['max'] - stats[column]['min']:.2f}</li>\n"
        summary += f"  <li><b>Range:</b> Min = {stats[column]['min']:.2f}, Max = {stats[column]['max']:.2f}</li>\n"
        summary += f"  <li><b>Quartiles:</b> Q1 = {stats[column]['25%']:.2f}, Q3 = {stats[column]['75%']:.2f}</li>\n"
        summary += f"</ul>\n"
    
    # If there are missing values, add details with HTML formatting (smaller font)
    if missing.any():
        summary += "<h3 style='font-size: 1.3rem;'>⚠️ Missing Value Details</h3>\n\n"
        summary += "<ul style='font-size: 0.95rem;'>\n"
        for col, count in missing[missing > 0].items():
            percent = (count / len(df)) * 100
            summary += f"  <li><b>{col}:</b> {count:,} missing values ({percent:.1f}%)</li>\n"
        summary += "</ul>\n"
    
    return summary

def generate_chart_summary(df, chart_type, x_column, y_column=None, color_column=None):
    """Generate natural language summary of the chart."""
    try:
        if chart_type == "bar":
            return generate_bar_summary(df, x_column, y_column)
        elif chart_type == "line":
            return generate_line_summary(df, x_column, y_column)
        elif chart_type == "scatter":
            return generate_scatter_summary(df, x_column, y_column)
        elif chart_type == "histogram":
            return generate_histogram_summary(df, x_column)
        elif chart_type == "pie":
            return generate_pie_summary(df, x_column, y_column)
        elif chart_type == "box":
            return generate_box_summary(df, x_column, y_column)
        elif chart_type == "area":
            # Area charts are similar to line charts
            return generate_line_summary(df, x_column, y_column).replace("Line Chart", "Area Chart").replace("📈", "📊")
        elif chart_type == "violin":
            # Similar to box plot but with density
            base_summary = generate_box_summary(df, x_column, y_column)
            return base_summary.replace("Box Plot", "Violin Plot").replace("📦", "🎻") + "\n\n*Note: The violin shape shows the probability density of the data at different values.*"
        elif chart_type == "heatmap":
            return f"""### 🔥 Heatmap Pattern Analysis

This visualization shows the relationship intensity between {x_column} and {y_column}.

**What to Look For:**
<ul>
  <li><b>Dark Areas:</b> Represent higher values or stronger relationships</li>
  <li><b>Light Areas:</b> Represent lower values or weaker relationships</li>
  <li><b>Patterns:</b> Look for clusters, gradients, or symmetry that might indicate underlying structure</li>
  <li><b>Outliers:</b> Isolated cells with notably different colors from their neighbors</li>
</ul>

<p><em>Tip: Heatmaps are excellent for spotting patterns that might not be obvious in other chart types.</em></p>"""
        elif chart_type == "bubble":
            base_summary = generate_scatter_summary(df, x_column, y_column)
            return base_summary.replace("Scatter Plot", "Bubble Plot").replace("🔍", "⭕") + "\n\n*Note: The size of each bubble represents a third dimension in your data.*"
        else:
            return f"""### 📊 Chart Analysis: {chart_type.title()}

This visualization compares {x_column} and {y_column if y_column else 'frequency'}.

**Quick Data Overview:**
<ul>
  <li><b>Data Points:</b> {len(df)}</li>
  <li><b>Variables:</b> {x_column}{f" and {y_column}" if y_column else ""}</li>
  <li><b>Chart Type:</b> {chart_type.title()}</li>
</ul>

<p><em>Note: Explore the detailed statistics section below for more insights.</em></p>"""
    except Exception as e:
        return f"""### ⚠️ Chart Analysis

The system encountered a challenge generating detailed insights for this visualization.

**Possible reasons:**
<ul>
  <li><b>Complex data relationships</b></li>
  <li><b>Missing values in key fields</b></li>
  <li><b>Unexpected data structure</b></li>
</ul>

<p>You can still examine the chart visually and check the detailed statistics tab for more information.</p>"""

def generate_bar_summary(df, x_column, y_column):
    """Generate summary for bar charts."""
    try:
        max_val = df[y_column].max()
        max_category = df.loc[df[y_column] == max_val, x_column].iloc[0]
        min_val = df[y_column].min()
        min_category = df.loc[df[y_column] == min_val, x_column].iloc[0]
        avg_val = df[y_column].mean()
        
        summary = f"""### 📊 Bar Chart Analysis: {y_column} by {x_column}

This visualization shows how {y_column} varies across different {x_column} categories.

**Key Findings:**
<ul>
  <li><b>Highest Value:</b> {max_category} stands out with {max_val:,.2f}</li>
  <li><b>Lowest Value:</b> {min_category} shows {min_val:,.2f}</li>
  <li><b>Average Value:</b> {avg_val:,.2f} across all {len(df)} categories</li>
  <li><b>Range:</b> The difference between highest and lowest is {max_val - min_val:,.2f}</li>
</ul>

<p><em>Tip: Look for patterns in how the bars are distributed - are they evenly spread or clustered?</em></p>"""

        return summary
    except Exception:
        return f"This bar chart compares {x_column} and {y_column}."

def generate_line_summary(df, x_column, y_column):
    """Generate summary for line charts."""
    try:
        first_val = df[y_column].iloc[0]
        last_val = df[y_column].iloc[-1]
        change = ((last_val - first_val) / first_val) * 100
        max_val = df[y_column].max()
        max_date = df.loc[df[y_column] == max_val, x_column].iloc[0]
        min_val = df[y_column].min()
        min_date = df.loc[df[y_column] == min_val, x_column].iloc[0]
        
        trend = "upward" if change > 5 else "downward" if change < -5 else "relatively stable"
        
        summary = f"""### 📈 Line Chart Trend Analysis: {y_column} over Time

This visualization tracks how {y_column} has changed from {df[x_column].min()} to {df[x_column].max()}.

**Key Insights:**
<ul>
  <li><b>Overall Trend:</b> {y_column} shows a {trend} trend ({change:+.1f}%)</li>
  <li><b>Starting Value:</b> {first_val:,.2f}</li>
  <li><b>Ending Value:</b> {last_val:,.2f}</li>
  <li><b>Peak:</b> {max_val:,.2f} on {max_date}</li>
  <li><b>Lowest Point:</b> {min_val:,.2f} on {min_date}</li>
</ul>

<p><em>Tip: Look for patterns like seasonality, sudden spikes or drops, and long-term trends.</em></p>"""

        return summary
    except Exception:
        return f"This line chart shows {y_column} over {x_column}."

def generate_scatter_summary(df, x_column, y_column):
    """Generate summary for scatter plots."""
    try:
        correlation = df[x_column].corr(df[y_column])
        relationship = "weak" if abs(correlation) < 0.3 else "moderate" if abs(correlation) < 0.7 else "strong"
        direction = "positive" if correlation > 0 else "negative"
        
        interpretation = ""
        if abs(correlation) > 0.7:
            interpretation = f"As {x_column} increases, {y_column} tends to {'increase' if correlation > 0 else 'decrease'} substantially."
        elif abs(correlation) > 0.3:
            interpretation = f"As {x_column} increases, {y_column} tends to {'increase' if correlation > 0 else 'decrease'} somewhat."
        else:
            interpretation = f"There doesn't appear to be a clear pattern between {x_column} and {y_column}."
            
        summary = f"""### 🔍 Scatter Plot Relationship Analysis

This visualization explores the relationship between {x_column} and {y_column} across {len(df)} data points.

**What the Data Shows:**
<ul>
  <li><b>Correlation Strength:</b> {relationship.capitalize()} ({correlation:.2f})</li>
  <li><b>Direction:</b> {direction.capitalize()} relationship</li>
  <li><b>Interpretation:</b> {interpretation}</li>
</ul>

<p><em>Tip: Look for clusters, outliers, and whether points follow a pattern or are randomly scattered.</em></p>"""

        return summary
    except Exception:
        return f"This scatter plot compares {x_column} and {y_column}."

def generate_histogram_summary(df, x_column):
    """Generate summary for histograms."""
    try:
        mean = df[x_column].mean()
        median = df[x_column].median()
        std_dev = df[x_column].std()
        
        # Check for skewness
        skewness = df[x_column].skew()
        if skewness > 0.5:
            distribution = "right-skewed (higher values are spread out)"
        elif skewness < -0.5:
            distribution = "left-skewed (lower values are spread out)"
        else:
            distribution = "approximately normally distributed"
        
        summary = f"""### 📊 Histogram Distribution Analysis: {x_column}

This visualization shows how {x_column} values are distributed across your dataset.

**Distribution Insights:**
<ul>
  <li><b>Central Tendency:</b> Average = {mean:,.2f}, Median = {median:,.2f}</li>
  <li><b>Spread:</b> Standard deviation = {std_dev:,.2f}</li>
  <li><b>Range:</b> From {df[x_column].min():,.2f} to {df[x_column].max():,.2f}</li>
  <li><b>Shape:</b> The distribution appears to be {distribution}</li>
</ul>

<p><em>Tip: Compare the mean and median values - a large difference often indicates skewed data with outliers.</em></p>"""

        return summary
    except Exception:
        return f"This histogram shows the distribution of {x_column}."

def generate_pie_summary(df, x_column, y_column):
    """Generate summary for pie charts."""
    try:
        total = df[y_column].sum()
        max_slice = df.loc[df[y_column].idxmax()]
        min_slice = df.loc[df[y_column].idxmin()]
        max_percentage = (max_slice[y_column] / total) * 100
        min_percentage = (min_slice[y_column] / total) * 100
        
        # Calculate concentration - how much of the pie is in the top 20% of categories
        sorted_df = df.sort_values(by=y_column, ascending=False)
        top_n = max(1, int(len(df) * 0.2))
        top_share = (sorted_df.iloc[:top_n][y_column].sum() / total) * 100
        
        summary = f"""### 🥧 Pie Chart Composition Analysis

This visualization breaks down {y_column} across different {x_column} categories.

**Composition Highlights:**
<ul>
  <li><b>Total Value:</b> {total:,.2f}</li>
  <li><b>Dominant Category:</b> {max_slice[x_column]} represents {max_percentage:.1f}% of the total</li>
  <li><b>Smallest Category:</b> {min_slice[x_column]} accounts for only {min_percentage:.1f}%</li>
  <li><b>Concentration:</b> The top {top_n} categories make up {top_share:.1f}% of the total</li>
  <li><b>Diversity:</b> Data spread across {len(df)} distinct categories</li>
</ul>

<p><em>Tip: Focus on the largest segments first, and consider grouping very small segments for clearer insights.</em></p>"""

        return summary
    except Exception:
        return f"This pie chart shows {y_column} by {x_column}."

def generate_box_summary(df, x_column, y_column):
    """Generate summary for box plots."""
    try:
        median = df[y_column].median()
        q1 = df[y_column].quantile(0.25)
        q3 = df[y_column].quantile(0.75)
        iqr = q3 - q1
        lower_whisker = max(df[y_column].min(), q1 - 1.5 * iqr)
        upper_whisker = min(df[y_column].max(), q3 + 1.5 * iqr)
        
        # Check for potential outliers
        outliers = df[(df[y_column] < lower_whisker) | (df[y_column] > upper_whisker)]
        outlier_count = len(outliers)
        
        spread_description = "tightly clustered" if iqr < (q3 - q1) * 0.5 else "widely spread" if iqr > (q3 - q1) * 2 else "moderately spread"
        
        summary = f"""### 📦 Box Plot Distribution Analysis

This visualization shows the statistical distribution of {y_column} values.

**Distribution Breakdown:**
<ul>
  <li><b>Middle Value (Median):</b> {median:,.2f}</li>
  <li><b>Middle 50% Range:</b> From {q1:,.2f} (25th percentile) to {q3:,.2f} (75th percentile)</li>
  <li><b>Spread Assessment:</b> The data is {spread_description} with an interquartile range of {iqr:,.2f}</li>
  <li><b>Range Without Outliers:</b> From {lower_whisker:,.2f} to {upper_whisker:,.2f}</li>
  <li><b>Potential Outliers:</b> {outlier_count} data points fall outside the expected range</li>
</ul>

<p><em>Tip: Look at the box size (middle 50% of data) and position of the median line to understand data concentration and skew.</em></p>"""

        return summary
    except Exception:
        return f"This box plot shows the distribution of {y_column}."