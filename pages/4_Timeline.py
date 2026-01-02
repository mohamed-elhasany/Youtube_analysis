# pages/4_Timeline.py
import streamlit as st
from src.cleaning import load_data 
from src.sidebar import show_global_slicers
from src.analysis import channel_analysis
from src.plotting import generate_line_plot
# ---------- guarantee data ----------
if "df" not in st.session_state:
    st.session_state.df = load_data() 
    
# sidebar
metric, _, _, channel = show_global_slicers()

st.title("📈 Timeline – Channel Evolution")
st.divider()

if channel == "All":
    st.info("Please select a single channel in the sidebar to view its timeline.")
    st.stop()

data = channel_analysis(st.session_state.df, channel, metric)
tok = {"channel": channel, "_by": metric}
fig = generate_line_plot(data, tok)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📘 Reading the line"):
    st.markdown(f"""
    - **X-axis** = publish date  
    - **Y-axis** = **{metric.lower()}**  
    **Look for:** spikes → replicate topic / collab; drops → avoid timing / format.
    """)