
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("GridSpot MVP - EV Charging Opportunity Map")

df = pd.read_csv("data/gridspot_data.csv")
st.dataframe(df)

st.write("This is a placeholder for the interactive map.")
