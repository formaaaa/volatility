import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# read data and set index
df = pd.read_csv('data/EURUSD/EURUSD1440.csv', names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
df.set_index('date', inplace=True)
df.drop(columns=['time', 'volume'], inplace=True)

# calculate choppiness index
df['TR'] = np.maximum(np.maximum(df['high'] - df['low'], np.abs(df['high'] - df['close'].shift())),
                      np.abs(df['low'] - df['close'].shift()))

n = 14
df['ATR'] = df['TR'].rolling(n).mean()

numerator = np.log10(df['ATR'].rolling(n).sum() / (df['high'].rolling(n).max() - df['low'].rolling(n).min()))
denominator = np.log10(n)

df['CI'] = 100 * numerator / denominator


def zigzag(df, deviation=3):
    # Calculate the price extremes
    df['high'] = df['close'].rolling(window=10).max()
    df['low'] = df['close'].rolling(window=10).min()

    # Calculate the distance from the extremes
    df['high_diff'] = df['high'] - df['close']
    df['low_diff'] = df['close'] - df['low']

    # Identify the swing points
    df['swing'] = np.nan
    up_swing = df['high_diff'] >= deviation
    down_swing = df['low_diff'] >= deviation
    df.loc[up_swing, 'swing'] = df['low'][up_swing]
    df.loc[down_swing, 'swing'] = df['high'][down_swing]

    # Print the swing points
    print(df['swing'])

    # Forward fill the swing points to create the ZigZag line
    df['zigzag'] = df['swing'].fillna(method='ffill')

    # Remove the extra columns
    df.drop(columns=['high', 'low', 'high_diff', 'low_diff', 'swing'], inplace=True)

    # Identify the peaks and valleys
    df['peaks'] = np.where(df['zigzag'] > df['zigzag'].shift(1), df['CI'], np.nan)
    df['valleys'] = np.where(df['zigzag'] < df['zigzag'].shift(1), df['CI'], np.nan)

    # Print the peaks and valleys
    print(df['peaks'])
    print(df['valleys'])

    return df



df = zigzag(df)
df['peaks'] = np.where(df['zigzag'] > df['zigzag'].shift(1), df['CI'], np.nan)
df['valleys'] = np.where(df['zigzag'] < df['zigzag'].shift(1), df['CI'], np.nan)


df.to_csv('EURUSD_zz.csv')

# create figure with subplots
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.02)

# add upper subplot for EURUSD price
fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='EURUSD Price'), row=1, col=1)

# add lower subplot for choppiness index with peaks and valleys scatter plot
fig.add_trace(go.Scatter(x=df.index, y=df['CI'], name='Choppiness Index'), row=2, col=1)
fig.add_trace(go.Scatter(x=df.index, y=df['peaks'], name='Peaks', mode='markers', marker=dict(color='red', size=8)),
              row=2, col=1)
fig.add_trace(
    go.Scatter(x=df.index, y=df['valleys'], name='Valleys', mode='markers', marker=dict(color='green', size=8)), row=2,
    col=1)

# update x-axis properties
fig.update_xaxes(title_text='Date', row=2, col=1)
fig.update_xaxes(showticklabels=False, row=1, col=1)

# update y-axis properties
fig.update_yaxes(title_text='EURUSD Price', row=1, col=1)
fig.update_yaxes(title_text='Choppiness Index', row=2, col=1)

# update layout
fig.update_layout(title='EURUSD Price and Choppiness Index with Peaks and Valleys',
                  height=800)

# show figure
fig.show()




"""
when the chop fall back under 61.8 and continues to or below 38.2, then it reverses above 38.2 or 50



"""

# add peaks and valleys column
# threshold_peak = 55
# threshold_valley = 45
# shift = 1

# df['peaks'] = np.where((df['CI'] > df['CI'].shift(shift)) & (df['CI'] > df['CI'].shift(-shift)) & (df['CI'] >
# threshold_peak), df['CI'], np.nan)
# df['valleys'] = np.where((df['CI'] < df['CI'].shift(shift)) & (df['CI'] < df[
# 'CI'].shift(-shift)) & (df['CI'] < threshold_valley), df['CI'], np.nan)
