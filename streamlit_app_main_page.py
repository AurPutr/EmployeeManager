import streamlit as st
import pandas as pd
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
