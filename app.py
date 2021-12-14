import streamlit as st
import plotly.express as px
import pandas as pd


df = pd.read_csv('prices.csv')

tokens = df['name'].unique()
n_tokes = len(tokens)
st.title("Lets make money with DefiChain")
for token in tokens:
    df_filtered = df[df['name'] == token]
    st.text(token)
    fig = px.line(df_filtered, x='time', y='dex_diff')
    st.plotly_chart(fig, use_container_width=True)
