import streamlit as st
import base64

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
    background-image: url("https://img.freepik.com/free-photo/bamboo-leaf-elements-green_53876-95290.jpg");
    background-size: cover;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>About Us</h1>"

st.markdown(title_html, unsafe_allow_html=True)

# def sidebar_bg(side_bg):
#     side_bg_ext = 'gif'
#     st.markdown(
#         f"""
#         <style>
#         [data-testid="stSidebar"] > div:first-child {{
#             background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
#             }}
#         </style>
#         """,
#     unsafe_allow_html=True,
#     )
# side_bg = 'treegif.webp'
# sidebar_bg(side_bg)

st.write("Rygiel Corpuz: Our mentor!!")
left_co, cent_co, righ_co = st.columns(3)
with left_co:
    st.write("FRONTEND")
    st.write("Laura Sales")
    st.write("Kaia Sonoda")
with righ_co:
    st.write("BACKEND")
    st.write("Oudom Pach")
    st.write("Sammy Vrla")
    st.write("Aman Vishwanathan")
