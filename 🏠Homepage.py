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

st.markdown(page_bg_img, unsafe_allow_html=True)
# https://static.vecteezy.com/system/resources/thumbnails/002/623/469/small_2x/bamboo-background-grove-of-bamboo-stems-and-leaves-banner-copy-space-environmental-illustration-in-a-realistic-style-vector.jpg
# https://img.freepik.com/free-photo/bamboo-leaf-elements-green_53876-95290.jpg



# # <style>
# #     [data-testid="collapsedControl"] {
# #         display: none
# #     }
# # </style>
# # """,
# #     unsafe_allow_html=True,
# # )

# # #'Are you Sober?' Page
# def creds_entered():
#     if st.session_state["user"].strip() == "yes": #and st.session_state["passwd"].strip() == "admin":
#         st.session_state["authenticated"] = True
#     else:
#         st.session_state["authenticated"] = False
#         if not st.session_state["user"]:
#             st.warning("Are you sober? (type yes or no)")
#         else:
#             st.error("Invalid state, come back later :face_with_raised_eyebrow:")
#             webbrowser.open_new_tab('https://www.summitdetox.com/blog/the-stock-market-and-your-drinking/')


# def authenticate_user():
#     if "authenticated" not in st.session_state:
#         st.text_input(label="Are you sober?", value="", key="user", on_change=creds_entered)
#         return False
#     else:
#         if st.session_state["authenticated"]:
#             return True
#         else:
#             st.text_input(label="Are you sober?", value="", key="user", on_change=creds_entered)
#             return False

#         if st.session_state["authenticated"]:
#             return True

# if authenticate_user():
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
    

# no more money rain :((
# st.markdown(title_html, unsafe_allow_html=True)
# #for money to fall lolol
# rain(
#     emoji="💸",
#     font_size=20,
#     falling_speed=15,
#     animation_length="infinite",
# )




selected = option_menu(
    menu_title=None,
    options=["Home","Model & Portfolio", "Stock Search","Comic Stocks", "Calendar","ChatBot"],
    orientation="horizontal",
)

if selected == "Home":
    st.page_link("🏠Homepage.py")

if selected == "Model & Portfolio":
    st.switch_page("pages/1_📂Model and Portfolio.py")

if selected == "Stock Search":
    st.switch_page("pages/2_🔍Stock Search.py")

if selected == "Comic Stocks":
    st.switch_page("pages/3_🦸‍♀️Comic_Stocks.py")

if selected == "Calendar":
    st.switch_page("pages/4_📅Calendar.py")

if selected == "ChatBot":
    st.switch_page("pages/5_🐼ChatBot.py")

# if selected == "About Us":
#     st.switch_page("pages/6_👤About Us.py")

# line
st.markdown("<hr style='border-top: 2px solid green;'>", unsafe_allow_html=True)
#Description
st.write("Welcome to PandAI! Your virtual stock prediction web application. Are you new to the stock market? Do you find yourself lost in the stocks? We here at PandAI have analyzed massive amounts of stock data to help beginners like you. Press the 'Get Started' button below to learn how to save some big-time money!")
#Get Started Button
result = st.button("Get Started!")



if result:  # ideally opens up four new pages (3 features + about us)
    st.switch_page("pages/1_📂Model and Portfolio.py")

st.write("Confused? Learn more here about each feature!")
with st.expander("📂 Model and Portfolio"):
    st.write("After answering some questions about your investment goals, we will give you a score based on whether or not the article was positive and generate a portfolio of stocks that align with your best interests.")
with st.expander("🔍 Stock Search"):
    st.write("Enter the ticker for your desired company. We will review the most recent news articles relating to its stocks, summarize them, and then give each a score based on how the article sounds.")
with st.expander("🦸‍♀️ Comic_Stocks"):
    st.write("ccsefgesf")
with st.expander("📅 Calendar"):
    st.write("The calendar shows the user when the market opens and closes, and they can type in whatever ticker to look up the earnings call dates.")
with st.expander("🐼 ChatBot"):
    st.write("sefsefsefes")

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
#Calendar Description:
#The calendar shows th user when the market opens and closers and they can type in whatever ticker to look up the earnings call dates