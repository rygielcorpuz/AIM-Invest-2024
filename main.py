import streamlit as st
from datetime import date
from streamlit_option_menu import option_menu


import yfinance as yf 
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go #plotly is an interactive graph

START = "2015-01-01" #where data starts
TODAY = date.today().strftime("%Y-%m-%d") #all the way to today

#TITLE
import streamlit as st

# Define the HTML strings for the title and subtitle
title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>📉 Lost in Stocks 📈</h1>"
subtitle_html = "<h2 style='text-align: center; margin-top: -10px; margin-bottom: 20px; font-size: smaller;'>💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸</h2>"

#displaying it all
st.markdown(title_html, unsafe_allow_html=True)
st.markdown(subtitle_html, unsafe_allow_html=True)

################################################


ticker = st.text_input('Enter Ticker', 'TCKR')
sentAnal = st.text_input('Enter Sentiment Analysis', 'You are Either going to be Happy 😊 or Sad 😢' )
sex = st.select_slider("Choose Sex", ['male','female'])
istrategy = st.slider("Investment Strategy",0,1000)
startInvest = st.slider("Starting Investment",0,1000)
timeHorizon = st.slider("Time Horizon",0,1000)


subtitle_html = "<h2 style='text-align: center; margin-top: -10px; margin-bottom: 20px; font-size: smaller;'>💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸</h2>"
st.markdown(subtitle_html, unsafe_allow_html=True)


stocks = ("MSFT", "GOOG", "APPL", "GME")
selected_stock = st.selectbox("Select dataset for prediction", stocks)

n_years = st.slider("Years of prediction:", 1, 4)
period = n_years * 365

def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text("Load data...")
data = load_data(selected_stock)
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
