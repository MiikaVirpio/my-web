import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from .dash_layout import CHOICE_LABELS
from ..dash_helpers import VAPOR_SEQUENCE

def plot_scatter(df, companies, x_column, y_column, size_column, color_column):
    fig = px.scatter(
        df[df["name"].isin(companies)], # Subsetting hot!
        x=x_column,
        y=y_column,
        size=size_column,
        size_max=80, # How big you want Neste to be, practically.
        color=color_column,
        hover_name="yf_ticker", # The time this took...
        text="name",
    )
    fig.update_layout(
        xaxis_title=CHOICE_LABELS[x_column],
        yaxis_title=CHOICE_LABELS[y_column],
        legend_title=CHOICE_LABELS[color_column],
        template=pio.templates["VAPOR"],
    )
    return fig

def plot_lines(df, prices, companies):
    fig = go.Figure()
    for company in companies:
        # A bit of fiddle to get ticker from name and then close for ticker from prices
        # These ar the times I have thoughts of SQL and ORM
        ticker_prices = prices["Close"][df.loc[df["name"] == company, "yf_ticker"].iloc[0]]
        # Sets the first price to 0 and the rest to relative change to that.
        indexed_ticker_prices = (ticker_prices / ticker_prices[0]) - 1
        fig.add_trace(go.Scatter(
            x=prices.index,
            y=indexed_ticker_prices,
            mode="lines",
            name=company,
            text=ticker_prices, # Value is decimal percentage, but hover text is actual price
            ))
    # Disable legend if over 30 companies. Full market goes out the window otherwise.
    if len(companies) > 30:
        fig.update_layout(showlegend=False)
    fig.update_layout(
        height=800,
        template=pio.templates["VAPOR"],
    )
    return fig

def plot_sunburst(df, companies):
    fig = px.sunburst(
        df[df["name"].isin(companies)],
        path=["sector", "industry", "name"],
        values="mcap",
        color="sector",
        color_discrete_sequence=VAPOR_SEQUENCE, # Made it myself 😍
        )
    fig.update_layout(
        height=800,
        template=pio.templates["VAPOR"],
    )
    return fig

def plot_trader(df, prices, company):
    open_ = prices["Open"][df.loc[df["name"] == company, "yf_ticker"].iloc[0]]
    high_ = prices["High"][df.loc[df["name"] == company, "yf_ticker"].iloc[0]]
    low_ = prices["Low"][df.loc[df["name"] == company, "yf_ticker"].iloc[0]]
    close_ = prices["Close"][df.loc[df["name"] == company, "yf_ticker"].iloc[0]]
    sma5_ = close_.rolling(5).mean()
    sma20_ = close_.rolling(20).mean()
    def rolling_rsi(window):
        gain, loss, prev = 0, 0, None
        for close in window:
            if prev and close > prev:
                gain += (close-prev)/prev
            if prev and close < prev:
                loss += abs((close-prev)/prev)
            prev = close
        relative_strength = (gain/len(window))/(loss/len(window))
        return 100-(100/(1+relative_strength))
    rsi_ = close_.rolling(14).apply(rolling_rsi)
    williams_r_ = -((high_.rolling(14).max() - close_) / (high_.rolling(14).max() - low_.rolling(14).min()))
    stochastic_k_ = ((close_ - low_.rolling(14).min()) * 100 / (high_.rolling(14).max() - low_.rolling(14).min()))
    stochastic_d_ = stochastic_k_.rolling(3).mean()
    fig = go.Figure()
    fig.update_layout(height=1000,
        yaxis4={"domain": [0.4, 1.0], "autorange": True, "fixedrange": False},
        yaxis3={"domain": [0.25, 0.4], "autorange": True, "fixedrange": False, "title": "RSI"},
        yaxis2={"domain": [0.125, 0.25], "autorange": True, "fixedrange": False, "title": "S%K&S%D"},
        yaxis={"domain": [0.0, 0.125], "autorange": True, "fixedrange": False, "title": "W%R"},
    )
    fig.add_trace(go.Candlestick(name="OHLC",x=close_.index,open=open_,high=high_,low=low_,close=close_,yaxis="y4"))
    fig.add_trace(go.Scatter(name="SMA 5",x=close_.index,y=sma5_,yaxis="y4",line={"width": 1.5, "color": "#d9ff4f"},opacity=0.6))
    fig.add_trace(go.Scatter(name="SMA 20",x=close_.index,y=sma20_,yaxis="y4",line={"width": 1.5, "color": "#ffb04f"},opacity=0.6))
    fig.add_trace(go.Scatter(name="RSI",x=close_.index,y=rsi_,yaxis="y3",line={"width": 1, "color": "#ffffff"}))
    fig.add_shape({"type":"line","line":{"dash":"dot"},"opacity":0.4,"x0":0,"x1":1,"xref":"x domain","y0":70,"y1":70,"yref":"y3"})
    fig.add_shape({"type":"line","line":{"dash":"dot"},"opacity":0.4,"x0":0,"x1":1,"xref":"x domain","y0":30,"y1":30,"yref":"y3"})
    fig.add_trace(go.Scatter(name="Stochastic%K",x=close_.index,y=stochastic_k_,yaxis="y2",line={"width": 0.8, "color": "#1f8bff"}))
    fig.add_trace(go.Scatter( name="Stochastic%D",x=close_.index,y=stochastic_d_,yaxis="y2", line={"width": 0.8, "color": "#4fd6ff"}))
    fig.add_trace(go.Scatter(name="Williams %R",x=close_.index,y=williams_r_,yaxis="y",line={"width": 0.8, "color": "#9f2ca3"}))
    fig.add_shape({"type":"line","line":{"dash":"dot"},"opacity":0.4,"x0":0,"x1":1,"xref":"x domain","y0":-0.2,"y1":-0.2,"yref":"y"})
    fig.add_shape({"type":"line","line":{"dash":"dot"},"opacity":0.4,"x0":0,"x1":1,"xref":"x domain","y0":-0.8,"y1":-0.8,"yref":"y"})
    fig.update_layout(
        template=pio.templates["VAPOR"],
    )
    return fig