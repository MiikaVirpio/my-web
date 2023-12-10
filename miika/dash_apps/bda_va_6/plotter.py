import pandas as pd
import plotly.graph_objects as go

df = pd.read_excel("../../static/dash_apps/bda_va_6/share_manipulated.xlsx", skiprows=3)
df = df.drop(df.columns[0], axis=1)
# Set index to be the first column
df = df.set_index(df.columns[0])

# Draw a line for each day to spot patterns
fig = go.Figure()
for day in df.index:
    fig.add_trace(go.Scatter(x=df.columns, y=df.loc[day], name=day, mode="lines"))
fig.show()
# Well, that was not very helpful.

# Unpivot the DataFrame from wide format to long format
df_melted = df.melt(var_name='Time', value_name='Value', ignore_index=False)
# Combine the date and time into a single datetime column
df_melted['Datetime'] = pd.to_datetime("2023 " + df_melted.index + ' ' + df_melted['Time'].astype(str))
# Set 'Datetime' as the index
df_melted.set_index('Datetime', inplace=True)
# Drop the unnecessary columns
df_melted.drop(['Time'], axis=1, inplace=True)
# Order by index
df_melted.sort_index(inplace=True)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df_melted.index, y=df_melted['Value'], mode="lines"))
fig2.show()

df_ohlc = df_melted['Value'].resample('1D').ohlc()

fig3 = go.Figure()
fig3.add_trace(go.Candlestick(x=df_ohlc.index,
                              open=df_ohlc['open'],
                              high=df_ohlc['high'],
                              low=df_ohlc['low'],
                              close=df_ohlc['close']))
fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.show()