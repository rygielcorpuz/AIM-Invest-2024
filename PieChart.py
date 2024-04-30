import streamlit as st
import pandas as pd
import plotly.express as px

# Read the CSV file into a DataFrame
df_csv = pd.read_csv('Risk_Score1.csv')

# Define your asset classes and their corresponding allocations
asset_classes = [
    'Communication Services', 'Consumer Discretionary', 'Consumer Staples',
    'Energy', 'Financials', 'Health Care', 'Industrials', 'Information Technology',
    'Materials', 'Real Estate', 'Utilities'
]

# Set the risk score for testing
risk_score = 0

# Find the row corresponding to the selected risk score
row = df_csv[df_csv['Risk Score'] == risk_score]

# Extract columns C to M (index 2 to 13) from the selected row
selected_data = row.iloc[:, 2:14].values.tolist()[0]

# Replace allocations with the selected data
allocations = selected_data

# Filter out negative allocations and their corresponding asset classes
positive_allocations = []
positive_asset_classes = []
negative_asset_classes = []

for asset, alloc in zip(asset_classes, allocations):
    if alloc >= 0:
        positive_asset_classes.append(asset)
        positive_allocations.append(alloc)

# Create a DataFrame for positive allocations
df = pd.DataFrame({'Asset Class': positive_asset_classes, 'Allocation': positive_allocations})

# Plotting the pie chart for positive allocations
fig = px.pie(df, values='Allocation', names='Asset Class', title='Portfolio Allocations (Positive Allocations Only)',
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.update_traces(textposition='inside', textinfo='percent+label')

# Display the plot using Streamlit
st.plotly_chart(fig)
