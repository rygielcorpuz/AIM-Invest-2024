
'''
pip install yahoo_fin

pip install pandas_ta

pip install selectorlib

pip install requests-html
'''


import requests
import json

# Function to fetch data from the API
def fetch_data(api_key):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=technology&limit=1000&time_from=20220101T0130&time_to=20221231T0130&apikey={api_key}'
    r = requests.get(url)
    return r.json()

def fetch_data1(api_key):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=technology&limit=1000&time_from=20230101T0130&time_to=20230601T0130&apikey={api_key}'
    r = requests.get(url)
    return r.json()

def fetch_data2(api_key):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=technology&limit=1000&time_from=20230602T0130&time_to=20231231T0130&apikey={api_key}'
    r = requests.get(url)
    return r.json()

def fetch_data3(api_key):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=technology&limit=1000&time_from=20240101T0130&apikey={api_key}'
    r = requests.get(url)
    return r.json()

# List to store data from multiple API calls
combined_data = []

# Replace 'your_api_key' with your actual API key
api_key = ''

# Make multiple API calls and append data to the list
for _ in range(1):  # Example: Making 5 API calls
    data = fetch_data(api_key)
    #print(data)
    combined_data.extend(data['feed'])
    data1 = fetch_data1(api_key)
    combined_data.extend(data1['feed'])
    data2 = fetch_data3(api_key)
    combined_data.extend(data2['feed'])
    data3 = fetch_data3(api_key)
    combined_data.extend(data3['feed'])

# Write the combined data to a JSON file
with open('combined_article_links.json', 'w') as json_file:
    json.dump(combined_data, json_file, indent=4)

with open('/content/combined_article_links.json', 'r') as json_file:
    data = json.load(json_file)

# Print the contents of the JSON file
print(json.dumps(data, indent=4))

import json
import csv

# Load JSON data
with open('combined_article_links.json') as json_file:
    data = json.load(json_file)
# Open CSV file for writing
with open('outputnew.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=[
        'Full_Article_Sentiment', 'Summary_Sentiment', 'Date_Of_Publication',
        'Title', 'Ticker_Covered', 'Ticker_Sentiment_Score', 'Author', 'Author_Link', 'Summary'
    ])

    # Write CSV header
    writer.writeheader()

    # Iterate through JSON data and write to CSV
    for item in data:
        for ticker_info in item['ticker_sentiment']:
            row = {
                'Full_Article_Sentiment': ticker_info['ticker_sentiment_score'],
                'Summary_Sentiment': item['overall_sentiment_score'],
                'Date_Of_Publication': item['time_published'][:4] + '-' + item['time_published'][4:6] + '-' + item['time_published'][6:8],
                'Title': item['title'],
                'Ticker_Covered': ticker_info['ticker'],
                'Ticker_Sentiment_Score': ticker_info['ticker_sentiment_score'],
                'Author': ', '.join(item['authors']),
                'Author_Link': item['url'],  # No author link provided in JSON
                'Summary': item['summary'],
            }
            writer.writerow(row)

import pandas as pd
test = pd.read_csv('outputnew.csv')

pip install pandas==1.5.3

test

import os
import pandas as pd
import yfinance as yf
from yahoo_fin.stock_info import get_data
import pandas_ta as ta
import re

# Replace 'your_dataset.csv' with the path to your CSV file
#file_path
file_path = 'outputnew.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(file_path,error_bad_lines=False)

# Filter out rows where 'Ticker_Covered' is empty or NaN
df_filtered = df[df["Ticker_Covered"].notna() & (df["Ticker_Covered"] != "")]

# Get the unique tickers into a list
unique_tickers = df_filtered["Ticker_Covered"].unique().tolist()

# Print the list of unique tickers
print(len(unique_tickers))


# Your output list
output_list = unique_tickers

# Regular expression to find text in parentheses
ticker_pattern = re.compile(r"\((.*?)\)")

# Extract tickers using the regular expression
tickers_only = [
    ticker_pattern.search(name).group(1)
    for name in output_list
    if ticker_pattern.search(name)
]

# Print the list of tickers
print(tickers_only)


# List of tickers you want to get data for
#tickers = tickers_only
tickers = unique_tickers

# The directory where you want to save the CSV file
output_directory = "stock_data_csv"
os.makedirs(output_directory, exist_ok=True)

# Define the date range and interval for the historical data
start_date = "2022-09-29"
end_date = "2024-03-21"
interval = "1d"  # 1 day

# Define the parameters for the MACD
macd_fast = 12
macd_slow = 26
macd_signal = 9

# Prepare an empty list to store the DataFrames
dataframes = []
print(len(tickers))
# Loop through the list of tickers and retrieve/save the data
for ticker in tickers:
    try:
        print(f"Getting data for {ticker}")
        # Retrieve stock data
        data = get_data(
            ticker, start_date=start_date, end_date=end_date, interval=interval
        )

        # Reset the index to turn the date index into a column if it is not already
        data.reset_index(inplace=True)

        # Rename the date column if necessary to ensure clarity
        if "index" in data.columns:
            data.rename(columns={"index": "Date"}, inplace=True)

        # Ensure the date column is in datetime format (usually it should already be)
        data["Date"] = pd.to_datetime(data["Date"])

        # Add a new column for the ticker symbol
        data["Ticker"] = ticker

        # Calculate the Money Flow Index (MFI)
        data["MFI"] = ta.mfi(data["high"], data["low"], data["close"], data["volume"])

        # Calculate the Moving Average Convergence Divergence (MACD)
        macd = ta.macd(
            data["close"], fast=macd_fast, slow=macd_slow, signal=macd_signal
        )
        data = pd.concat([data, macd], axis=1)

        # Calculate the Bollinger Bands and %B
        bbands = ta.bbands(data["close"])
        data["%B"] = (data["close"] - bbands["BBL_5_2.0"]) / (
            bbands["BBU_5_2.0"] - bbands["BBL_5_2.0"]
        )
        data = pd.concat([data, bbands], axis=1)

        # Append the DataFrame to the list
        dataframes.append(data)

    except Exception as e:
        print(f"Failed to get data for {ticker}: {e}")

# Concatenate all the DataFrames in the list
print(len(dataframes))
combined_data = pd.concat(dataframes)

# Ensure 'Date' is a column and not an index
if "Date" not in combined_data.columns:
    combined_data.reset_index(inplace=True)
    combined_data.rename(columns={"index": "Date"}, inplace=True)

# Define the new order of the columns with 'Ticker' and 'Date' first
column_order = ["Ticker", "Date"] + [
    col for col in combined_data.columns if col not in ["Ticker", "Date"]
]

# Reindex the DataFrame with the new column order
combined_data = combined_data[column_order]
combined_data = combined_data.drop(columns=["ticker"])

# Ensure 'Date' is a datetime object
combined_data["Date"] = pd.to_datetime(combined_data["Date"])

# Convert 'Date' to the format 'MM/DD/YYYY'
combined_data["Date"] = combined_data["Date"].dt.strftime("%m/%d/%Y")

# Save the combined data to a single CSV file
csv_file_path = os.path.join(output_directory, "combined_stock_data.csv")
combined_data.to_csv(csv_file_path, index=False)
print(f"Combined data saved to {csv_file_path}")

print("Data retrieval and calculations complete.")

dff = pd.read_csv('combined_stock_data.csv',error_bad_lines=False)

dff

# Feature Engineering for the stock dataset
import pandas as pd

stock_data_path = "combined_stock_data.csv"

# Re-load the stock data in case we need a fresh start
stock_data = pd.read_csv(stock_data_path, parse_dates=["Date"])

# Make sure 'Date' is the index for easier manipulation
stock_data.set_index("Date", inplace=True)

# Calculate daily percentage change in closing price
stock_data["daily_pct_change"] = stock_data["adjclose"].pct_change()

# Calculate moving averages for closing prices
stock_data["close_5_day_ma"] = stock_data["adjclose"].rolling(window=5).mean()
stock_data["close_20_day_ma"] = stock_data["adjclose"].rolling(window=20).mean()

# Calculate volatility (standard deviation of daily pct change over last 20 days)
stock_data["volatility_20_day"] = (
    stock_data["daily_pct_change"].rolling(window=20).std()
)

# Calculate daily percentage change in volume
stock_data["volume_pct_change"] = stock_data["volume"].pct_change()


# Calculate moving averages for volume
stock_data["volume_5_day_ma"] = stock_data["volume"].rolling(window=5).mean()
stock_data["volume_20_day_ma"] = stock_data["volume"].rolling(window=20).mean()

# Use existing technical indicators but make sure there are no missing values
# For the sake of this example, we will fill missing values with the median of the column

technical_indicators = [
    "MFI",
    "MACD_12_26_9",
    "MACDh_12_26_9",
    "MACDs_12_26_9",
    "%B",
    "BBL_5_2.0",
    "BBM_5_2.0",
    "BBU_5_2.0",
    "BBB_5_2.0",
    "BBP_5_2.0",
]
stock_data[technical_indicators] = stock_data[technical_indicators].fillna(
    stock_data[technical_indicators].median()
)

# Fill missing values in the entire DataFrame with the mean of each column
stock_data.fillna(stock_data.mean(), inplace=True)

# Reset index before exporting to make sure 'Date' is a column
stock_data.reset_index(inplace=True)

# Define the path for the stock features CSV file
stock_features_path = "stock_features.csv"

# Export the enhanced stock data to a CSV file
stock_data.to_csv(stock_features_path, index=False)

sentiment_data_path = "outputnew.csv"
# Re-load the sentiment data to start fresh
sentiment_data = pd.read_csv(sentiment_data_path, parse_dates=["Date_Of_Publication"])

# Daily Average Sentiment
# Group by Date and Ticker to calculate daily average sentiment scores
daily_sentiment = (
    sentiment_data.groupby(["Date_Of_Publication", "Ticker_Covered"])
    .agg({"Full_Article_Sentiment": "mean", "Summary_Sentiment": "mean"})
    .reset_index()
)

# Sentiment Score Change
# Calculate the day-over-day change in sentiment for each ticker
daily_sentiment["change_in_full_sentiment"] = daily_sentiment.groupby("Ticker_Covered")[
    "Full_Article_Sentiment"
].diff()
daily_sentiment["change_in_summary_sentiment"] = daily_sentiment.groupby(
    "Ticker_Covered"
)["Summary_Sentiment"].diff()

# Rolling Average Sentiment
# Compute rolling averages of sentiment scores to smooth out daily fluctuations
daily_sentiment["rolling_avg_full_sentiment"] = daily_sentiment.groupby(
    "Ticker_Covered"
)["Full_Article_Sentiment"].transform(
    lambda x: x.rolling(window=5, min_periods=1).mean()
)
daily_sentiment["rolling_avg_summary_sentiment"] = daily_sentiment.groupby(
    "Ticker_Covered"
)["Summary_Sentiment"].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

# Sentiment Volatility
# Calculate the standard deviation of sentiment scores over a rolling window
daily_sentiment["volatility_full_sentiment"] = daily_sentiment.groupby(
    "Ticker_Covered"
)["Full_Article_Sentiment"].transform(
    lambda x: x.rolling(window=5, min_periods=1).std()
)
daily_sentiment["volatility_summary_sentiment"] = daily_sentiment.groupby(
    "Ticker_Covered"
)["Summary_Sentiment"].transform(lambda x: x.rolling(window=5, min_periods=1).std())

# Renaming columns for clarity
daily_sentiment.rename(
    columns={"Date_Of_Publication": "Date", "Ticker_Covered": "Ticker"}, inplace=True
)

daily_sentiment.fillna(sentiment_data.mean(), inplace=True)
# Export the sentiment features to a CSV file
sentiment_features_path = "sentiment_features.csv"
daily_sentiment.to_csv(sentiment_features_path, index=False)

ds = pd.read_csv('sentiment_features.csv')

ds

sf = pd.read_csv('stock_features.csv')

sf





import pandas as pd

# Assuming 'stock_data' and 'sentiment_data' are already loaded and preprocessed Pandas DataFrames
stock_data = pd.read_csv("combined_stock_data.csv", parse_dates=["Date"])
sentiment_data = pd.read_csv("sentiment_features.csv", parse_dates=["Date"])

# Merge the datasets on 'Date' and 'Ticker'
combined_data = pd.merge(stock_data, sentiment_data, on=["Date", "Ticker"], how="outer")

# Handle missing values, for example, by filling with the mean
#combined_data.fillna(combined_data.mean(), inplace=True)
combined_data_filled = combined_data.fillna(combined_data.groupby('Ticker').transform('mean'))
combined_data_filled.fillna(combined_data.mean(), inplace=True)
#combined_data_filled.dropna(axis=0,how='any', inplace=True)
#combined_data.dropna(how='any')
# Ensure the final DataFrame is sorted by date for time-series analysis
combined_data_filled.sort_values(by="Date", inplace=True)


# Now 'combined_data' is ready to be used for model training

combined_data_filled.to_csv("combined_data_market_final.csv", index=False)

import pandas as pd
fdf = pd.read_csv("combined_data_market_final.csv")

# Set display options to show all columns
pd.set_option('display.max_columns', None)

#fdf.fillna(fdf.groupby('Ticker').transform('mean'))
#fdf.dropna(axis=0,how='any', inplace=True)
#fdf.to_csv("combined_data_market_final.csv", index=False)

fdf

fdf.fillna(fdf.groupby('Ticker').transform('mean'))
fdf

column_names = fdf.columns.astype(str).tolist()

# Print all column names as strings
print(column_names)

pip install keras==2.15.0

pip install tensorflow==2.15.0

from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd

combined_data = pd.read_csv("combined_data_market_final.csv", parse_dates=["Date"])
# Drop non-numeric columns
numeric_data = combined_data.drop(columns=["Date", "Ticker"])

# Check for infinities and replace them with NaN
numeric_data = numeric_data.replace([np.inf, -np.inf], np.nan)

# Now, check if there are any NaNs in the DataFrame
print(numeric_data.isna().sum())

# You can choose to fill NaNs with a value, such as the mean or median of the column
# For example, to fill with the mean:
numeric_data.fillna(numeric_data.mean(), inplace=True)

# Ensure there are no longer any infinities or NaNs
assert not numeric_data.isin([np.inf, -np.inf, np.nan]).any().any()

# Now you can proceed with scaling
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(numeric_data)


# Define the sequence length (the window of data the LSTM will see for making the next prediction)
sequence_length = 20  # For example, we might want to look at 20 days of stock data to predict the next day

# Prepare the input and output sequences
X, y = [], []
for i in range(len(scaled_features) - sequence_length):
    X.append(scaled_features[i : i + sequence_length])
    y.append(
        scaled_features[i + sequence_length, numeric_data.columns.get_loc("adjclose")]
    )  # Predicting the next day's adjusted close price

X = np.array(X)
y = np.array(y)

# Define the train data size
train_size = int(len(X) * 0.8)

# Split the data
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# The LSTM will expect input data in the form of (number of samples, number of time steps, number of features per step)
# Since we're predicting stock prices, our output will be one-dimensional (the predicted 'adjclose' price)

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout

# Assuming 'n_features' is the number of features in the scaled feature data
n_features = X.shape[2]

model = Sequential()
model.add(
    LSTM(units=50, return_sequences=True, input_shape=(sequence_length, n_features))
)
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=False))
model.add(Dropout(0.2))
model.add(
    Dense(units=1)
)  # The output layer that predicts the next day's 'adjclose' price

model.compile(optimizer="adam", loss="mean_squared_error")

# Let's see the model summary
model.summary()

# Define the number of epochs and batch size
epochs = 50  # The number of iterations over the entire dataset
batch_size = 32  # The number of samples per gradient update

# Train the model
history = model.fit(
    X_train,
    y_train,
    epochs=epochs,
    batch_size=batch_size,
    validation_data=(X_test, y_test),
    verbose=1,
)
# Evaluate the model
loss = model.evaluate(X_test, y_test, verbose=1)
print(f"Test loss: {loss}")

model.save('trained_lstm_model50.h5')

from tensorflow.keras.models import load_model

# Load the model from the .h5 file
model = load_model('trained_lstm_model50.h5')