import plotly.express as px
import streamlit as st

# Define your asset classes and their corresponding allocations
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
st.plotly_chart(fig, use_container_width=True)

# # Plotting the pie chart for positive allocations
# fig, ax = make_subplots()
# ax.pie(positive_allocations, labels=positive_asset_classes, autopct='%1.1f%%', startangle=90)
# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# px.title('Portfolio Allocations (Positive Allocations Only)')

# # Display the key for all asset classes (whether in the pie chart or not)
# # Display the key for all asset classes with allocation type labels
# legend_labels = {asset: asset if asset in positive_asset_classes else asset for asset in asset_classes}
# legend_handles = [px.Line2D([0], [0], marker='o', color='w', markerfacecolor='red' if asset in negative_asset_classes else 'green', markersize=10, label=label) for asset, label in legend_labels.items()]

# # Display the legend
# px.legend(handles=legend_handles, labels=legend_labels.values(), loc='center left', bbox_to_anchor=(1, 1))

# # Show the plot
# px.show()

