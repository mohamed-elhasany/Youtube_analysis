# pages/3_Box-Plot.py

import traceback  # TEMP: show real error
try:
    import streamlit as st
    from src.cleaning import load_data
    from src.sidebar import show_global_slicers
    from src.plotting import generate_boxplot
except Exception as e:
    st.error(traceback.format_exc())
    st.stop()

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