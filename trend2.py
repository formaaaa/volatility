import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import matplotlib.ticker as ticker

df = pd.read_csv("data/EURUSD/EURUSD1440.csv", names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
df.set_index('date', inplace=True)
df.drop(columns=['time', 'volume'], inplace=True)

df['TR'] = np.maximum(np.maximum(df['high'] - df['low'], np.abs(df['high'] - df['close'].shift())),
                     np.abs(df['low'] - df['close'].shift()))

n = 14
df['ATR'] = df['TR'].rolling(n).mean()

numerator = np.log10(df['ATR'].rolling(n).sum() / (df['high'].rolling(n).max() - df['low'].rolling(n).min()))
denominator = np.log10(n)

df['CI'] = 100 * numerator / denominator

# Select the relevant period
start_date = '2015-04-20'
end_date = '2022-02-24'
df_selected = df.loc[start_date:end_date]

# Set trend to 0 by default
df_selected['trend'] = 0

# Find the indices where CI crosses 61.8 and 38.2
ci_cross_618 = df_selected[df_selected['CI'] > 61.8].index
ci_cross_382 = df_selected[df_selected['CI'] < 38.2].index

# Find the index where CI crosses 61.8 from top to bottom
cross_618_top_bottom = None
for i in range(1, len(ci_cross_618)):
    if df_selected.loc[ci_cross_618[i-1], 'CI'] > 61.8 and df_selected.loc[ci_cross_618[i], 'CI'] < 61.8:
        cross_618_top_bottom = ci_cross_618[i]
        break

# Find the index where CI crosses 38.2 from bottom to top
cross_382_bottom_top = None
for i in range(1, len(ci_cross_382)):
    if df_selected.loc[ci_cross_382[i-1], 'CI'] < 38.2 and df_selected.loc[ci_cross_382[i], 'CI'] > 38.2:
        cross_382_bottom_top = ci_cross_382[i]
        break

# Set trend = 1 for the desired period
if cross_618_top_bottom is not None and cross_382_bottom_top is not None:
    df_selected.loc[cross_618_top_bottom:cross_382_bottom_top, 'trend'] = 1
    df_selected.loc[end_date, 'trend'] = 1
    df_selected.loc[start_date, 'trend'] = 0

print(df_selected[['CI', 'trend']])

df_selected.to_csv('EURUSD_choppiness_index2.csv', index=False)
