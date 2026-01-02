# pages/1_Bar_Chart.py
import streamlit as st
from src.sidebar import show_global_slicers
from src.cleaning import load_data
from src.analysis import prepare_to_plot_Bar_Heat
from src.plotting import generate_bar_plot

# guarantee dataframe
if "df" not in st.session_state:
    st.session_state.df = load_data()

# sidebar
metric, group, sort, _ = show_global_slicers()
top = sort == "Ascending"          # ← local variable, NOT st.session_state.sort

st.title("📊 Bar Chart – Top / Bottom Performers")
st.divider()

grp_col = {"Categories": "Category_Title", "Channels": "Channel_Title"}[group]

data = prepare_to_plot_Bar_Heat(st.session_state.df, "Bar", metric, True, grp_col, top)
if isinstance(data, str):
    st.error(data)
    st.stop()

tok = {"x": metric, "Top": top, "grouping": {True: grp_col}}
fig = generate_bar_plot(data, tok)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📘 Interpretation"):
    st.markdown(f"""
    - Each bar = one **{group[:-1].lower()}**  
    - Height = total **{metric.lower()}**  
    - Order = **{'lowest → highest' if top else 'highest → lowest'}**  
    **Take-away:** allocate promotion budget to dark (high) bars.
    """)