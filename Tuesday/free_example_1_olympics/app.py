# ==============================================================================
# FREE EXAMPLE 1 — Tuesday, Week 4 (CEN 3352)
# A second worked example, same shape as the teaching demo, different data.
# Study this on your own time — it is not live-coded in class.
# ==============================================================================
# Data: official Paris 2024 Olympic medal table (13 countries), sourced from
# the IOC's own results site, olympics.com/en/olympic-games/paris-2024/medals.
#
# This dataset has TWO good numeric columns (Gold, Total) instead of one —
# notice how the slider below lets you pick which one to filter by. That's
# a small step past the teaching example, worth trying in your own project.
#
# Run it:   streamlit run app.py
# (paris2024_olympic_medals.csv must be in the same folder as this file)
# ==============================================================================

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Paris 2024 Medal Table Explorer", page_icon="🏅", layout="wide")
st.title("Paris 2024 Olympics — Medal Table Explorer")
st.caption("Official IOC medal counts for the top 13 countries at the Paris 2024 Summer Olympics.")

# LOAD --------------------------------------------------------------------------
df = pd.read_csv("paris2024_olympic_medals.csv")

# LOOK BEFORE YOU BUILD -----------------------------------------------------------
with st.expander("Peek at the raw data (df.head, df.shape, df.columns)"):
    st.dataframe(df.head())

    rows = df.shape[0]
    cols = df.shape[1]
    st.write(f"**df.shape** — {rows} rows, {cols} columns.")

    st.write(list(df.columns))

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
st.subheader("Filter the medal table")
col1, col2, col3 = st.columns(3)
with col1:
    countries = df["Country"].unique().tolist()
    countries = sorted(countries)
    country_options = ["All countries"] + countries
    country_choice = st.selectbox("Filter by country", country_options)
with col2:
    metric_choice = st.selectbox("Filter by which medal count?", ["Gold", "Silver", "Bronze", "Total"])
with col3:
    lowest_value = int(df[metric_choice].min())
    highest_value = int(df[metric_choice].max())
    min_value = st.slider(
        f"Minimum {metric_choice.lower()} medals",
        min_value=lowest_value,
        max_value=highest_value,
        value=lowest_value,
    )

# SEARCH ----------------------------------------------------------------------------
search_text = st.text_input("Search by country name", placeholder="e.g. Un")

meets_minimum = df[metric_choice] >= min_value
filtered = df[meets_minimum]

if country_choice != "All countries":
    matches_country = filtered["Country"] == country_choice
    filtered = filtered[matches_country]

if search_text:
    matches_search = filtered["Country"].str.contains(search_text, case=False, na=False)
    filtered = filtered[matches_search]

# SORT --------------------------------------------------------------------------------
sort_col1, sort_col2 = st.columns(2)
with sort_col1:
    sort_by = st.selectbox("Sort by", ["Total", "Gold", "Silver", "Bronze", "Country"])
with sort_col2:
    ascending = st.checkbox("Ascending order", value=False)

filtered = filtered.sort_values(by=sort_by, ascending=ascending)

# METRICS -----------------------------------------------------------------------------
st.divider()
m1, m2, m3 = st.columns(3)

m1.metric("Countries shown", len(filtered))

if len(filtered) > 0:
    combined_gold = int(filtered["Gold"].sum())
else:
    combined_gold = 0
m2.metric("Combined gold medals (shown)", combined_gold)

if len(filtered) > 0:
    combined_total = int(filtered["Total"].sum())
else:
    combined_total = 0
m3.metric("Combined total medals (shown)", combined_total)

# TABLE — always the filtered data, never the original df --------------------------
st.dataframe(filtered, hide_index=True, use_container_width=True)

st.caption("Week 4 · Free Example 1 · CEN 3352 · Front-End Development and Design")

# ==============================================================================
# THURSDAY ADDS TWO CHARTS BELOW THIS LINE — see Thursday/free_example_1_olympics/app.py
# ==============================================================================