import streamlit as st
import pandas as pd
import datetime



#Add New Employee page
st.header('Add New Employee')
name = st.text_input("Name:")
surname = st.text_input("Surname:")
tt_id = st.text_input("Ticketron ID:")
team = st.selectbox(
    "Team",
    ("EN TN TWW", "FR TN TWW", "ECC EN TN TWW", "ECC FR TN TWW", "HVV TN TWW",
     "EN EG TWW", "EN EG TP", "US/AU EG TP", "ECC EG TP", "EN KE TP", "US/AU KE TP",
     "EN ZA TP", "EN UA HW", "ECC UA HW", "EN PH HW", "FR TN OS", "FR MA OS")
) #same as with position field
position = st.selectbox(
    "Position",
    ("Trainer", "QA")
) #is it possible do not have a default value?
email = st.text_input("Email address:")
start_date = st.date_input("Joining date", datetime.date.today())
end_date = st.date_input("Leaving date", datetime.date.today())
#end_date field shouldn't be mandatory
status = st.checkbox("Active Employee")

#st.session_state.duomenys = pd.concat

# we need to add submit button and
