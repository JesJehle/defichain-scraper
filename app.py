import streamlit as st
import plotly.graph_objects as go
import pandas as pd


df = pd.read_csv('prices.csv')

tokens = df['name'].unique()
n_tokes = len(tokens)
st.title("Lets make money with DefiChain")
for token in tokens:
    st.title(token)
    df_filtered = df[df['name'] == token]
    df_sorted = df_filtered.sort_values(by="time", key=pd.to_datetime)
    moving_avg = df_sorted.copy()
    moving_avg['dex_diff'] = df_sorted['dex_diff'].rolling(15).mean()
    moving_avg['time'] = df_sorted['time']
    current_price_diff = round(df_sorted.iloc[-1]['dex_diff'], 2)
    current_average = round(moving_avg.iloc[-1]['dex_diff'], 2)
    st.text(f"Current Price Difference: {current_price_diff} %")
    st.text(f"The moving average is: {current_average}")
    magnitude = round(abs(current_price_diff / current_average)) * "#"
    if current_price_diff < current_average:
        st.markdown(f"**buying** {magnitude }")
    else:
        st.markdown(f"**selling** {magnitude }")

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=df_sorted['time'], y=df_sorted['dex_diff'],
                   name='dex / oracle', line=dict(color='#ff9900', width=2))
    )
    fig.add_trace(
        go.Scatter(x=moving_avg['time'], y=moving_avg['dex_diff'],
                   name="moving average",  line=dict(color='white', width=2))
    )
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))
    st.plotly_chart(fig, use_container_width=True)
