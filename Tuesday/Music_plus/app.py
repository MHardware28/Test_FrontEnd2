import streamlit as st
import pandas as pd

st.set_page_config(page_title="MUSIC", page_icon="🎵", layout="wide")
# this sets the icon to a medal in the browser tab
st.title("A WORLD OF MUSIC")
#Title of the page

df = pd.read_csv("Apple.csv")
st.dataframe(df)
#This displays the music data in a table format

#This will search by the artist name specifically
search_text = st.text_input("Search by artist name", placeholder="e.g. Chronixx")
st.write(f"Search results for: {search_text}")
if search_text:
    filtered_df = df[df["Artist name"].str.contains(search_text.lower(), case=False, na=False)]
    st.dataframe(filtered_df)

filtered = filtered_df

#This will now all the user to sort said list in ascending/descending order

ascending = st.checkbox("Sort in ascending order", value=True)
filtered = filtered.sort_values("Track name", ascending=ascending)
st.dataframe(filtered)