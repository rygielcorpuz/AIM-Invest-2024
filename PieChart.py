import plotly.express as px
import streamlit as st
import json
asset_classes = [
    'Communication Services', 'Consumer Discretionary', 'Consumer Staples',
    'Energy', 'Financials', 'Health Care', 'Industrials', 'Information Technology',
    'Materials', 'Real Estate', 'Utilities'
]

allocations = [
    -0.47312298643488293, 0.053050744198994394, -0.6107992816519578,
    0.49255242795907644, 0.14420839055863732, 0.17455517102087623,
    0.04867145837128394, 0.2785425979972478, -0.09150048677916986,
    0.9188028169402195, 0.06503914781967507
]

# Filter out negative allocations and their corresponding asset classes
positive_allocations = []
positive_asset_classes = []
negative_asset_classes = []

for asset, alloc in zip(asset_classes, allocations):
    if alloc >= 0:
        positive_asset_classes.append(asset)
        positive_allocations.append(alloc)

import pandas as pd
df = pd.DataFrame({'Asset Class': positive_asset_classes, 'Allocation': positive_allocations})

# Plotting the pie chart for positive allocations
fig = px.pie(df, values='Allocation', names='Asset Class', title='Portfolio Allocations (Positive Allocations Only)')
fig.update_traces(textposition='inside', textinfo='percent+label')

# Display the plot
fig.show()