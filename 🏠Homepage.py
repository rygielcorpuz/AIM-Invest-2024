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

#tab name for fun
st.set_page_config(
    page_title="PandAI",
    page_icon=":bamboo:",
    initial_sidebar_state="collapsed"
)
# st.markdown(
#     """
# <style>
#     [data-testid="collapsedControl"] {
#         display: none
#     }
# </style>
# """,
#     unsafe_allow_html=True,
# )

# #'Are you Sober?' Page
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

        if st.session_state["authenticated"]:
            return True


#everything in the website should is down below 
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

    # DISPLAYING EVERYTHING
    title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>📉 🎋PandAI🎋 📈</h1>"

    st.markdown(title_html, unsafe_allow_html=True)

    st.page_link("🏠Homepage.py", label="Home", icon="🏠")
    st.page_link("pages/1_📂Model and Portfolio.py", label="Model/Portfolio", icon="📂")
    st.page_link("pages/2_🔍Stock Search.py", label="Stock Search", icon="🔍")
    st.page_link("pages/3_📅Calendar.py", label="Calendar", icon="📅")
    st.page_link("pages/4_👤About Us.py", label="About Us", icon="👤")

    #Description
    st.write("Welcome to PandAI, your virtual stock prediction application. Are you new to the stock market? Do you find yourself lost in the stocks? We here at PandAI have analyzed massive amounts of stock data in order to help make beginners like you. Simply press the Get Started button below, and we will lead you to our features.")
    st.write("1. Model and Portfolio: After answering some questions about your investment goals, we will give you a score and generate a portfolio of stocks that align with your best interests.")
    st.write("2. Stock Search: Enter the ticker for your desired company. We will sift through the most recent news articles relating to its stocks, summarize them, then give each a score based on its tone.")
    st.write("3. Calendar: idk ask sammy")

    #Get Started Button
    result = st.button("Get Started") 
    if result: #ideally opens up four new pages (3 features + about us)
        st.switch_page("pages/1_Model and Portfolio.py")

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
    from PIL import Image
    img=Image.open('pandai_logo.png')
    left_co, cent_co,last_co = st.columns(3)
    with cent_co:
        st.image(img)
        autoplay_audio("natureMusic.mp3")
#Calendar Description:
#The calendar shows th user when the market opens and closers and they can type in whatever ticker to look up the earnings call dates

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