import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import matplotlib.ticker as ticker

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

df['trend'] = 0

prev_high = 0
trend_start = None
trend_end = None
trend_detected = False

for i in range(1, len(df)):
    if not trend_detected and df['CI'][i] > 61.8 and df['CI'][i-1] > prev_high:
        trend_detected = True
        trend_start = i
        prev_high = df['CI'][i-1]
    elif trend_detected and df['CI'][i] < 38.2:
        trend_end = i
        df['trend'][trend_start:trend_end] = 1
        trend_detected = False
    elif trend_detected and df['CI'][i] < prev_high:
        prev_high = df['CI'][i]
    elif trend_detected and df['CI'][i] > 40:
        trend_end = i
        df['trend'][trend_start:trend_end] = 1
        trend_detected = False

fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

fig.add_trace(go.Candlestick(x=df.index,
                              open=df