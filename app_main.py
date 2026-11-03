import streamlit as st


st.set_page_config(
    page_title="QD Team DataBase",
    layout="wide",
)
pg = st.navigation(
    [
        st.Page("views/streamlit_app_main_page.py", title="Home page"),
        st.Page("views/streamlit_app.py", title=":heavy_plus_sign: Add new employee"),
        st.Page("views/streamlit_app_shadowing.py", title=":heavy_plus_sign: Add new shadowing"),
        st.Page("views/streamlit_app_profile_page.py", title="Profile Page"),
        st.Page("views/streamlit_app_team_page.py", title="Team Page"),
    ]
)
pg.run()