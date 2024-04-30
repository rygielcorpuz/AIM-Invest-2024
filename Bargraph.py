

import streamlit as st
from urllib.request import urlopen, Request
from datetime import datetime
from bs4 import BeautifulSoup as bs #important for data scraping
import pandas as pd #helps w/ data manipulation
import plotly
import re
import requests # helps send & receive response from web browswer
import plotly.express as px
import json # for graph plotting in website
# NLTK VADER for sentiment analysis
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_news(ticker):
    finviz_url = "https://finviz.com/quote.ashx?t="
    url = finviz_url + ticker
    req = Request(url=url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'})
    response = urlopen(req)
    # Read the contents of the file into 'html'
    html = bs(response)
    # Find 'news-table' in the Soup and load it into 'news_table'
    news_table = html.find(id='news-table')
    return news_table

    pass

ticker = "AAPL"
news = get_news(ticker)
print(news.prettify())

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

      #replacing 'today' with date, make sure not to use 'dataFrame' bc pandas doesnt know which function ur callign
        df['date'] = df['date'].replace('Today', datetime.today().strftime('%Y-%m-%d')) #this is getting the world time & formatting it
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    # Returns:
    #   parsed_news_df (df): Parsed news data with columns: date, time, headline, datetime
    return df




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


sid = SentimentIntensityAnalyzer()

parse_news(news)

score_news(parse_news(news))

url = "https://finviz.com/quote.ashx?t=AAPL"

response = requests.get(url)

print(response)

html_page = bs(response.content, 'html.parser')

html_page

if not isinstance(html_page, bs):
    raise TypeError("`html_page` must be a BeautifulSoup object")

tableNews = get_news(ticker)
parseNews = parse_news(tableNews)

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


tableNews = get_news(ticker)
print(tableNews)
parseNews = parse_news(tableNews)
print(parseNews)
df = score_news(parseNews)
print(df)
st.dataframe(df)

import plotly.express as px
import pandas as pd
import numpy as np

# Sample DataFrame
np.random.seed(0)
dates = pd.date_range('2024-01-01', periods=100, freq='H')
df = pd.DataFrame({
    'date': dates,
    'ticker': 'AAPL',
    'sentiment_score': np.random.rand(100)
})


def plot_hourly_sentiment(df, ticker):
    # Group by date column from df and calculate the mean
    mean_scores = df.groupby(df['date'].dt.hour)['sentiment_score'].mean()

    # Plot a bar chart with plotly
    fig = px.bar(mean_scores, x=mean_scores.index, y='sentiment_score', title=ticker + ' Hourly Sentiment')
    return fig

def plot_daily_sentiment(df, ticker):
    # Group by date column from df and calculate the mean
    mean_scores = df.groupby(df['date'].dt.date)['sentiment_score'].mean()

    # Plot a bar chart with plotly
    fig = px.bar(mean_scores, x=mean_scores.index, y='sentiment_score', title=ticker + ' Daily Sentiment')
    return fig

# Call the functions
hourly_fig = plot_hourly_sentiment(df, ticker)
daily_fig = plot_daily_sentiment(df, ticker)

# Display the figures using Streamlit
st.plotly_chart(hourly_fig)
st.plotly_chart(daily_fig)


