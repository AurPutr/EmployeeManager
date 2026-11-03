import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime


#add new shadowing
st.header('New Shadowing Session')
shadowing_type = st.selectbox(label="Shadowing Type", options=["Trainer Shadowing Session",
                "Ticket Evaluation Shadowing Session","Coaching Shadowing Session"],
                index=None,
                placeholder="Choose a type of shadowing session...")
name = st.text_input("Name:")
surname = st.text_input("Surname:")
team = st.selectbox(
    "Team",
    ("EN TN TWW", "FR TN TWW", "ECC EN TN TWW", "ECC FR TN TWW", "HVV TN TWW",
     "EN EG TWW", "EN EG TP", "US/AU EG TP", "ECC EG TP", "EN KE TP", "US/AU KE TP",
     "EN ZA TP", "EN UA HW", "ECC UA HW", "EN PH HW", "FR TN OS", "FR MA OS")
) #same as with position field
session_date = st.date_input("Session Date", datetime.date.today())

ticket_evaluation = {
    "Investigation Part": [
        "1. Translating messages/relevant proofs when not in EN",
        "2. Reviewing proofs",
        "3. Reviewing previous answers",
        "4. Reviewing other tickets related with the same issue",
        "5. Related information in message (name, amount, etc.) is correct",
        "6. Checking tags, statuses, re-opens and internal notes",
        "7. Reviewing notices sent",
        "8. Reviewing templates sent",
        "9. Reviewing member's profile (suspiciousness)",
        "10. Reviewing member's profile (comments)",
        "11. Conversation between members",
        "12. Shipping events and statuses",
        "13. Reviewing external tracking system of shipping provider",
    ],
    "Evaluation Quality Part": [
        "1. Quickly identifying the process/contact reason",
        "2. Checking compensation reason and amount",
        "3. Leaving clear and detailed feedback for agents",
        "4. Registering noticed mistakes",
    ],
    "Tool Navigation Part": [
        "1. Scoring Book usage and navigation",
        "2. Vinted Knowledge usage and navigation",
        "3. Navigation on Ticketron",
        "4. Navigation on Quality Tool",
        "5. Navigation in Vinted Product tools",
    ],
}

coaching_evaluation = {
    "Opening": [
        "1. Clearly states the session purpose",
        "2. Presents structure and agenda of the meeting "
    ],
    "Context (COIN)": [
        "3. References specific Ticket ID, date, and other relevant information"
    ],
    "Observation (COIN)": [
        "4. Describes the issue using clear facts - what mistakes were identified",
        "5. Uses specific process maps, articles, scoring book, etc."
    ],
    "Impact (COIN)": [
        "6. Clearly defines or asks the agent to identify the core member issue during the discussion",
        "7. Asks to explain how the mistake then impacted the member or resolution"
    ],
    "Engagement": [
        "8. Coach leads an open discussion by asking open-ended reflection question "
        "(e.g., What was your approach here?) before suggesting solutions.",
        "9. Encourages the agent to explain why a specific approach was chosen "
        "and to consider what the correct way would be"
    ],
    "Root Cause": [
        "10. Clearly defines the root cause of the issues and discusses it with the agent "
        "(Knowledge, Skill, Behavior, Process, Communication)"
    ],
    "Next Steps": [
        "11. Coach agrees with the agent on specific next steps for the improvement",
        "12. Agrees a numeric target to reach and clear deadlines"
    ]
}

def ticket_score(result):
    """Returns the score for one ticket (0–100), or None if it can't be scored yet."""
    answers = [
        answer
        for criteria in ticket_evaluation
        for answer in result[criteria].values()
    ]
    yes = answers.count("Yes")
    no = answers.count("No")
    if yes + no == 0:
        return None
    return yes / (yes + no) * 100
def ticket_evaluation_form(ticket_no):
    """Draws the full evaluation form for one ticket and returns the answers."""
    result = {}
    result["ticket"] = st.text_input(
        "Please insert ticket ID or link of the ticket:",
        key=f"t{ticket_no}_link",
    )
    st.subheader("Evaluation Criteria:")

    for s, (section, criteria) in enumerate(ticket_evaluation.items()):
        st.subheader(f"{section}:")
        answers = {}
        for i, criterion in enumerate(criteria):
            answers[criterion] = st.radio(
                criterion,
                ["Yes", "No", "N/A"],
                index=None,
                horizontal=True,
                key=f"t{ticket_no}_s{s}_c{i}",   # e.g. t2_s0_c5
            )
        result[section] = answers

    result["comments"] = st.text_area(
        "Enter comments about this ticket:",
        key=f"t{ticket_no}_comments",
    )
    return result


if shadowing_type == "Ticket Evaluation Shadowing Session":
    tabs = st.tabs(["Ticket 1", "Ticket 2", "Ticket 3"])
    all_tickets = {}
    for n, tab in enumerate(tabs, start=1):
        with tab:
            all_tickets[n] = ticket_evaluation_form(n)

            st.subheader("Shadowing Score")

    scores = {n: ticket_score(t) for n, t in all_tickets.items()}

    cols = st.columns(4)
    for n, score in scores.items():
        cols[n - 1].metric(
            f"Ticket {n}",
            f"{score:.0f}%" if score is not None else "–",
        )

    valid = [s for s in scores.values() if s is not None]
    if valid:
        final = sum(valid) / len(valid)
        cols[3].metric("Final Score", f"{final:.0f}%")

    submit_ticket_eval = st.button("Submit Ticket Evaluation Shadowing Data")

if shadowing_type == "Coaching Shadowing Session":
    coached_agent = st.number_input(
        "Coached Agent ID:", min_value=1000, max_value=99999, value=None)
    st.subheader("Coaching Criteria")
    answers_coaching = {}
    for s, (section, criteria) in enumerate(coaching_evaluation.items()):
        st.subheader(section)
        for i, criterion in enumerate(criteria):
            answers_coaching[criterion] = st.radio(
                criterion,
                ["Yes", "No"],
                index=None,
                horizontal=True,
                key=f"crit_coach_s{s}_c{i}",
            )
    st.text_area("Comments:")
    st.subheader("Coaching Score")

    answers = list(answers_coaching.values())
    yes = answers.count("Yes")
    no = answers.count("No")

    if yes + no > 0:
        coaching_score = yes / (yes + no) * 100
        st.metric("Final Score", f"{coaching_score:.0f}%")
    else:
        coaching_score = None
        st.metric("Final Score", "–")
    submit_coaching = st.button("Submit Coaching Shadowing Data")