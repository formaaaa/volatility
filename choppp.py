import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

df.to_csv('EURUSD_choppiness_index.csv')

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex='all', figsize=(12, 8))

ax1.plot(df.index, df['close'])
ax1.set_ylabel('Price')

ax2.plot(df.index, df['CI'], color='green')
ax2.set_ylabel('Choppiness Index')

# set x-axis date formatter to display only years
years = mdates.YearLocator()   # every year
years_fmt = mdates.DateFormatter('%Y')
ax2.xaxis.set_major_locator(years)
ax2.xaxis.set_major_formatter(years_fmt)

plt.show()
