
import streamlit as st

def calculate_total_score(scale_score, multiple_choice_score):
    # Add the two scores together
    risk_score = scale_score + multiple_choice_score
    return risk_score

def score():
    st.title("Risk Aversion Questionnaire")
    
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
                multiple_choice_total_score += 0
        elif i == 3:
            response = st.radio(question, choices_q4)
            # Calculate multiple choice score for question 4
            if response.startswith("a)"):
                multiple_choice_total_score += 4
            elif response.startswith("b)"):
                multiple_choice_total_score += 3
            elif response.startswith("c)"):
                multiple_choice_total_score += 2
            elif response.startswith("d)"):
                multiple_choice_total_score += 0
        elif i == 4:
            response = st.radio(question, choices_q5)
            # Calculate multiple choice score for question 5
            if response.startswith("a)"):
                multiple_choice_total_score += 2
            elif response.startswith("b)"):
                multiple_choice_total_score += 0
        user_responses.append(response)

    st.write("Your responses:")
    for i, response in enumerate(user_responses):
        st.write(f"Question {i+1}: {response}")
    
    risk_score = calculate_total_score(scale_total_score, multiple_choice_total_score)
    st.write(f"Total score of risk aversion: {risk_score/4}")
    return risk_score/4


import streamlit as st
import pandas as pd
import plotly.express as px

# Read the CSV file into a DataFrame
df_csv = pd.read_csv('Risk_Score1.csv')

# Define your asset classes and their corresponding allocations
asset_classes = [
    'Communication Services', 'Consumer Discretionary', 'Consumer Staples',
    'Energy', 'Financials', 'Health Care', 'Industrials', 'Information Technology',
    'Materials', 'Real Estate', 'Utilities'
]


# Set the risk score for testing
number = score()

#round to the nearest score in csv
score_in_csv=[0, 1.5, 2.5, 3, 4.5, 5]


def round_to_nearest_in_list(number, score_in_csv):
  # Sort the list of numbers in ascending order.
  score_in_csv.sort()

  # Find the index of the closest number in the list to the given number.
  closest_number_index = 0
  for i, list_number in enumerate(score_in_csv):
    if abs(number - list_number) < abs(number - score_in_csv[closest_number_index]):
      closest_number_index = i

  # Return the closest number in the list.
  return score_in_csv[closest_number_index]

risk_score = round_to_nearest_in_list(number, score_in_csv)

# Find the row corresponding to the selected risk score
row = df_csv[df_csv['Risk Score'] == risk_score]

# Extract columns C to M (index 2 to 13) from the selected row
selected_data = row.iloc[:, 2:14].values.tolist()[0]

# Replace allocations with the selected data
allocations = selected_data

# Filter out negative allocations and their corresponding asset classes
positive_allocations = []
positive_asset_classes = []
negative_asset_classes = []

for asset, alloc in zip(asset_classes, allocations):
    if alloc >= 0:
        positive_asset_classes.append(asset)
        positive_allocations.append(alloc)

# Create a DataFrame for positive allocations
df = pd.DataFrame({'Asset Class': positive_asset_classes, 'Allocation': positive_allocations})

# Plotting the pie chart for positive allocations
fig = px.pie(df, values='Allocation', names='Asset Class', title='Portfolio Allocations (Positive Allocations Only)',
             color_discrete_sequence=px.colors.qualitative.Set3)
fig.update_traces(textposition='inside', textinfo='percent+label')

# Display the plot using Streamlit
st.plotly_chart(fig)
