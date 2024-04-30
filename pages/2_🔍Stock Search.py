
import streamlit as st
import pandas as pd #helps w/ data manipulation
import re
import requests # helps send & receive response from web browswer
import plotly
import plotly.express as px
import json # for graph plotting in website
import nltk # NLTK VADER for sentiment analysis
import yfinance as yf 
from fireworks.client import Fireworks
import webbrowser
import base64
import numpy as np
import time
nltk.downloader.download('vader_lexicon')
from datetime import datetime
from streamlit_option_menu import option_menu
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs #important for data scraping
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go #plotly is an interactive graph
from datetime import datetime, timedelta

#tab name for fun
st.set_page_config(
    page_title="PandAI",
    page_icon=":bamboo:",
    initial_sidebar_state="collapsed"
)

title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>Stock Search</h1>"
st.markdown(title_html, unsafe_allow_html=True)
st.markdown("<hr style='border-top: 2px solid green;'>", unsafe_allow_html=True)


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
        count = 0

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
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
            #df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], infer_datetime_format=True)
            #df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

                # Returns:
                #   parsed_news_df (df): Parsed news data with columns: date, time, headline, datetime
        return df
    

    def score_news(parsed_news_df):
        # instantiate sentiment intensity analyzer
        sia = SentimentIntensityAnalyzer()

        # iterate through parsed_news_df headlines and compute polarity scores
        scores = []
        for headline in parsed_news_df['headline']:
            score = sia.polarity_scores(headline)
            scores.append(score)

        # convert scores to DataFrame
        scores_df = pd.DataFrame(scores)

        # join data frames
        parsed_scored = parsed_news_df.join(scores_df)

        # set index of parsed_scored to 'datetime' column
        parsed_scored.set_index('datetime', inplace=True)

        # drop the 'date' and 'time' columns
        parsed_scored.drop(['date', 'time'], axis=1, inplace=True)

        # rename the 'compound' column to 'sentiment_score'
        parsed_scored.rename(columns={'compund': 'sentiment_score'}, inplace=True)

        return parsed_scored

    # Prints the data frame
    tableNews = get_news(ticker)
    print(tableNews)
    parseNews = parse_news(tableNews)
    print(parseNews)
    parseNews.to_csv('temp2.csv', index=False)
    df = score_news(parseNews)
    print(df)
    df.to_csv('temp.csv', index=False)
    st.dataframe(df)

    # turn headlines into csv
    df.drop(['neg', 'neu', 'pos', 'compound'], axis=1, inplace=True)
    df.to_csv("headlines.csv", index=False)
    df = pd.read_csv("headlines.csv")


    text_data = df['headline']


    concatenated_text = "\n".join(text_data)


    concatenated_text = concatenated_text.lower()

    api_key = "AgVn8csdNAt5zUogJAn6CFa6PMUFRInohxjDaoqwsmqdzMPP"


    client = Fireworks(api_key="AgVn8csdNAt5zUogJAn6CFa6PMUFRInohxjDaoqwsmqdzMPP")
    response = client.chat.completions.create(
      model="accounts/fireworks/models/mixtral-8x7b-instruct",
      messages=[{
        "role": "user",
        "content": "analyze the headlines summary and provide insights that would be relevant to a beginner with less experience with stocks",
        "content": concatenated_text,

      }],
    )
    st.write(response.choices[0].message.content)

    #Function: DISPLAYS SENTIMENT GRAPHS VISUALLY 
    np.random.seed(0)
    dates = pd.date_range((datetime.today() - timedelta(days=5)).strftime("%Y-%m-%d"), periods=100, freq='H')
    df = pd.DataFrame({
        'date': dates,
        'ticker': ticker,
        'sentiment_score': np.random.rand(100)
    })

    def plot_hourly_sentiment(df, ticker):
        # Group by date and ticker columns from df and calculate the mean
        mean_scores = df.groupby(['date', 'ticker']).mean()

        # Plot a bar chart with plotly
        fig = px.bar(mean_scores, x=mean_scores.index.get_level_values(0), y='sentiment_score', title=ticker + ' Hourly Sentiment')
        fig.update_xaxes(title_text='Hourly Sentiment')  # Update x-axis label
        fig.update_yaxes(title_text='Sentiment Score')  # Update y-axis label
        return fig

    def plot_daily_sentiment(df, ticker):
        # Group by date and ticker columns from df and calculate the mean
        mean_scores = df.groupby(['ticker', pd.Grouper(key='date', freq='D')]).mean().reset_index()

        # Plot a bar chart with plotly
        fig = px.bar(mean_scores, x='date', y='sentiment_score', title=ticker + ' Daily Sentiment')
        fig.update_xaxes(title_text='Date')  # Update x-axis label
        fig.update_yaxes(title_text='Sentiment Score')  # Update y-axis label
        return fig

    # def plot_hourly_sentiment(df, ticker):
    #     # Group by date and ticker columns from scored_news and calculate the mean
    #     mean_scores = df.groupby(['date', 'ticker']).mean()

    #     # Plot a bar chart with plotly
    #     fig = px.bar(mean_scores, x=mean_scores.index.get_level_values(0), y='sentiment_score', title=ticker + ' Hourly Sentiment')
    #     fig.update_xaxes(title_text='Hourly Sentiment')  # Update x-axis label
    #     fig.update_yaxes(title_text='Sentiment Score')  # Update y-axis label
    #     return fig
            
    # #this one isn't loading correctly
    # def plot_daily_sentiment(df, ticker):
    #     # Group by date and ticker columns from scored_news and calculate the mean
    #     mean_scores = df.groupby(['date', 'ticker']).mean()
    #     #mean_scores = df.resample('D', on='date').mean()

    #     # Plot a bar chart with plotly
    #     fig = px.bar(mean_scores, x=mean_scores.index.get_level_values(0), y='sentiment_score', title=ticker + ' Daily Sentiment')
    #     fig.update_xaxes(title_text='Daily Sentiment')  # Update x-axis label
    #     fig.update_yaxes(title_text='Sentiment Score')  # Update y-axis label
    #     return fig


    # Call the functions
    hourly_fig = plot_hourly_sentiment(df, ticker)
    daily_fig = plot_daily_sentiment(df, ticker)

    # Display the figures
    st.plotly_chart(plot_hourly_sentiment(df, ticker))
    st.plotly_chart(plot_daily_sentiment(df, ticker))
    # hourly_fig.show()
    # daily_fig.show()

    #for the background
    def blur_image(image, radius):
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
        return blurred_image
        
    page_bg_img = """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.freepik.com/free-photo/bamboo-leaf-elements-green_53876-95290.jpg");
        background-size: cover;
    }
    </style>
    """

    st.markdown(page_bg_img, unsafe_allow_html=True)


    #for comic stocks (progress bar)
    st.write("this is for the comic stocks")
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    st.button("Rerun")