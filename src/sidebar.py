# src/sidebar.py
import streamlit as st

def show_global_slicers():
    """Render universal sidebar controls."""
    with st.sidebar:
        st.title("⚙️ Global Slicers")
        metric  = st.selectbox("Metric", ["Views", "Likes", "Dislikes", "Comments"])
        group   = st.selectbox("Group by", ["Categories", "Channels"])
        sort    = st.selectbox("Sort", ["Ascending", "Descending"])
        channel = st.selectbox("Channel (timeline)", ["All"] + sorted(st.session_state.df.Channel_Title.unique()))
        return metric, group, sort, channel