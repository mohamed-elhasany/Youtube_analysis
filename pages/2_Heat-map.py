# pages/2_Heat-map.py
import streamlit as st
from src.cleaning import load_data
from src.sidebar import show_global_slicers
from src.analysis import prepare_to_plot_Bar_Heat
from src.plotting import generate_heatmap
# ---------- guarantee data ----------
if "df" not in st.session_state:
    st.session_state.df = load_data() 
# sidebar
metric, group, sort, _ = show_global_slicers()

# ---------- heat-map guard ----------
group = "Categories"   # <--  hard-lock
st.sidebar.markdown("🔒 **Heat-map locked to** `Categories`  (channels too heavy)")

grp_col = "Category_Title"
top = sort == "Ascending"


st.title("🔥 Heat-map – Intensity Grid")
st.divider()

grp_col = {"Categories": "Category_Title", "Channels": "Channel_Title"}[group]
top = sort == "Ascending"

data = prepare_to_plot_Bar_Heat(st.session_state.df, "Heat", metric, True, grp_col, top)
if isinstance(data, str):
    st.error(data); st.stop()

tok = {"x": metric, "Top": top, "grouping": {True: grp_col}}
fig = generate_heatmap(data, tok)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📘 How to read"):
    st.markdown(f"""
    **Colour intensity ∝ {metric.lower()}**  
    Darker = higher values → **hot spots**  
    Use hot columns to cross-promote content between **{group.lower()}**.
    """)