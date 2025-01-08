import plotly.graph_objects as go
import streamlit as st

def plot_stock_price(df):
    if df.empty:
        st.write("No stock price data available")
        return

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'], mode='lines'))
    fig.update_layout(
        title='5 Year Stock Price',
        xaxis_title='Date',
        yaxis_title='Price',
        showlegend=False
    )
    st.plotly_chart(fig)
