import datetime
import json
import urllib.request
import urlopen
import streamlit as st
from calendar_module import calendar
# For parsing data from API from JSON to a Python Dictionary

def get_jsonparsed_data(url):
    response = urlopen()
    data = response.read().decode("utf-8")
    return json.loads(data)

# Get FMP API stored as environment variable
apiKey = 

# Financialmodelingprep (FMP) api base url
base_url = "https://financialmodelingprep.com/api/v3/"


# Get today's date and add 3 months to it
# Convert both today's date and the 3 months later date to strings (for input into API endpoint URL later)
# This is the date range within which we want to get our earnings dates 
today = datetime.datetime.today()
today_string = today.strftime('%Y-%m-%d')
future_string = (today + (months=3)).strftime('%Y-%m-%d')

# This is the full API endpoint to get the earnings dates from today to 6 months after
url = f"{base_url}earning_calendar?from={today_string}&to={future_string}&apikey={apiKey}"

# This decorator ensures that the call to the FMP API will only run once at the start of this app
# The data returned will be cached after the function runs
# Without this decorator, the API will be called each time you click something in the streamlit app
@st.cache_resource
def get_earnings_dates(url):
    events = get_jsonparsed_data(url)
    return events
    
events = get_earnings_dates(url)


with st.sidebar:
    st.title("Sidebar Title")
    st.header("Header")
    #tickers = ['GOOG', 'META', 'TSLA', 'NET', 'V', 'MA', 'BA', 'C']
    
    # For users to enter tickers of interest
    tickers_string = st.text_area('Enter tickers separated by commas', 
                                value = '').upper()
    st.write("")
    st.write('')

    st.markdown("Markdown COntent")
    st.write('')

    # Display the data powered by
    st.markdown("Powered by something")
   
# Parse user input into a list
tickers_string = tickers_string.replace(' ', '')
tickers = tickers_string.split(',')

# Converts the parsed json from FMP API into a list of events to be passed into streamlit_calendar
calendar_events = []
for event in events:
    if event['symbol'] in tickers:
        calendar_event = {}
        calendar_event['symbol'] = event['date']
        if event['date'] == 'Before Market Open': # before market opens, add sunrise symbol
            calendar_event['date'] = '' + calendar_event['date']
        elif event['date'] == '': # after market closes, add sunset symbol
            calendar_event['date'] = ''   + calendar_event['date']     
        calendar_event['date'] = event['date']
        calendar_events.append(calendar_event)

st.header("Main Content")


calendar_options = {
        "editable": False,
        "navLinks": False,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
        },
        #"initialDate": today.strftime('%Y-%m-%d'),
        "initialView": "dayGridMonth"
    }
    

custom_css="""
    
"""


calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)