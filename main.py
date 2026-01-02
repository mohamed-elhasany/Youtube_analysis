# main.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import streamlit as st
import pandas as pd
from src.sidebar import show_global_slicers
from src.cleaning import load_data
from src.analysis import prepare_to_plot_Bar_Heat

st.set_page_config(page_title="YouTube-US Executive Report",  page_icon="📺", layout="wide")

# ---------- guarantee data ----------
if "df" not in st.session_state:
    st.session_state.df = load_data()

# ---------- universal sidebar ----------
metric, group, sort, _ = show_global_slicers()

# ---------- report ----------

st.title("📊 Executive Summary – YouTube US Trending")
st.divider()

df = st.session_state.df
grp_col = {"Categories": "Category_Title", "Channels": "Channel_Title"}[group]

# ---------- KPI row ----------
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Total Videos", f"{len(df):,}")
with c2:
    st.metric(f"Total {metric}", f"{df[metric].sum():,}")
with c3:
    st.metric(f"Avg {metric}", f"{df[metric].mean():.0f}")
with c4:
    st.metric(f"Median {metric}", f"{df[metric].median():.0f}")

st.divider()

# ---------- top-5 tables ----------
left, right = st.columns(2)
with left:
    st.subheader(f"🏆 Top 5 {group} by {metric}")
    data = prepare_to_plot_Bar_Heat(df, "Bar", metric, True, grp_col, True).head(5)
    data["Rank"] = range(1, 6)
    st.dataframe(data[[grp_col, metric, "Rank"]].set_index("Rank"), use_container_width=True)

with right:
    st.subheader(f"📉 Bottom 5 {group} by {metric}")
    data = prepare_to_plot_Bar_Heat(df, "Bar", metric, True, grp_col, False).tail(5)
    data["Rank"] = range(1, 6)
    st.dataframe(data[[grp_col, metric, "Rank"]].set_index("Rank"), use_container_width=True)

# ---------- how to read ----------
with st.expander("📘 How to read this report"):
    st.markdown("""
    - **KPI cards** = snapshot of the entire dataset  
    - **Top / Bottom tables** = where to double-down or stop investing  
    Change slicers in the sidebar to refresh numbers instantly.
    """)