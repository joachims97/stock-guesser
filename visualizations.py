import plotly.graph_objects as go
import streamlit as st

def plot_stock_price(df):
    if df.empty:
        st.write("No stock price data available")
        return

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['close'],
            mode='lines',
            hovertemplate='$%{y:.2f}<extra></extra>',
            line=dict(color='#2196F3')
        )
    )

    fig.update_layout(
        title='5 Year Chart',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        showlegend=False,
        hovermode='x',
        xaxis=dict(
            fixedrange=False,
            showspikes=True,  # Enable spikes (vertical line)
            spikethickness=1,
            spikecolor="gray",
            spikemode="across",  # Makes the spike go across the plot
            spikesnap="cursor"
        ),
        yaxis=dict(
            fixedrange=True,
            showspikes=False  # No horizontal spike
        ),
        dragmode=False
    )

    st.plotly_chart(fig, config={
        'displayModeBar': False,
        'scrollZoom': False
    })