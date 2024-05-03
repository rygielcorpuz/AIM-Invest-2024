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
import random
nltk.downloader.download('vader_lexicon')
from datetime import datetime
from streamlit_option_menu import option_menu
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs #important for data scraping
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go #plotly is an interactive graph
from streamlit_extras.let_it_rain import rain 
from streamlit_extras.colored_header import colored_header
from PIL import Image

#tab name for fun
st.set_page_config(
    page_title="PandAI",
    page_icon=":bamboo:",
    initial_sidebar_state="collapsed"
)


#for the background
def blur_image(image, radius):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
    return blurred_image
    
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.pixers.pics/pho_wat(s3:700/FO/66/66/62/03/700_FO66666203_6564ae5dc24ef5df1744e193f60e554f.jpg,700,700,cms:2018/10/5bd1b6b8d04b8_220x50-watermark.png,over,480,650,jpg)/stickers-bamboo-background.jpg.");
    background-color: rgba(255, 255, 255, 0.38); 
    background-blend-mode: lighten; 
    background-size: 150%; /* Increase this value to zoom in */
    background-repeat: no-repeat; /* Add this to prevent image repeat */
    background-position: center; /* Center the image in the view */
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


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


# DISPLAYING EVERYTHING
#title
title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>📉 🎋PandAI🎋 📈</h1>"
img = Image.open('pandai_logo2.png')
left_co, lc_co, lcc_co, cent_co, rcc_co, rc_co, last_co = st.columns(7)
with lc_co:
    st.image(img, width=500)
    

selected = option_menu(
    menu_title=None,
    options=["Home","Portfolio Optimizer", "Stock Search","Comic Stocks", "Calendar","Virtual Assistant"],
    orientation="horizontal",
)

if selected == "Home":
    st.page_link("🏠Homepage.py")

if selected == "Model & Portfolio":
    st.switch_page("pages/1_📂Portfolio_Optimizer.py")

if selected == "Stock Search":
    st.switch_page("pages/2_🔍Stock Search.py")

if selected == "Comic Stocks":
    st.switch_page("pages/3_🦸‍♀️Comic_Stocks.py")

if selected == "Calendar":
    st.switch_page("pages/4_📅Calendar.py")

if selected == "Virtual Assistant":
    st.switch_page("pages/5_🐼ChatBot.py")

# line
st.markdown("<hr style='border-top: 2px solid green;'>", unsafe_allow_html=True)
#Description
st.write("Welcome to PandAI! Your virtual stock prediction web application. Are you new to the stock market? Do you find yourself lost in the stocks? We here at PandAI have analyzed massive amounts of stock data to help beginners like you. Press the 'Get Started' button below to learn how to save some big-time money!")
#Get Started Button
result = st.button("Get Started!")



if result:  # ideally opens up four new pages (3 features + about us)
    st.switch_page("pages/1_📂Portfolio_Optimizer.py")

st.write("Confused? Learn more here about each feature!")
with st.expander("📂 Portfolio Optimizer"):
    st.write("After answering some questions about your investment goals, we will give you a score based on whether or not the article was positive and generate a portfolio of stocks that align with your best interests.")
with st.expander("🔍 Stock Search"):
    st.write("Enter the ticker for your desired company. We will review the most recent news articles relating to its stocks, summarize them, and then give each a score based on how the article sounds.")
with st.expander("🦸‍♀️ Comic Stocks"):
    st.write("Analyzes the sentiment of an article and creatively transforms it into a child-friendly comic story, making it easier for users to understand and enjoy.")
with st.expander("📅 Calendar"):
    st.write("The calendar shows the user when the market opens and closes, and they can type in whatever ticker to look up the earnings call dates.")
with st.expander("🐼 Virtual Assistant"):
    st.write("Meet Po, your dedicated personal assistant panda who is ready to answer any questions you have about the website.")

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
    
#future logo
img=Image.open('pandai_logo2.png')
left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image(img)
    autoplay_audio("natureMusic.mp3")
