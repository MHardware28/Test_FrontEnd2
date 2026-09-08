# ==============================================================================
# FREE EXAMPLE 2 — Thursday, Week 4 (CEN 3352)
# Tuesday's coffee explorer, plus two charts. Study this on your own time —
# it is not live-coded in class.
# ==============================================================================
# Data: real responses from "The Great American Coffee Taste Test" — a blind
# tasting survey James Hoffmann (2007 World Barista Champion, YouTuber) ran
# with coffee company Cometeer in October 2023, cleaned and published by the
# TidyTuesday project (rfordatascience/tidytuesday, 2024-05-14). This file is
# a 32-row reproducible random sample — see Tuesday's app.py for full notes
# on how the sample and columns were built.
#
# Run it:   streamlit run app.py
# (coffee_survey_sample.csv must be in the same folder as this file)
# ==============================================================================

import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

st.set_page_config(page_title="Coffee Taste Test Explorer", page_icon="☕", layout="wide")
st.title("The Great American Coffee Taste Test — Explorer")
st.caption("A sample of real respondent ratings from James Hoffmann & Cometeer's Oct. 2023 blind tasting survey.")

# LOAD --------------------------------------------------------------------------
df = pd.read_csv("coffee_survey_sample.csv")

# LOOK BEFORE YOU BUILD -----------------------------------------------------------
with st.expander("Peek at the raw data (df.head, df.shape, df.columns)"):
    st.dataframe(df.head())

    # Get the number of rows and columns
    rows = df.shape[0]
    cols = df.shape[1]
    st.write(f"**df.shape** — {rows} rows, {cols} columns.")

    # list() turns df.columns into a plain list so it prints cleanly
    st.write(list(df.columns))

    st.caption(
        "Real survey data is messier than anything you've typed by hand: brew_method came from a "
        "multi-select question, roast_level has uneven category sizes, and every rating is a real "
        "person's honest 1-5, not a clean round number."
    )

# st.dataframe vs st.table ---------------------------------------------------------
with st.expander("st.dataframe vs st.table — see the difference"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("st.dataframe — interactive")
        st.dataframe(df.head())
    with col_b:
        st.caption("st.table — static")
        st.table(df.head())

st.divider()

# FILTERS -------------------------------------------------------------------------
st.subheader("Filter the respondents")
col1, col2 = st.columns(2)
with col1:
    # Get every roast level that appears in the data, with no duplicates
    roast_levels = df["roast_level"].unique().tolist()

    # Sort them alphabetically
    roast_levels = sorted(roast_levels)

    # Add an "All roasts" option at the very front of the list
    roast_options = ["All roasts"] + roast_levels

    roast_choice = st.selectbox("Filter by roast level", roast_options)
with col2:
    min_preference = st.slider(
        "Minimum preference rating for Coffee A (1-5)",
        min_value=1,
        max_value=5,
        value=1,
    )

# SEARCH ----------------------------------------------------------------------------
# brew_method is free text, not a fixed set of options, so a search box makes
# more sense here than a selectbox — try searching "pour" or "espresso".
search_text = st.text_input("Search by brew method", placeholder="e.g. pour")

# Check each row: is the preference rating at or above the minimum?
meets_minimum = df["coffee_a_preference_1to5"] >= min_preference
filtered = df[meets_minimum]

if roast_choice != "All roasts":
    # Check each row: does roast_level match what was picked in the dropdown?
    matches_roast = filtered["roast_level"] == roast_choice
    filtered = filtered[matches_roast]

if search_text:
    # Check each row: does brew_method contain the search text?
    # case=False means ignore uppercase/lowercase differences
    # na=False means treat missing values as "no match" instead of crashing
    matches_search = filtered["brew_method"].str.contains(search_text, case=False, na=False)
    filtered = filtered[matches_search]

# SORT --------------------------------------------------------------------------------
sort_col1, sort_col2 = st.columns(2)
with sort_col1:
    sort_by = st.selectbox(
        "Sort by", ["coffee_a_preference_1to5", "self_rated_expertise", "roast_level", "age_group"]
    )
with sort_col2:
    ascending = st.checkbox("Ascending order", value=False)

filtered = filtered.sort_values(by=sort_by, ascending=ascending)

# METRICS -----------------------------------------------------------------------------
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Respondents shown", len(filtered))

# Figure out the average preference rating shown
if len(filtered) > 0:
    avg_preference = round(filtered["coffee_a_preference_1to5"].mean(), 2)
else:
    avg_preference = "—"
m2.metric("Average preference rating (shown)", avg_preference)

# Figure out the average self-rated expertise shown
if len(filtered) > 0:
    avg_expertise = round(filtered["self_rated_expertise"].mean(), 1)
else:
    avg_expertise = "—"
m3.metric("Average self-rated expertise (shown)", avg_expertise)

# TABLE — always the filtered data, never the original df --------------------------
st.dataframe(filtered, hide_index=True, use_container_width=True)

st.caption("Week 4 · Free Example 2 · CEN 3352 · Front-End Development and Design")


# ==============================================================================
# EVERYTHING BELOW THIS LINE IS NEW TODAY
# ==============================================================================
st.subheader("Charts")

if len(filtered) == 0:
    st.info("No respondents match the current filters — widen them to see charts.")
else:
    chart_col1, chart_col2 = st.columns(2)

    # Comparing bitterness vs. acidity ratings across roast levels is a
    # category comparison, so it's a bar chart — but there are two numeric
    # values per roast level, so both need encoding. Averaging first with
    # groupby keeps the bars readable instead of plotting all 32 raw points.
    with chart_col1:
        st.caption("Altair \u2014 average bitterness vs. acidity by roast level (comparing categories \u2192 bar chart)")
        by_roast = (
            filtered.groupby("roast_level", as_index=False)[["coffee_a_bitterness_1to5", "coffee_a_acidity_1to5"]]
            .mean()
            .melt(id_vars="roast_level", var_name="Attribute", value_name="Average rating")
        )
        by_roast["Attribute"] = by_roast["Attribute"].replace(
            {"coffee_a_bitterness_1to5": "Bitterness", "coffee_a_acidity_1to5": "Acidity"}
        )
        altair_chart = (
            alt.Chart(by_roast)
            .mark_bar()
            .encode(
                x=alt.X("roast_level:N", title="Roast level"),
                y=alt.Y("Average rating:Q", scale=alt.Scale(domain=[0, 5])),
                color=alt.Color("Attribute:N", scale=alt.Scale(range=["#6F4E37", "#C9A66B"]), title=None),
                xOffset="Attribute:N",
                tooltip=["roast_level", "Attribute", "Average rating"],
            )
        )
        st.altair_chart(altair_chart, use_container_width=True)

    # How many shown respondents fall into each roast level is a parts-of-a-
    # whole question — what SHARE of the filtered group prefers each roast —
    # so a donut is appropriate, and stays readable with only a few roast
    # levels ever appearing in the filtered set.
    with chart_col2:
        st.caption("Plotly \u2014 roast level mix, shown respondents (parts of a whole \u2192 donut chart)")
        roast_counts = filtered["roast_level"].value_counts().reset_index()
        roast_counts.columns = ["roast_level", "count"]
        plotly_fig = px.pie(
            roast_counts,
            names="roast_level",
            values="count",
            hole=0.4,
            title="Roast Level Mix",
            color_discrete_sequence=px.colors.sequential.Brwnyl,
        )
        plotly_fig.update_traces(textinfo="label+percent")
        st.plotly_chart(plotly_fig, use_container_width=True)

st.caption("Week 4 \u00b7 Free Example 2 \u00b7 CEN 3352 \u00b7 Front-End Development and Design")
