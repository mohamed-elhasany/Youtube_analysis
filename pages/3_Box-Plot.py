# pages/3_Box-Plot.py
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from src.cleaning import load_data 
from src.sidebar import show_global_slicers
from src.plotting import generate_boxplot


# ---------- guarantee data ----------
if "df" not in st.session_state:
    st.session_state.df = load_data() 
    
# sidebar
_, _, _, _ = show_global_slicers()   # keep slicers visible

st.title("📦 Box-Plot – Distribution Overview")
st.divider()

fig = generate_boxplot(st.session_state.df)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📘 Understanding the boxes"):
    st.markdown("""
    - **Box** = middle 50 % of videos  
    - **Line inside** = median  
    - **Points outside** = outliers (viral hits or flops)  
    **Action:** tall box → unpredictable; compress it with better thumbs/titles.
    """)