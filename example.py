from youtubesearchpython import VideosSearch
import streamlit as st

videosSearch = VideosSearch('NoCopyrightSounds', limit = 2)

st.write(videosSearch.result())