
import streamlit as st

def apply_custom_styles():
    # Only call Streamlit functions inside this function
    st.markdown("""
        <style>
        .stApp {
            background-color: #3D8D7A;
            color : #FBFFE4;
        }
        .stSidebar {
            background-color: #FBFFE4;
            color: #3D8D7A;
        }
        .stButton>button {
            background-color: #3D8D7A;
            color: #FBFFE4;
            border-radius: 5px;
            width: 170px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #FBFFE4;
            color: #3D8D7A;
            border-color: #3D8D7A;
            transition: background-color 0.3s ease;
        }

        .stTextInput>div>div>input {
            background-color: #FBFFE4;
            color: black;
        }

        .stSelectbox>div>div>input {
            background-color: #B3D8A8;
            color: black;
        }

        .metric-container {
            background-color: #B3D8A8;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }

        .map-container {
            border: 1px solid #1B4079;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }

        h1, h2, h3 {
            color: #FBFFE4;
        }
        .stDataFrame>dataframe {
            background-color: #B3D8A8;
        }
        .stSubheader {
            color: #FBFFE4;
            bacground-color: #B3D8A8;
        }
        .stTextInput>div>div>input{
            background-color: #FBFFE4;
        }
        </style>
    """, unsafe_allow_html=True)
