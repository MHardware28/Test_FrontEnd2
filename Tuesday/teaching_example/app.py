# ==============================================================================
# TEACHING EXAMPLE — Tuesday, Week 4 (CEN 3352)
# Data Loading & Filtering
# ==============================================================================
# This is the file the instructor live-codes in front of the room, section by
# section, matching the slide deck (CEN3352_Week4_Tuesday.pptx). Every section
# below is labeled with the concept number from the slides so you can jump to
# wherever the lecture left off.
#
# Thursday picks this exact file back up and adds two charts at the bottom.
#
# The data is real: verified 2026 World Cup goalscorer totals
# (worldcup_scorers.csv), sourced from NBC Sports' official tournament
# tracker, published July 2026.
#
# Run it:   streamlit run app.py
# (worldcup_scorers.csv must be in the same folder as this file)
# ==============================================================================

import streamlit as st
import pandas as pd

st.set_page_config(page_title="World Cup Scorers Explorer", page_icon="\u26BD", layout="wide")
st.title("2026 World Cup \u2014 Top Scorers Explorer")
st.caption("Real, verified goalscorer totals. A loading-and-filtering demo, not the full tournament record.")

# ------------------------------------------------------------------------------
# CONCEPT 2 OF 5 — LOADING REAL DATA: ONE LINE
# ------------------------------------------------------------------------------
# A CSV is just a plain-text spreadsheet: commas separate columns, one row
# per line. pandas turns it into a dataframe in a single call. "pd" is the
# near-universal nickname for pandas — you'll see it in almost every example.
#
# The file MUST sit in the same folder as this script. A FileNotFoundError
# here almost always means the CSV is in the wrong place, not that your code
# is wrong — that's the single most common Week 4 error.
# ------------------------------------------------------------------------------
df = pd.read_csv("worldcup_scorers.csv")

# ------------------------------------------------------------------------------
# CONCEPT 3 OF 5 — LOOK BEFORE YOU BUILD
# ------------------------------------------------------------------------------
# Three things worth checking the moment ANY new dataset loads, before you
# write a single filter. In a notebook you'd run these as separate cells; in
# a Streamlit app they just print straight to the page. Comment these back
# out once you've eyeballed the data — they're a one-time sanity check, not
# part of the finished app.
# ------------------------------------------------------------------------------
with st.expander("Peek at the raw data (df.head, df.shape, df.columns)"):
    st.write("**df.head()** — first 5 rows. Did this load the way you expected?")
    st.dataframe(df.head()) # by default picks 5 rows, but you can pass a number to see more or fewer

    rows = df.shape[0] # number of rows, shape[0] is the first element of the shape tuple
    cols = df.shape[1]# number of columns, shape[1] is the second element of the shape tuple
    st.write(f"**df.shape** — {rows} rows, {cols} columns.") #PRINT ROW AND COLUMN 

    st.write(df.columns)          # Index(['Player', 'Country', 'Goals'], dtype='object')
    st.write(list(df.columns))    # ['Player', 'Country', 'Goals']ist() turns df.columns into a plain list so it prints cleanly

# ------------------------------------------------------------------------------
# CONCEPT 4 OF 5 — st.dataframe vs st.table
# ------------------------------------------------------------------------------
# Both show a table. They are NOT the same tool, and picking the wrong one
# is a common Week 4 mistake.
#
#   st.dataframe  → interactive: scrollable, sortable by clicking a column
#                   header, resizable columns. Use this almost always — it's
#                   what the rest of this app and the assignment expect.
#
#   st.table      → static: no scrolling, no sorting, renders EVERY row at
#                   once. Rarely what you want for a real dataset — useful
#                   only for a handful of summary rows.
#
# See the difference for yourself with the same 5 rows in both widgets:
# ------------------------------------------------------------------------------
with st.expander("st.dataframe vs st.table — see the difference"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.caption("st.dataframe — interactive")
        st.dataframe(df.head())
    with col_b:
        st.caption("st.table — static")
        st.table(df.head())

st.divider()

# ------------------------------------------------------------------------------
# LIVE CODING STEP 1 — Filter widgets
# ------------------------------------------------------------------------------
# Two widgets from Week 3, doing new work: instead of building a sentence,
# they now narrow a dataframe.
#
#   sorted(df["Country"].unique()) reads the actual countries straight from
#   the data — NEVER hardcode the list of options. If the CSV changes, this
#   line still works; a hardcoded list silently goes stale.
# ------------------------------------------------------------------------------
st.subheader("Filter the scorers")
col1, col2 = st.columns(2)
with col1:
    # Get every country that appears in the data, with no duplicates
    countries = df["Country"].unique().tolist()

    # Sort them alphabetically
    countries = sorted(countries)

    # Add an "All countries" option at the very front of the list
    country_options = ["All countries"] + countries

    # Show the dropdown
    country_choice = st.selectbox("Filter by country", country_options)

with col2:
    # Find the lowest and highest goal counts in the data
    lowest_goals = int(df["Goals"].min())
    highest_goals = int(df["Goals"].max())

    # Show the slider, using those as its min and max
    min_goals = st.slider("Minimum goals", lowest_goals, highest_goals, value=3)


# ------------------------------------------------------------------------------
# LIVE CODING STEP 2 — Searching
# ------------------------------------------------------------------------------
# A text_input is the third common filter shape, alongside selectbox and
# slider. .str.contains() checks whether a substring appears anywhere in the
# column; case=False makes "mbap" match "Mbappe". na=False keeps missing
# values from crashing the filter.
# ------------------------------------------------------------------------------
search_text = st.text_input("Search by player name", placeholder="e.g. mbap")

# ------------------------------------------------------------------------------
# Apply all three filters together. Start from the full dataframe and narrow
# it down one condition at a time — this is the pattern to copy for the
# assignment's second filter.
# ------------------------------------------------------------------------------
# Check each row: is Goals >= min_goals? (True or False for every row)
meets_minimum = df["Goals"] >= min_goals

# Keep only the rows where that was True
filtered = df[meets_minimum]

if country_choice != "All countries":
    # Check each row: does Country match what was picked in the dropdown?
    matches_country = filtered["Country"] == country_choice

    # Keep only the rows where that was True
    filtered = filtered[matches_country]
if search_text:
    # Check each row: does the player's name contain the search text?
    # case=False means ignore uppercase/lowercase differences
    # na=False means treat missing names as "no match" instead of crashing
    matches_search = filtered["Player"].str.contains(search_text, case=False, na=False)

    # Keep only the rows where that was True
    filtered = filtered[matches_search]

# ------------------------------------------------------------------------------
# LIVE CODING STEP 3 — Sorting
# ------------------------------------------------------------------------------
# st.dataframe already lets a user click a column header to sort — that's
# "free" sorting you get for nothing. But sometimes YOU want to control the
# default order the data is shown in, before the user touches anything.
# df.sort_values() does that explicitly.
# ------------------------------------------------------------------------------
sort_col1, sort_col2 = st.columns(2)
with sort_col1:
    sort_by = st.selectbox("Sort by", ["Goals", "Player", "Country"])
with sort_col2:
    ascending = st.checkbox("Ascending order", value=False)

filtered = filtered.sort_values(by=sort_by, ascending=ascending)

# ------------------------------------------------------------------------------
# SUMMARY METRICS — computed FROM the filtered data, so they update with
# every widget above. Never hardcode a number here.
# ------------------------------------------------------------------------------
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Players shown", len(filtered))
# Figure out the total goals shown
if len(filtered) > 0:
    total_goals = int(filtered["Goals"].sum())
else:
    total_goals = 0

# Figure out the top scorer shown
if len(filtered) > 0:
    top_scorer = filtered.iloc[0]["Player"]
else:
    top_scorer = "—"

m2.metric("Total goals (shown)", total_goals)
m3.metric("Top scorer (shown)", top_scorer)


# ------------------------------------------------------------------------------
# LIVE CODING STEP 4 — The table
# ------------------------------------------------------------------------------
# Display `filtered`, NOT `df`. This is the single most common beginner
# mistake in this whole assignment: showing the original, unfiltered
# dataframe because it's already sitting there as a variable.
#
# hide_index=True drops the 0,1,2... row numbers, which mean nothing to a
# viewer. use_container_width=True fills the available column width — this replaced
# use_container_width still runs today but prints a deprecation
# warning, and it will eventually stop working, so use width from here on.
# ------------------------------------------------------------------------------
st.dataframe(filtered, hide_index=True, use_container_width=True)


st.caption("Week 4 \u00b7 Data Explorer \u00b7 CEN 3352 \u00b7 Front-End Development and Design")

# ==============================================================================
# THURSDAY ADDS TWO CHARTS BELOW THIS LINE — see Thursday/teaching_example/app.py
# ==============================================================================
