import streamlit as st
import base64

from PIL import Image

title_html = "<h1 style='text-align: center; font-family: Times New Roman;'>About Us</h1>"

st.markdown(title_html, unsafe_allow_html=True)

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

st.write("💪R Y G I E L💪")