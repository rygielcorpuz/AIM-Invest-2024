import streamlit as st
import pandas as pd #helps w/ data manipulation
import re
import requests # helps send & receive response from web browswer
import plotly
import plotly.express as px
import json # for graph plotting in website
import nltk # NLTK VADER for sentiment analysis
import yfinance as yf 
import webbrowser
import base64
import numpy as np
nltk.downloader.download('vader_lexicon')
from datetime import datetime
from streamlit_option_menu import option_menu
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs #important for data scraping
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go #plotly is an interactive graph

title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>Stock Search</h1>"
st.markdown(title_html, unsafe_allow_html=True)


START = "2015-01-01" #where data starts
TODAY = datetime.today().strftime("%Y-%m-%d") #all the way to today

ticker = st.text_input("Enter Ticker Name")
st.write("Some common tickers:  \n- AMZN: Amazon  \n- AAPL: Apple  \n- GOOG: Google  \n- MSFT: Microsoft  \n- TSLA: Tesla")

run = st.button("Search")
if run:
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text("Loading data...")
    data = load_data(ticker)
    data_load_state.text("Loading data...done!")

            #not sure if we need this
            # st.subheader('Raw data')
            # st.write(data.tail())

            # # Plot raw data
            # def plot_raw_data():
            #     fig = go.Figure()
            #     fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
            #     fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
            #     fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
            #     st.plotly_chart(fig)

            # plot_raw_data()

            # # Predict forecast with Prophet.
            # df_train = data[['Date','Close']]
            # df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

            # m = Prophet()
            # m.fit(df_train)
            # future = m.make_future_dataframe(periods=period)
            # forecast = m.predict(future)

            # # Show and plot forecast
            # st.subheader('Forecast data')
            # st.write(forecast.tail())
                
            # st.write(f'Forecast plot for {n_years} years')
            # fig1 = plot_plotly(m, forecast)
            # st.plotly_chart(fig1)

            # st.write("Forecast components")
            # fig2 = m.plot_components(forecast)
            # st.write(fig2)


            #Function: GET NEWS TICKER  
    def get_news(ticker):
        finviz_url = "https://finviz.com/quote.ashx?t="
        url = finviz_url + ticker
        req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
        response = urlopen(req)
        # Read the contents of the file into 'html'
        html = bs(response,'html.parser')
        # Find 'news-table' in the Soup and load it into 'news_table'
        news_table = html.find(id='news-table')
        return news_table


    #Function: PARSING THRU THE NEWS TABLE
    def parse_news(news_table):
        # Parse news data from HTML table into df
        arrayList = []

        for x in news_table.find_all('tr'):
        # Parameters:
        #news_table (BeautifulSoup object): HTML table containing news data
            try:
                headline = x.a.get_text() #'a' tag for the headline of the article, u need parenthesis so function knows what to call, otherwise it'll be confused
                #print(headline)
                td = x.td.text.split() #this is to split the time and the date
                #  print(td)
                #  td creates a list
                if len(td) == 1:
                    time = td[0]
                    #set time with 2nd index
                else: #this would be anything greater than one
                    date = td[0] #date is first on list [0], then consecutively time is [1]
                    time = td[1]
                    arrayList.append([date, time, headline]) #putting an date, time, and headline arrayList inside of here
                #making a list of column names

                #set date w first index of td
            except:
                pass
            columnName = ['date', 'time', 'headline']

            df = pd.DataFrame(arrayList, columns=columnName)

            #replacing 'today' with date, make sure not to use 'dataFrame' bc pandas doesnt know which function ur calling
            df['date'] = df['date'].replace('Today', datetime.today().strftime('%Y-%m-%d')) #this is getting the world time & formatting it
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='mixed')
            #df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], infer_datetime_format=True)
            #df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

                # Returns:
                #   parsed_news_df (df): Parsed news data with columns: date, time, headline, datetime
        return df
    sid = SentimentIntensityAnalyzer()


    #Function: SCORES ARTICLES FOR SENTIMENT ANALYSIS
    def score_news(parsed_news_df):
            
        # iterate through parsed_news_df headlines and compute polarity scores
        scores = [] #creates an empty list to put the sentiment scores in
        for headline in parsed_news_df['headline']:
            score = sid.polarity_scores(headline) #computes scores
            scores.append(score)

        # convert scores to DataFrame
        scores_df = pd.DataFrame(scores)

        # appending data frames
        parsed_scored_news = parsed_news_df.join(scores_df) #adds scores to og dataframe

        # Drop unnecessary columns
        parsed_scored_news.drop(['date', 'time'], axis=1, inplace=True)
        #parsed_scored_news.drop(['date', 'time', 'headline'], axis=1, inplace=True)

        # Rename sentiment score column
        parsed_scored_news.rename(columns={'sentiment': 'sentiment_score'}, inplace=True)

        # Set datetime column as index
        parsed_scored_news.set_index('datetime', inplace=True)

        return parsed_scored_news

    tableNews = get_news(ticker)
    print(tableNews)
    parseNews = parse_news(tableNews)
    print(parseNews)
    df = score_news(parseNews)
    print(df)
    st.dataframe(df)

    # turn headlines into csv
    df.drop(['neg', 'neu', 'pos', 'compound'], axis=1, inplace=True)
    df.to_csv("headlines.csv", index=False)

    #Function: DISPLAYS SENTIMENT GRAPHS VISUALLY
    np.random.seed(0)
    dates = pd.date_range('2022-01-01', periods=100, freq='H')
    df = pd.DataFrame({
        'date': dates,
        'ticker': ticker,
        'sentiment_score': np.random.rand(100)
    })

    def plot_hourly_sentiment(df, ticker):
        # Group by date and ticker columns from scored_news and calculate the mean
        mean_scores = df.groupby(['date', 'ticker']).mean()

        # Plot a bar chart with plotly
        fig = px.bar(mean_scores, x=mean_scores.index.get_level_values(0), y='sentiment_score', title=ticker + ' Hourly Sentiment')
        return fig
            
    #this one isn't loading correctly
    def plot_daily_sentiment(df, ticker):
        # Group by date and ticker columns from scored_news and calculate the mean
        mean_scores = df.groupby(['date', 'ticker']).mean()

        # Plot a bar chart with plotly
        fig = px.bar(mean_scores, x=mean_scores.index.get_level_values(0), y='sentiment_score', title=ticker + ' Daily Sentiment')
        return fig


    # Call the functions
    hourly_fig = plot_hourly_sentiment(df, ticker)
    daily_fig = plot_daily_sentiment(df, ticker)

    # Display the figures
    hourly_fig.show()
    daily_fig.show()