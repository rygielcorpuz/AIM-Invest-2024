import streamlit as st

def calculate_total_score(scale_score, multiple_choice_score):
    # Add the two scores together
    risk_score = scale_score + multiple_choice_score
    return risk_score

def main():
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
    
if __name__ == "__main__":
    main()
