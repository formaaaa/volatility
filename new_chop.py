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

# Initialize trend column with all zeros
df['trend'] = 0

# Find periods of trending market
for i in range(1, len(df)):
    if df['CI'].iloc[i] < 61.8 < df['CI'].iloc[i - 1]:
        trend_start_idx = i
        trend_end_idx = i

        # Check if it ever crossed 38.2 in the next 21 rows
        for j in range(i + 1, min(i + 22, len(df))):
            if df['CI'].iloc[j] < 38.2:
                trend_end_idx = j

        # Mark all dates from start to crossing 38.2 as trend = 1
        df.loc[df.index[trend_start_idx:trend_end_idx], 'trend'] = 1

        # Continue to search for next row when it goes back above 38.2
        for j in range(trend_end_idx + 1, len(df)):
            if df['CI'].iloc[j] > 38.2:
                trend_start_idx = j
                trend_end_idx = j

                # Mark all dates until it goes back above 38.2 as trend = 1
                df.loc[df.index[trend_start_idx:trend_end_idx], 'trend'] = 1
                break

print(df.head())

df.to_csv('EURUSD_choppiness_index_new.csv')

"""# Add 61.8 and 38.2 lines to CI chart
ci_upper_band = 61.8
ci_lower_band = 38.2


fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1, row_heights=[0.7, 0.3])


fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='EURUSD Price'), row=1, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['CI'], name='Choppiness Index', line=dict(color='green')), row=2, col=1)
fig.add_hline(y=ci_upper_band, line_dash="dot", annotation_text="Upper Band", row=2, col=1)
fig.add_hline(y=ci_lower_band, line_dash="dot", annotation_text="Lower Band", row=2, col=1)


fig.update_layout(title_text='EURUSD Price and Choppiness Index', xaxis_ranges)"""