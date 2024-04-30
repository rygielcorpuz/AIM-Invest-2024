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

def calculate_total_score(scale_score, multiple_choice_score):
    # Add the two scores together
    risk_score = scale_score + multiple_choice_score
    return risk_score

def main():
    st.markdown("***")
    st.markdown("***")
    title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>Risk Aversion Questionnaire</h1>"
    st.markdown(title_html, unsafe_allow_html=True)
    #st.title("Risk Aversion Questionnaire")
    
    # Questions
    questions = [
        "How comfortable are you with investing in high-risk, high-return assets such as stocks or cryptocurrencies?",
        "On a scale of 0 to 5, how willing are you to accept short-term fluctuations in the value of your investments?",
        "When considering investment options, which statement best reflects your attitude towards risk?",
        "What is your time horizon for investing in the stock market?",
        "In addition to whatever you own, you have been given $1,000. You are now asked to choose between: " 
    ]

    # Choices for multiple choice questions
    choices_q3 = [
        "a) I prefer investments with high potential returns, even if they come with a higher level of risk.",
        "b) I seek a balance between risk and return, willing to accept moderate fluctuations in exchange for reasonable gains.",
        "c) I prioritize preserving my initial investment over potential gains, opting for lower-risk options.",
        "d) I avoid investments altogether due to fear of losing money."
    ]

    choices_q4 = [
        "a) Short-term, I'm looking to make quick profits and capitalize on market movements.",
        "b) Medium-term, I aim to achieve financial goals within 5-10 years and willing to tolerate some fluctuations.",
        "c) Long-term, I'm investing for retirement or other distant financial objectives and can withstand market volatility.",
        "d) I have no specific time horizon and may need access to my funds at any moment."
    ]

    choices_q5 = [
        "a) A sure gain of $500",
        "b) A 50 percent chance to gain $1,000 and a 50 percent chance to gain nothing"
    ]

    # User responses
    user_responses = []

    # Initialize the total scores
    scale_total_score = 0
    multiple_choice_total_score = 0

    for i, question in enumerate(questions):
        if i < 2:
            response = st.slider(question, 0, 5, step=1)
            scale_total_score += response  # Add scale response to total score
        elif i == 2:
            response = st.radio(question, choices_q3)
            # Calculate multiple choice score for question 3
            if response.startswith("a)"):
                multiple_choice_total_score += 4
            elif response.startswith("b)"):
                multiple_choice_total_score += 3
            elif response.startswith("c)"):
                multiple_choice_total_score += 2
            elif response.startswith("d)"):
                multiple_choice_total_score += 1
        elif i == 3:
            response = st.radio(question, choices_q4)
            # Calculate multiple choice score for question 4
            if response.startswith("a)"):
                multiple_choice_total_score += 3
            elif response.startswith("b)"):
                multiple_choice_total_score += 2
            elif response.startswith("c)"):
                multiple_choice_total_score += 1
            elif response.startswith("d)"):
                multiple_choice_total_score += 0
        elif i == 4:
            response = st.radio(question, choices_q5)
            # Calculate multiple choice score for question 5
            if response.startswith("a)"):
                multiple_choice_total_score += 1
            elif response.startswith("b)"):
                multiple_choice_total_score += 0
        user_responses.append(response)

    st.write("Your responses:")
    for i, response in enumerate(user_responses):
        st.write(f"Question {i+1}: {response}")
    
    risk_score = calculate_total_score(scale_total_score, multiple_choice_total_score)
    st.write(f"Total score of risk aversion: {risk_score/4}")
    
if __name__ == "__main__":
    main()