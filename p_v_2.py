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


def identify_swing_points(df, deviation=10):
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

    # Forward fill the swing points to create the ZigZag line
    df['zigzag'] = df['swing'].fillna(method='ffill')

    # Plot the swing points
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['close'], name='EURUSD Price'))
    fig.add_trace(go.Scatter(x=df.index, y=df['zigzag'], name='ZigZag Line'))
    fig.add_trace(go.Scatter(x=df.index, y=df['swing'], name='Swing Points', mode='markers', marker=dict(color='black', size=8)))
    fig.show()

    # Remove the extra columns
    df.drop(columns=['high', 'low', 'high_diff', 'low_diff', 'swing'], inplace=True)

    return df


def calculate_zigzag(df):
    # Identify the peaks and valleys
    df['peaks'] = np.where(df['zigzag'] > df['zigzag'].shift(1), df['CI'], np.nan)
    df['valleys'] = np.where(df['zigzag'] < df['zigzag'].shift(1), df['CI'], np.nan)

    return df


# identify swing points
df = identify_swing_points(df)

# calculate ZigZag line
df = calculate_zigzag(df)

df.to_csv('EURUSD_zz.csv')