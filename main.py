import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs #important for data scraping
import pandas as pd #helps w/ data manipulation
import re
import requests # helps send & receive response from web browswer
import plotly.express as px
import json # for graph plotting in website
# NLTK VADER for sentiment analysis
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import yfinance as yf 
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go #plotly is an interactive graph

import webbrowser
import base64

#tab name for fun
st.set_page_config(
    page_title="Lost in Stocks",
    page_icon= ":chart_with_upwards_trend:"
)

def creds_entered():
    if st.session_state["user"].strip() == "yes": #and st.session_state["passwd"].strip() == "admin":
        st.session_state["authenticated"] = True
    else:
        st.session_state["authenticated"] = False
        if not st.session_state["user"]:
            st.warning("Are you sober? (type yes or no)")
        else:
            st.error("Invalid state, come back later :face_with_raised_eyebrow:")
            webbrowser.open_new_tab('https://www.summitdetox.com/blog/the-stock-market-and-your-drinking/')


def authenticate_user():
    if "authenticated" not in st.session_state:
        st.text_input(label="Are you sober?", value="", key="user", on_change=creds_entered)
        return False
    else:
        if st.session_state["authenticated"]:
            return True
        else:
            st.text_input(label="Are you sober?", value="", key="user", on_change=creds_entered)
            return False


        #st.text_input(label="Password :", value="", key="passwd", type="password", on_change=creds_entered)
#        return False
#    else:
        if st.session_state["authenticated"]:
            return True
#        else:
   
            #st.text_input(label="Are you sober?", value="", key="yes", on_change=creds_entered)
            #st.text_input(label="Password :", value=" ", key="passwd", type="password", on_change=creds_entered)
            #return False

if authenticate_user():
    def sidebar_bg(side_bg):
        side_bg_ext = 'gif'
        st.markdown(
            f"""
            <style>
            [data-testid="stSidebar"] > div:first-child {{
                background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
                }}
            </style>
            """,
        unsafe_allow_html=True,
        )
    side_bg = 'treegif.webp'
    sidebar_bg(side_bg)

    START = "2015-01-01" #where data starts
    TODAY = datetime.today().strftime("%Y-%m-%d") #all the way to today

    

    # Define the HTML strings for the title and subtitle
    title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>📉 Lost in Stocks 📈</h1>"
    subtitle_html = "<h2 style='text-align: center; margin-top: -10px; margin-bottom: 20px; font-size: smaller;'>💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸</h2>"

    #displaying it all
    st.markdown(title_html, unsafe_allow_html=True)
    st.markdown(subtitle_html, unsafe_allow_html=True)

    ################################################

    #ticker = st.text_input("Enter Ticker Name", "AAPL")
    sentAnal = st.text_input('Enter Sentiment Analysis', 'You are Either going to be Happy 😊 or Sad 😢' )
    ticker = st.text_input('Enter desired stock ticker for prediction', 'AAPL')
    istrategy = st.slider("Investment Strategy",0,1000)
    startInvest = st.slider("Starting Investment",0,1000)
    timeHorizon = st.slider("Time Horizon",0,1000)


    subtitle_html = "<h2 style='text-align: center; margin-top: -10px; margin-bottom: 20px; font-size: smaller;'>💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸</h2>"
    st.markdown(subtitle_html, unsafe_allow_html=True)


    #stocks = ("MSFT", "GOOG", "AAPL", "GME")
    #ticker = st.selectbox("Select dataset for prediction", stocks)

    n_years = st.slider("Years of prediction:", 1, 4)
    period = n_years * 365

    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text("Load data...")
    data = load_data(ticker)
    data_load_state.text("Loading data...done!")

    st.subheader('Raw data')
    st.write(data.tail())

    # Plot raw data
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
        
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)


    #creating the vertical/horizontal menu bars
    #making a side bar menu
    with st.sidebar:#so the menu bar wont automatically pop 
        selected = option_menu(
            menu_title =None, #required or put "Main Menu" here
            options=["Home", "Projects", "Contact", "Calendar"], #required
            icons=["house", "book", "envelope", "calendar"], #optional
            menu_icon="cast", #optional - icon for menu title
            default_index=0, #optional - when u open the website, where default it will open, so 'Home' will be selected first
            orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color":"peach"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "25px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "pink"},
            },
        )

    #############################################################################################################################################
    #2 Horizontal Menu
    #selected = option_menu(
    #        menu_title =None, #required or put "Main Menu" here
    #        options=["Home", "Projects", "Contact"], #required
    #        icons=["house", "book", "envelope"], #optional
    #        menu_icon="cast", #optional - icon for menu title
    #        default_index=0, #optional - when u open the website, where default it will open, so 'Home' will be selected first
    #        orientation="horizontal",
    #        styles={
    #            "container": {"padding": "0!important", "background-color":"peach"},
    #            "icon": {"color": "orange", "font-size": "25px"},
    #            "nav-link": {
    #                "font-size": "25px",
    #                "text-align": "left",
    #                "margin": "0px",
    #                "--hover-color": "#eee",
    #            },
    #            "nav-link-selected": {"background-color": "green"},
    #        },
    #    )

    if selected == "Home":
        st.title(f"You have selected {selected}")
    if selected == "Projects":
        st.title(f"You have selected {selected}")
    if selected == "Contact":
        st.title(f"You have selected {selected}")

    #future logo
    from PIL import Image
    img=Image.open('logo_placeholder.png')

    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(img)


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

        pass



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
            df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='mixed')

            #df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], infer_datetime_format=True)



            #df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
        # Returns:
        #   parsed_news_df (df): Parsed news data with columns: date, time, headline, datetime
        return df



    nltk.download('vader_lexicon') #downloads it
    sid = SentimentIntensityAnalyzer()

    def score_news(parsed_news_df):
        # Score news headlines sentiment using VADER sentiment analysis
        # Parameters:
        #   parsed_news_df (DataFrame): Parsed news data with columns: date, time, headline, datetime
        # Returns:
        #   parsed_and_scored_news (DataFrame): News data with sentiment scores added


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

    # Example usage:
    # parsed_news_df is assumed to be the DataFrame obtained after parsing news articles
    # scored_news_df = score_news(parsed_news_df)
        pass


    # ticker = "AAPL"
    # news = get_news(ticker)
    # print(news.prettify())
    # parse_news(get_news('AAPL'))
    # parse_news(news)
    # score_news(get_news('APPL'))
    # score_news(news)
    tableNews = get_news(ticker)
    print(tableNews)
    parseNews = parse_news(tableNews)
    print(parseNews)
    df = score_news(parseNews)
    #df.to_csv("dff.csv", index=False)
    print(df)
    st.dataframe(df)

    # turn headlines into csv
    df.drop(['neg', 'neu', 'pos', 'compound'], axis=1, inplace=True)
    df.to_csv("headlines.csv", index=False)

