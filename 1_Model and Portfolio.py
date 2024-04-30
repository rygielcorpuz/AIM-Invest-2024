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
import json
import requests
nltk.downloader.download('vader_lexicon')
from datetime import datetime
from streamlit_option_menu import option_menu
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as bs #important for data scraping
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go #plotly is an interactive graph
from streamlit_lottie import st_lottie


title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>Model/Portfolio</h1>"
st.markdown(title_html, unsafe_allow_html=True)

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

# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_url_breathe = "https://app.lottiefiles.com/share/33281adf-24e7-43e9-b203-1651abfba346"
# lottie_breathe = load_lottieurl(lottie_url_breathe)
# st_lottie(lottie_breathe, key="hello")

# st_lottie(
#     lottie_breathe,
#     speed=.5,
#     reverse=False,
#     loop=True,
#     quality="medium",
#     renderer="svg",
#     height=None,
#     width=None,
#     key=None,
# )
# st_lottie(lottie_breathe, key="hello")

file_ = open("breathe.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()


l_co, lc_co, c_co, cc_co, ccc_co, c_co, r_co = st.columns(7)
with c_co, cc_co:
    st.write("R E L A X")

    
one_co, two_co, three_co, four_co, five_co, six_co, seven_co = st.columns(7)
with three_co:
    autoplay_audio("natureMusic.mp3")
with two_co:
    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
        unsafe_allow_html=True,
    )
