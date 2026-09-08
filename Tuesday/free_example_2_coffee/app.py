# ==============================================================================
# FREE EXAMPLE 2 — Tuesday, Week 4 (CEN 3352)
# A third worked example, same shape as the teaching demo, different data.
# Study this on your own time — it is not live-coded in class.
# ==============================================================================
# Data: real responses from "The Great American Coffee Taste Test" — a blind
# tasting survey James Hoffmann (2007 World Barista Champion, YouTuber) ran
# with coffee company Cometeer in October 2023. ~4,000 viewers rated the same
# coffees and answered questions about how they drink coffee.
#
# The full survey (4,042 responses, 57 columns) was cleaned and published by
# the TidyTuesday project: rfordatascience/tidytuesday, 2024-05-14. This file
# uses a 32-row random sample (seed=42, reproducible) of respondents who fully
# rated "Coffee A" — the first coffee in the blind tasting — kept to columns
# relevant to a beginner filtering demo. Ratings are on the survey's original
# 1-5 scale; "brew_method" keeps only the FIRST method each respondent listed,
# since the raw survey allowed multiple selections.
#
# Run it:   streamlit run app.py
# (coffee_survey_sample.csv must be in the same folder as this file)
# ==============================================================================

import streamlit as st
import pandas as pd

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
# THURSDAY ADDS TWO CHARTS BELOW THIS LINE — see Thursday/free_example_2_coffee/app.py
# ======