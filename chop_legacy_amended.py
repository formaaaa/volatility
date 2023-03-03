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


# Filter data to only include dates after 2022-01-01
df = df[df.index >= '2022-01-01']


fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])


line_color = np.where(df['trend'] == 1, 'orange', 'lime')


fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='EURUSD Price',
                        line=dict(color=line_color), dx=1, dy=1))


fig.add_trace(go.Scatter(x=df.index, y=df['CI'], name='Choppiness Index', line=dict(color='green')), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['trend'], name='Trend', line=dict(color='red')), row=2, col=1)


fig.update_layout(title_text='EURUSD Price and Choppiness Index', xaxis_rangeslider_visible=False)


fig.show()
