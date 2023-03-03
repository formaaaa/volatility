import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

df = pd.read_csv("data/EURUSD/EURUSD1440.csv",
                 names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
df.set_index('date', inplace=True)
df.drop(columns=['time', 'volume'], inplace=True)

df['TR'] = np.maximum(np.maximum(df['high'] - df['low'], np.abs(df['high'] - df['close'].shift())),
                      np.abs(df['low'] - df['close'].shift()))

n = 14
df['ATR'] = df['TR'].rolling(n).mean()

numerator = np.log10(df['ATR'].rolling(n).sum() / (df['high'].rolling(n).max() - df['low'].rolling(n).min()))
denominator = np.log10(n)

df['CI'] = 100 * numerator / denominator

df['trend'] = np.where(df['CI'] < 50, 1, 0)

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

fig.add_trace(go.Candlestick(x=df.index,
                             open=df['open'],
                             high=df['high'],
                             low=df['low'],
                             close=df['close'],
                             name='EURUSD'), row=1, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['CI'],
                         mode='lines',
                         name='Choppiness Index'), row=2, col=1)

fig.add_trace(go.Scatter(x=df.index,
                         y=df['trend'],
                         mode='lines',
                         name='Trend'), row=2, col=1)

fig.update_layout(xaxis_rangeslider_visible=False)

fig.show()

df.to_csv('EURUSD_choppiness_index.csv')

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])

fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='EURUSD Price'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['CI'], name='Choppiness Index', line=dict(color='green')), row=2, col=1)

fig.update_layout(title_text='EURUSD Price and Choppiness Index', xaxis_rangeslider_visible=False)

fig.show()

"""fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex='all', figsize=(12, 8))
ax1.plot(df.index, df['close'])
ax1.set_ylabel('Price')
ax2.plot(df.index, df['CI'], color='green')
ax2.set_ylabel('Choppiness Index')
# set x-axis date formatter to display only years
years = mdates.YearLocator()   # every year
years_fmt = mdates.DateFormatter('%Y')
ax2.xaxis.set_major_locator(years)
ax2.xaxis.set_major_formatter(years_fmt)
plt.show()"""
