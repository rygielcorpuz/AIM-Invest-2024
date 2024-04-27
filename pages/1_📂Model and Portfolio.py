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

title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>Model/Portfolio</h1>"
st.markdown(title_html, unsafe_allow_html=True)

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
