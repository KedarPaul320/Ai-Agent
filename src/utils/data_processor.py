"""
Data processing utilities
"""
import pandas as pd

def filter_dataframe(df, column, start_value, end_value):
    """Filter dataframe by value range."""
    try:
        # Handle datetime columns
        if pd.api.types.is_datetime64_any_dtype(df[column]):
            mask = (df[column] >= pd.Timestamp(start_value)) & (df[column] <= pd.Timestamp(end_value))
        # Handle numeric columns
        elif pd.api.types.is_numeric_dtype(df[column]):
            mask = (df[column] >= start_value) & (df[column] <= end_value)
        else:
            return df
        
        return df[mask]
    except Exception as e:
        print(f"Error filtering dataframe: {str(e)}")
        return df