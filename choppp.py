import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# Load data
df = pd.read_csv('EURUSD.csv', parse_dates=['date'])

# Calculate indicators
df['TR'] = np.maximum(np.maximum(df['high'] - df['low'], np.abs(df['high'] - df['close'].shift())),
                    np.abs(df['low'] - df['close'].shift()))
n = 14
df['ATR'] = df['TR'].rolling(n).mean()

numerator = np.log10(df['ATR'].rolling(n).sum() / (df['high'].rolling(n).max() - df['low'].rolling(n).min()))
denominator = np.log10(n)
df['CI'] = 100 * numerator / denominator
df['trend'] = 0

# Calculate trend
high_CI = df['CI'].shift(1) > 61.8
crossed_618 = [False] + list((df['CI'] < 61.8) & (df['CI'].shift(1) > 61.8))[1:]
rolling_min_CI = df['CI'].rolling(63).min() < 38.2
back_above_40 = df['CI'] > 40
start_date, end_date = None, None

print(df.index)
print(start_date)
print(end_date)

for i, (high, cross, roll_min, back) in enumerate(zip(high_CI, crossed_618, rolling_min_CI, back_above_40)):
    start_date, end_date = None, None  # add this line
    start_date = pd.Timestamp(df.iloc[i].name)
    end_date = pd.Timestamp(df.iloc[i].name) + pd.DateOffset(days=1)
    if back:
        df.loc[start_date:end_date, 'trend'] = 1
    else:
        df.loc[start_date:end_date - pd.Timedelta(seconds=1), 'trend'] = 1
        # Convert to timestamp
        if back:
            df.loc[df.index.get_loc(start_date):df.index.get_loc(end_date + pd.DateOffset(days=1)), 'trend'] = 1
        else:
            start_pos = df.index.get_loc(start_date)
            end_pos = df.index.get_loc(end_date)
            df.loc[start_pos:end_pos, 'trend'] = 1

df.to_csv('EURUSD_choppiness_index.csv', index=False)
pd.DataFrame({'high_CI': high_CI, 'crossed_618': crossed_618, 'rolling_min_CI': rolling_min_CI, 'back_above_40': back_above_40}).to_csv('trend_indicators.csv', index=False)

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
