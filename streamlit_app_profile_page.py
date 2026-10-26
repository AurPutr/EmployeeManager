import streamlit as st
import pandas as pd
import datetime


st.title('Name Surname') #name surname should be printed automatically
st.title('Team Name') #same as with name surname
st.title('Current Loop & Loop Period')
# ----------------------------------------------------
# TABS
# ----------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Overall Results",
        "Evaluation Shadowing",
        "Coaching Shadowing",
        "Agent Quality Improvement",
        "Efficiency Monitoring",
        "Tests",
        "Ticket Solving"
    ]
)
# ----------------------------------------------------
# TAB 4 - AGENT QUALITY IMPROVEMENT
# ----------------------------------------------------
with tab4:
    st.header("Agent Quality Improvement")
    if 'duomenys_q_imp' not in st.session_state:
        st.session_state.duomenys_q_imp = pd.DataFrame(columns=[
            "Agent ID ", "Quality Score Baseline", "Quality Score Final", "Difference",
            "Score"
    ])
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Add New Results")
        # Naudojame formą, kad puslapis nepersikrautų kaskart keičiant vieną laukelį
        with st.form("ivesties_forma", clear_on_submit=True):
            agent_id = st.number_input("Agent ID:")
            q_score_baseline = st.number_input("Quality Score Baseline:", min_value=0, max_value=100)
            q_score_final = st.number_input("Quality Score Final:", min_value=0, max_value=100)
            difference = st.number_input("Difference:", value= q_score_final - q_score_baseline)
            score = st.number_input("Score:", )


            submit = st.form_submit_button("Submit Data")

            # Kai paspaudžiamas mygtukas, pridedame duomenis
            if submit:
                if agent_id == "":
                    st.error("Please enter agent ID")
                else:
                    # Sukuriame naują eilutę
                    new_line = pd.DataFrame([{
                        "Agent ID": agent_id,
                        "Quality Score Baseline": q_score_baseline,
                        "Quality Score Final": q_score_final,
                        "Difference": difference,
                        "Score": score
                    }])
                    # Sujungiame esamus duomenis su nauja eilute
                    st.session_state.duomenys_q_imp = pd.concat([st.session_state.duomenys_q_imp, new_line], ignore_index=True)
                    st.success(f"Data was successfully added to the table!")

    with col2:
        st.subheader("Data Table")

        # 2. Atvaizduojame interaktyvią lentelę naudojant st.data_editor
        # num_rows="dynamic" leidžia pačioje lentelėje pridėti/trinti eilutes
        updated_data_eff = st.data_editor(
            st.session_state.duomenys_q_imp,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="editor_quality_improvement" #not sure why I need to do this
        )
    text = st.text_area("Enter employee feedback:")

# ----------------------------------------------------
# TAB 5 - EFFICIENCY MONITORING
# ----------------------------------------------------
with tab5:
    st.header("Efficiency Monitoring")
    if 'duomenys_eff_mon' not in st.session_state:
        st.session_state.duomenys_eff_mon = pd.DataFrame(columns=[
            "Year ", "Month", "Avg. Evaluation Time", "Points"
    ])
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Add New Results")
        # Naudojame formą, kad puslapis nepersikrautų kaskart keičiant vieną laukelį
        with st.form("ivesties_forma_efficiency", clear_on_submit=True):
            year = st.number_input("Year:", min_value=2024, max_value=2050)
            month = st.selectbox("Month:",("January", "February", "March", "April", "May",
                                           "June", "July", "August", "September", "October", "November", "December"))
            avg_eval_time = st.number_input("Avg. Evaluation Time:", min_value=0, max_value=500)
            points = st.number_input("Points:", min_value=0, max_value=10)

            submit = st.form_submit_button("Submit Data")

            # Kai paspaudžiamas mygtukas, pridedame duomenis
            if submit:
                if year and month == "":
                    st.error("Data from this period already exists!")
                else:
                    # Sukuriame naują eilutę
                    new_line = pd.DataFrame([{
                        "Year": year,
                        "Month": month,
                        "Avg. Evaluation Time": avg_eval_time,
                        "Points": points
                    }])
                    # Sujungiame esamus duomenis su nauja eilute
                    st.session_state.duomenys_eff_mon = pd.concat([st.session_state.duomenys_eff_mon, new_line], ignore_index=True)
                    st.success(f"Data was successfully added to the table!")

    with col2:
        st.subheader("Data Table")

        # 2. Atvaizduojame interaktyvią lentelę naudojant st.data_editor
        # num_rows="dynamic" leidžia pačioje lentelėje pridėti/trinti eilutes
        updated_data_eff = st.data_editor(
            st.session_state.duomenys_eff_mon,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            key="editor_efficiency"
        )
    # text = st.text_area("Enter employee feedback:")
