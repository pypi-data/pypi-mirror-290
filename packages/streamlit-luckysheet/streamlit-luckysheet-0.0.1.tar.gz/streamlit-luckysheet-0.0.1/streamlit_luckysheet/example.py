import streamlit as st
from streamlit_luckysheet import streamlit_luckysheet

st.set_page_config(layout="wide")
st.subheader("Component with constant args")

result = streamlit_luckysheet()
