import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime


# --- SIDEBAR: Filters + Info ---
with st.sidebar:
    st.title(":material/filter_alt: Filters")
    selected_partner = st.selectbox(
        "Partner Name",
        ["TP", "TWW", "HW", "OS", "PLCH"],
        index=None,
        placeholder="Choose a partner name...",
        key="partner",
        bind="query-params",
    )
    selected_teams = st.multiselect(
        "Team Name",
        options=["EN TN TWW", "FR TN TWW", "ECC EN TN TWW", "ECC FR TN TWW", "HVV TN TWW",
                 "EN EG TWW", "EN EG TP", "US/AU EG TP", "ECC EG TP", "EN KE TP", "US/AU KE TP",
                 "EN ZA TP", "EN UA HW", "ECC UA HW", "EN PH HW", "FR TN OS", "FR MA OS"],
        default=None,
        placeholder="Choose a team name...",
        key="teams",
        bind="query-params",
    )

    # selected_loop_no = st.selectbox(
    #     label="Loop Number",
    #     options=sorted(df["team_loops"].unique().to_list()),
    #     default=[],
    #     key="loop_no",
    #     bind="query-params",
    # )

# min_date = df["date"].min()
# max_date = df["date"].max()
#
# date_range = st.date_input(
#     "Date Range",
#     value=(min_date, max_date),   # two dates turns on range mode
#     min_value=min_date,
#     max_value=max_date,
#     key="date_range",
# )

    selected_position = st.selectbox(
        "Position",
        options=["QA", "Trainer"],
        index=None,
        placeholder="Choose a position...",
        key="position",
        bind="query-params",
    )
    # method options depends on selected position
    # if selected_position == "QA":
    #     method_options = sorted(
    #         df.filter(pl.col("position").is_in(selected_position))["method_options"]
    #         .unique()
    #         .to_list()
    #     )
    # else:
    #     method_options = sorted(df["method_options"].unique().to_list())
    # selected_method_options = st.multiselect(
    #     "Methods",
    #     options=method_options,
    #     default=[],
    #     key="method_options",
    #     bind="query-params",
    # )

# ---------- 1. SETTINGS ----------
target = 70      # we need to have table targets
good = 85
METHOD_ORDER = ["Ticket Solving", "Coaching", "Knowledge Test",
                "Updated Process Test", "Analytical Case Study"]
RAG = alt.Scale(type="threshold", domain=[target, good],
                range=["#d64545", "#e8b04a", "#3a9e5f"])   # red / amber / green

# ---------- 2. FAKE DATA (replace later with your real data) ----------
np.random.seed(42)   # later on we need to delete this line when we will have our real data

teams = {"EN TN TWW": "TWW", "FR TN TWW": "TWW", "EN EG TP": "TP",
         "EN UA HW": "HW", "FR TN OS": "OS"}

rows = []
for team, partner in teams.items():
    for q in range(1, 7):                          # 6 QAs per team
        for period in ["Last loop", "Current"]:
            for method in METHOD_ORDER:
                rows.append({
                    "Partner": partner,
                    "Team": team,
                    "QA": f"{team} QA{q}",
                    "Period": period,
                    "Method": method,
                    "Score": np.random.randint(45, 100),
                })

df = pd.DataFrame(rows)

# final score per QA per loop = average of their method scores
df["FinalScore"] = df.groupby(["QA", "Period"])["Score"].transform("mean").round(1)

current = df[df["Period"] == "Current"]
last = df[df["Period"] == "Last loop"]

# ---------- 3. KPI NUMBERS ----------
qa_current = current.drop_duplicates("QA")     # one row per QA
qa_last = last.drop_duplicates("QA")

avg_score = qa_current["FinalScore"].mean()
prev_avg_score = qa_last["FinalScore"].mean()
at_risk = (qa_current["FinalScore"] < target).sum()

# ---------- 4. PAGE ----------
st.title("LOE Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Last Loop Avg. LOE Score", f"{prev_avg_score:.1f}", border=True)
col2.metric("Current Avg. LOE Score", f"{avg_score:.1f}",
            f"{avg_score - prev_avg_score:+.1f} vs last loop", border=True)
col3.metric("QAs at risk", at_risk, border=True)

# ---------- 5. CHARTS ----------
left, right = st.columns(2)

target_line = alt.Chart(pd.DataFrame({"x": [target]})).mark_rule(
    color="red", strokeDash=[6, 4], size=2).encode(x="x:Q")

with left:
    st.subheader("Final score by method")
    # each method's share of the final score (all methods together = final score)
    by_method = current.groupby(["Team", "Method"], as_index=False)["Score"].mean()
    by_method["Points"] = by_method["Score"] / len(METHOD_ORDER)
    st.bar_chart(by_method, x="Team", y="Points", color="Method", horizontal=True)

with right:
    st.subheader("Last loop vs current")
    loop_df = (df.drop_duplicates(["QA", "Period"])
                 .groupby(["Team", "Period"], as_index=False)["FinalScore"].mean())
    bars = alt.Chart(loop_df).mark_bar().encode(
        x=alt.X("FinalScore:Q", scale=alt.Scale(domain=[0, 100]), title="Score"),
        y=alt.Y("Team:N", title=None),
        yOffset=alt.YOffset("Period:N", sort=["Last loop", "Current"]),
        color=alt.Color("Period:N", title=None,
                        scale=alt.Scale(domain=["Last loop", "Current"],
                                        range=["#b0b0b0", "#4a7bd6"])),
        tooltip=["Team", "Period", alt.Tooltip("FinalScore:Q", format=".1f")],
    )
    st.altair_chart(bars + target_line, width="stretch")

# ---------- 6. METHODS: WHO IS STRUGGLING WHERE ----------
st.header("Methods: who is struggling where?")

level = "Team"

st.subheader("Score per method")
st.caption(f"🔴 below {target}   🟡 {target}–{good - 1}   🟢 {good}+   ·   sorted from lowest final score")

heat = current.groupby([level, "Method"], as_index=False)["Score"].mean()
row_order = current.groupby(level)["FinalScore"].mean().sort_values().index.tolist()

base = alt.Chart(heat).encode(
    x=alt.X("Method:N", sort=METHOD_ORDER, title=None,
            axis=alt.Axis(orient="top", labelAngle=0, labelLimit=150)),
    y=alt.Y(f"{level}:N", sort=row_order, title=None),
)
cells = base.mark_rect(stroke="white", strokeWidth=2).encode(
    color=alt.Color("Score:Q", scale=RAG, legend=None),
    tooltip=[level, "Method", alt.Tooltip("Score:Q", format=".1f")],
)
labels = base.mark_text(fontSize=12, color="white", fontWeight="bold").encode(
    text=alt.Text("Score:Q", format=".0f"),
)
st.altair_chart((cells + labels).properties(height=max(200, 30 * len(row_order))),
                width="stretch")