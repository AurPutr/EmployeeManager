import streamlit as st
import pandas as pd
import datetime


st.title('Team Name') # team name should be printed automatically
st.title('Current Loop & Loop Period')
# ----------------------------------------------------
# TABS
# ----------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "Team List",
        "Team Results",
        "Coaching Shadowing"
    ]
)
#here would be great to have tables with team data