"""
Chart analysis chatbot component
"""
import streamlit as st
import pandas as pd
import numpy as np

class ChartAnalyzer:
    def __init__(self, df, chart_type, x_column, y_column=None):
        self.df = df
        self.chart_type = chart_type
        self.x_column = x_column
        self.y_column = y_column
        
    def answer_question(self, question):
        """Generate response based on the question and chart context."""
        question = question.lower().strip()
        
        try:
            # Analyze trends
            if any(word in question for word in ['trend', 'pattern', 'change']):
                return self._analyze_trends()
                
            # Compare values
            elif any(word in question for word in ['compare', 'difference', 'versus', 'vs']):
                return self._compare_values()
                
            # Find extremes
            elif any(word in question for word in ['highest', 'lowest', 'maximum', 'minimum', 'peak', 'top', 'bottom']):
                return self._find_extremes()
                
            # Distribution analysis
            elif any(word in question for word in ['distribution', 'spread', 'range', 'variation']):
                return self._analyze_distribution()
                
            # Average and central tendency
            elif any(word in question for word in ['average', 'mean', 'median', 'typical']):
                return self._analyze_central_tendency()
                
            # General insights
            elif any(word in question for word in ['insight', 'tell', 'what', 'explain', 'describe']):
                return self._generate_general_insights()
                
            # Default response
            else:
                return self._generate_general_insights()
                
        except Exception as e:
            return f"I apologize, but I couldn't analyze that aspect of the chart. Please try asking in a different way."

    def _analyze_trends(self):
        """Analyze trends in the data."""
        if self.chart_type in ['line', 'area']:
            # For time series
            first_val = self.df[self.y_column].iloc[0]
            last_val = self.df[self.y_column].iloc[-1]
            change = ((last_val - first_val) / first_val) * 100
            
            # Calculate volatility
            std_dev = self.df[self.y_column].std()
            mean = self.df[self.y_column].mean()
            volatility = (std_dev / mean) * 100
            
            return f"""Looking at the trend over time, I notice that {self.y_column} has {'increased' if change > 0 else 'decreased'} 
            by approximately {abs(change):.1f}% from {first_val:,.2f} to {last_val:,.2f}.
            
            The data shows {'high' if volatility > 25 else 'moderate' if volatility > 10 else 'low'} volatility 
            ({volatility:.1f}% relative to the mean), which suggests {'significant fluctuations' if volatility > 25 
            else 'some variation' if volatility > 10 else 'relatively stable behavior'} over this period.
            
            {'You might want to investigate the factors causing the large swings in values.' if volatility > 25 
            else 'The pattern appears fairly predictable and manageable.' if volatility < 10 
            else 'There is a moderate level of variability that might need monitoring.'}\n"""
            
        else:
            return self._generate_general_insights()

    def _compare_values(self):
        """Compare different values or categories."""
        if self.y_column:
            grouped = self.df.groupby(self.x_column)[self.y_column].agg(['mean', 'count'])
            total = self.df[self.y_column].sum()
            
            # Get top 3 and bottom 3
            top3 = grouped.nlargest(3, 'mean')
            bottom3 = grouped.nsmallest(3, 'mean')
            
            insights = f"""Let me break down the comparison for you:

Top performers:
"""
            for idx, row in top3.iterrows():
                percentage = (row['mean'] * row['count'] / total) * 100
                insights += f"• {idx}: {row['mean']:,.2f} ({percentage:.1f}% of total)\n"
                
            insights += "\nLower performers:\n"
            for idx, row in bottom3.iterrows():
                percentage = (row['mean'] * row['count'] / total) * 100
                insights += f"• {idx}: {row['mean']:,.2f} ({percentage:.1f}% of total)\n"
                
            avg = self.df[self.y_column].mean()
            insights += f"\nThe average across all categories is {avg:,.2f}."
            
            return insights
        else:
            return "I can only compare values when there's both an X and Y axis in the chart."

    def _find_extremes(self):
        """Find and explain extreme values."""
        if self.y_column:
            max_val = self.df[self.y_column].max()
            min_val = self.df[self.y_column].min()
            max_row = self.df.loc[self.df[self.y_column] == max_val].iloc[0]
            min_row = self.df.loc[self.df[self.y_column] == min_val].iloc[0]
            
            avg = self.df[self.y_column].mean()
            max_diff = ((max_val - avg) / avg) * 100
            min_diff = ((avg - min_val) / avg) * 100
            
            return f"""Let me point out the notable extremes in the data:

Highest Point:
• {self.y_column}: {max_val:,.2f}
• {self.x_column}: {max_row[self.x_column]}
• This is {max_diff:.1f}% above the average

Lowest Point:
• {self.y_column}: {min_val:,.2f}
• {self.x_column}: {min_row[self.x_column]}
• This is {min_diff:.1f}% below the average

{'The difference between the highest and lowest points is quite significant.' if max_diff + min_diff > 100 
else 'The values are relatively consistent across the dataset.' if max_diff + min_diff < 50 
else 'There is a moderate spread between the highest and lowest values.'}\n"""
        else:
            return "I can only analyze extreme values when there's both an X and Y axis in the chart."

    def _analyze_distribution(self):
        """Analyze the distribution of values."""
        if self.y_column:
            q1 = self.df[self.y_column].quantile(0.25)
            q3 = self.df[self.y_column].quantile(0.75)
            median = self.df[self.y_column].median()
            iqr = q3 - q1
            skew = self.df[self.y_column].skew()
            
            distribution_type = (
                "right-skewed (higher values are more spread out)" if skew > 0.5
                else "left-skewed (lower values are more spread out)" if skew < -0.5
                else "fairly symmetrical"
            )
            
            spread = (
                "widely spread" if iqr > (q3 - q1) * 2
                else "tightly clustered" if iqr < (q3 - q1) * 0.5
                else "moderately spread"
            )
            
            return f"""Looking at how the values are distributed:

The data is {distribution_type} and {spread}.

• 25% of values fall below {q1:,.2f}
• The middle value (median) is {median:,.2f}
• 75% of values fall below {q3:,.2f}
• The middle 50% of values span a range of {iqr:,.2f}

{'This suggests quite a bit of variability in the data.' if iqr > (q3 - q1) * 2
else 'The values are quite consistent and predictable.' if iqr < (q3 - q1) * 0.5
else 'The spread of values is typical for this type of data.'}\n"""
        else:
            return "I can only analyze the distribution when there's both an X and Y axis in the chart."

    def _analyze_central_tendency(self):
        """Analyze average and typical values."""
        if self.y_column:
            mean = self.df[self.y_column].mean()
            median = self.df[self.y_column].median()
            mode = self.df[self.y_column].mode().iloc[0]
            std = self.df[self.y_column].std()
            
            return f"""Let me break down the typical values in this data:

• The average (mean) is {mean:,.2f}
• The middle value (median) is {median:,.2f}
• The most common value is {mode:,.2f}

{'The mean and median are quite different, suggesting some extreme values are pulling the average up.' if mean > median * 1.2
else 'The mean and median are very close, suggesting a balanced distribution.' if abs(mean - median) < median * 0.1
else 'There is some skew in the data, but nothing too extreme.'}

About 68% of the values fall between {(mean - std):,.2f} and {(mean + std):,.2f}.\n"""
        else:
            return "I can only analyze typical values when there's both an X and Y axis in the chart."

    def _generate_general_insights(self):
        """Generate general insights about the chart."""
        try:
            if self.y_column:
                total = self.df[self.y_column].sum()
                avg = self.df[self.y_column].mean()
                unique_count = self.df[self.x_column].nunique()
                
                # Try to identify any patterns
                if self.chart_type in ['line', 'area']:
                    first_val = self.df[self.y_column].iloc[0]
                    last_val = self.df[self.y_column].iloc[-1]
                    change = ((last_val - first_val) / first_val) * 100
                    pattern = f"Overall, there has been a {abs(change):.1f}% {'increase' if change > 0 else 'decrease'}."
                else:
                    std = self.df[self.y_column].std()
                    cv = (std / avg) * 100
                    pattern = (f"There is {'high' if cv > 50 else 'moderate' if cv > 25 else 'low'} "
                             f"variation across {self.x_column}s.")
                
                return f"""Let me explain what I see in this chart:

This visualization shows how {self.y_column} varies across {unique_count} different {self.x_column}s.

The total {self.y_column} is {total:,.2f}, with an average of {avg:,.2f} per {self.x_column}.

{pattern}

Would you like me to:
1. Analyze specific trends?
2. Compare different categories?
3. Look at extreme values?
4. Examine the distribution?

Just ask me about any of these aspects!\n"""
            else:
                count = len(self.df)
                unique_count = self.df[self.x_column].nunique()
                
                return f"""This chart shows the distribution of {self.x_column}.

There are {count} total data points across {unique_count} unique values.

Would you like me to analyze any specific aspect of the distribution?\n"""
                
        except Exception as e:
            return "I can provide a general analysis of the chart. What specific aspect would you like to know more about?"