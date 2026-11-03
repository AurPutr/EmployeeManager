import streamlit as st
import pandas as pd
import datetime
import plotly.express as px


st.title('Team Name') # team name should be printed automatically
st.title('Current Loop & Loop Period')
st.title('Avg. LOE score on ongoing loop')

df = pd.DataFrame([
    {"Employee": "Aurelija", "Task": "Onboarding",  "Start": "2026-11-01", "End": "2026-11-05"},
    {"Employee": "Jonas",    "Task": "Project A",   "Start": "2026-11-03", "End": "2026-11-20"},
    {"Employee": "Rūta",     "Task": "Vacation",    "Start": "2026-11-10", "End": "2026-11-17"},
])

fig = px.timeline(df, x_start="Start", x_end="End", y="Employee", color="Task")
fig.update_yaxes(autorange="reversed")  # first row at the top
st.plotly_chart(fig, use_container_width=True)

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
