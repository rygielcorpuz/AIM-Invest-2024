import streamlit as st
#for the background
def blur_image(image, radius):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius))
    return blurred_image

title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>Comic Stocks</h1>"
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
ticker = st.text_input("Enter Ticker Name")
st.write("Some common tickers:  \n- AMZN: Amazon  \n- AAPL: Apple  \n- GOOG: Google  \n- MSFT: Microsoft  \n- TSLA: Tesla")

run = st.button("Search")
if run:
    st.image('comicstocksreal.png', caption='The rise of Apple stock')
    st.write("ISSUE 1: 'DISOVERY'  We meet our protagonist, JASON, a young and ambitious investor, who has been following the tech industry for years. He's always been fascinated by the giants of Silicon Valley, but never thought he had the resources to invest in them. That is, until he stumbles upon an article about Apple Inc. and its revolutionary AI lab in Zurich.  Jason's curiosity is piqued, and he begins to dig deeper into Apple's world. He discovers the company's impressive track record, its innovative products, and its commitment to artificial intelligence. He's amazed by the potential of Apple's AI lab and its potential to enhance the iPhone's capabilities.  As Jason delves deeper into Apple's world, he starts to notice the stock's performance. He sees that it's been dipping before Amazon's earnings release, but he's not deterred. He believes in Apple's vision and decides to take a chance on the stock.  ISSUE 2: 'THE RISE'  Jason's gamble pays off, and Apple's stock begins to rise. He's thrilled to see his investment grow, and he becomes more confident in his decision. He starts to follow the news and analysis surrounding Apple, and he's encouraged by the positive sentiment.  As the days go by, Apple's stock continues to climb. Jason's friends and family start to take notice, and they begin to ask for his investment advice. He's happy to share his knowledge, and soon, he's known as the 'Apple whisperer' among his circle.  But Jason's not resting on his laurels. He's always on the lookout for new developments and news that could affect Apple's stock. He's aware of the competition from Huawei and Samsung, but he's convinced that Apple's innovative spirit will keep it ahead of the game.  ISSUE 3: 'THE CHALLENGE'  Just as Jason's investment is thriving, Apple's stock takes a hit. The company's China demand woes are overblown, according to some strategists, but Jason's not so sure. He starts to worry about the impact of Huawei's surging profits and the Western sanctions on Apple's sales.  As the news surrounding Apple's struggles intensifies, Jason's friends and family start to doubt his investment advice. They tell him that he's made a mistake, that Apple's best days are behind it. But Jason's not convinced. He believes in Apple's resilience and its ability to bounce back.  ISSUE 4: 'THE TURNAROUND'  Jason's faith in Apple is rewarded when the company's stock starts to rise again. He's vindicated, and his friends and family are impressed by his conviction. Apple's earnings report is better than expected, and the company's AI investment and iPhone sales are driving the growth.  As Apple's stock continues to soar, Jason becomes more confident in his investment skills. He starts to explore other tech stocks, looking for the next big opportunity. He's aware of the risks and challenges, but he's convinced that he can navigate the market and come out on top.  ISSUE 5: 'THE FUTURE'  Jason's investment portfolio is thriving, and he's known as a savvy investor among his peers. He's still bullish on Apple, and he's excited about the company's future plans. He's aware of the potential risks and challenges, but he's convinced that Apple's innovative spirit and commitment to AI will drive its growth.  As Jason looks to the future, he's excited about the possibilities. He's exploring new tech stocks, and he's convinced that he can find the next big winner. He's learned that investing in the stock market is a rollercoaster ride, but he's ready for the challenge.  The adventure continues...")