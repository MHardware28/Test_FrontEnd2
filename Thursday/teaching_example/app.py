# ==============================================================================
# TEACHING EXAMPLE — Thursday, Week 4 (CEN 3352)
# Charts With Altair & Plotly — MINI ASSIGNMENT 1 DUE TODAY
# ==============================================================================
# This is Tuesday's file, unchanged down to the divider — loaded, displayed,
# filterable. Everything below the divider is new: two charts, both built
# from `filtered`, matching the slide deck (CEN3352_Week4_Thursday.pptx).
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
import altair as alt
import plotly.express as px

st.set_page_config(page_title="World Cup Scorers Explorer", page_icon="⚽", layout="wide")
st.title("2026 World Cup — Top Scorers Explorer")
st.caption("Real, verified goalscorer totals. A layout-and-data demo, not the full tournament record.")

# Load the data
df = pd.read_csv("worldcup_scorers.csv")

st.subheader("Filter the scorers")
col1, col2 = st.columns(2)
with col1:
    # Get every country that appears in the data, with no duplicates
    countries = df["Country"].unique().tolist()

    # Sort them alphabetically
    countries = sorted(countries)

    # Add an "All countries" option at the very front of the list
    country_options = ["All countries"] + countries

    country_choice = st.selectbox("Filter by country", country_options)
with col2:
    # Find the lowest and highest goal counts in the data
    lowest_goals = int(df["Goals"].min())
    highest_goals = int(df["Goals"].max())

    min_goals = st.slider("Minimum goals", lowest_goals, highest_goals, value=3)

search_text = st.text_input("Search by player name", placeholder="e.g. mbap")

# Check each row: is Goals >= min_goals?
meets_minimum = df["Goals"] >= min_goals
filtered = df[meets_minimum]

if country_choice != "All countries":
    # Check each row: does Country match what was picked in the dropdown?
    matches_country = filtered["Country"] == country_choice
    filtered = filtered[matches_country]

if search_text:
    # Check each row: does the player's name contain the search text?
    matches_search = filtered["Player"].str.contains(search_text, case=False, na=False)
    filtered = filtered[matches_search]

sort_col1, sort_col2 = st.columns(2)
with sort_col1:
    sort_by = st.selectbox("Sort by", ["Goals", "Player", "Country"])
with sort_col2:
    ascending = st.checkbox("Ascending order", value=False)

filtered = filtered.sort_values(by=sort_by, ascending=ascending)

m1, m2, m3 = st.columns(3)
m1.metric("Players shown", len(filtered))

# Figure out the total goals shown
if len(filtered) > 0:
    total_goals = int(filtered["Goals"].sum())
else:
    total_goals = 0
m2.metric("Total goals (shown)", total_goals)

# Figure out the top scorer shown
if len(filtered) > 0:
    top_scorer = filtered.iloc[0]["Player"]
else:
    top_scorer = "—"
m3.metric("Top scorer (shown)", top_scorer)

st.dataframe(filtered, hide_index=True, use_container_width=True)

st.divider()

# ==============================================================================
# EVERYTHING BELOW THIS LINE IS NEW TODAY
# ==============================================================================

# ------------------------------------------------------------------------------
# CONCEPT 1 OF 4 — CHOOSING THE RIGHT CHART TYPE
# ------------------------------------------------------------------------------
# The question isn't "which chart looks best" — it's "what am I trying to
# show?" Answer that first, then pick the shape that answers it:
#
#   Comparing categories (who scored the most?)      → bar chart
#   Showing change over time (up or down over weeks?) → line chart
#   Showing parts of a whole (what SHARE of the total?) → pie chart, used
#       sparingly, and only when the slices genuinely sum to something
#       meaningful (100% of goals, 100% of respondents — not an average).
#
# This app needs one chart from each library, not because one is better,
# but because real projects mix tools. Both charts below are built from
# `filtered` — a chart built from the original `df` would run without
# errors, look completely normal, and still fail the assignment, because it
# wouldn't respond to anything the user did above.
# ------------------------------------------------------------------------------
st.subheader("Charts")

if len(filtered) == 0:
    st.info("No players match the current filters — widen them to see charts.")
else:
    chart_col1, chart_col2 = st.columns(2)

    # --------------------------------------------------------------------------
    # CONCEPT 4 OF 4 — ALTAIR'S GRAMMAR: CHART, MARK, ENCODE
    # --------------------------------------------------------------------------
    #   alt.Chart(filtered)   which dataframe to draw from
    #   .mark_bar()           what shape — mark_bar, mark_line, mark_point,
    #                         mark_arc (pie) all exist
    #   .encode(x=..., y=...) which columns map to which visual position
    #
    # "Goals by player" is a category comparison, so it's a bar chart. Two
    # customizations that matter here, per the "colors and labels" part of
    # today's topic:
    #   sort="-x"        orders bars by value, descending. Without it, Altair
    #                     sorts alphabetically, which almost never tells the
    #                     right story.
    #   alt.Color(...)    maps Country to bar color, so you can see at a
    #                     glance which country each scorer plays for, with a
    #                     legend Altair builds automatically.
    # --------------------------------------------------------------------------
    with chart_col1:
        st.caption("Altair — goals by player (comparing categories → bar chart)")

        # Start the chart, using the filtered data
        altair_chart = alt.Chart(filtered)

        # Draw it as bars
        altair_chart = altair_chart.mark_bar()

        # Map Goals to the x-axis, Player to the y-axis (sorted by value),
        # and Country to bar color
        altair_chart = altair_chart.encode(
            x=alt.X("Goals:Q", title="Goals"),
            y=alt.Y("Player:N", sort="-x", title=None),
            color=alt.Color("Country:N", title="Country"),
            tooltip=["Player", "Country", "Goals"],
        )

        st.altair_chart(altair_chart, use_container_width=True)

    # --------------------------------------------------------------------------
    # CONCEPT 2 OF 4 — TWO LIBRARIES, SAME JOB
    # --------------------------------------------------------------------------
    # Plotly Express: one function call per chart type — px.bar, px.pie,
    # px.scatter — and interactive (hover, zoom) with zero extra code.
    # "What SHARE of the shown goals came from each country?" is a
    # parts-of-a-whole question, and there are few enough countries here for
    # a pie/donut to stay readable — that's the "use sparingly" condition
    # from Concept 1 being satisfied, not ignored.
    #
    # color_discrete_sequence and a title are today's "customizing colors and
    # labels" — Plotly's defaults are fine, but naming your own palette and
    # title is what makes a chart look intentional instead of default.
    # --------------------------------------------------------------------------
    with chart_col2:
        st.caption("Plotly — share of goals by country (parts of a whole → donut chart)")

        # Add up total goals for each country in the filtered data
        by_country = filtered.groupby("Country", as_index=False)["Goals"].sum()

        # Build the pie chart
        plotly_fig = px.pie(
            by_country,
            names="Country",
            values="Goals",
            hole=0.4,
            title="Share of Shown Goals",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )

        # Show each slice's label and percentage on the chart itself
        plotly_fig.update_traces(textinfo="label+percent")

        st.plotly_chart(plotly_fig, use_container_width=True)

st.caption("Week 4 · Data Explorer · CEN 3352 · Front-End Development and Design")