import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt


def get_max_min(prices, smoothing, window_range):
    smooth_prices_high = prices['high'].rolling(window=smoothing).mean().dropna()
    smooth_prices_low = prices['low'].rolling(window=smoothing).mean().dropna()
    local_max = argrelextrema(smooth_prices_high.values, np.greater)[0]
    local_min = argrelextrema(smooth_prices_low.values, np.less)[0]
    price_local_max_dt = []
    for i in local_max:
        if (i > window_range) and (i < len(prices) - window_range):
            price_local_max_dt.append(prices.iloc[i - window_range:i + window_range]['high'].idxmax())
    price_local_min_dt = []
    for i in local_min:
        if (i > window_range) and (i < len(prices) - window_range):
            price_local_min_dt.append(prices.iloc[i - window_range:i + window_range]['low'].idxmin())
    maxima = pd.DataFrame(prices.loc[price_local_max_dt])
    minima = pd.DataFrame(prices.loc[price_local_min_dt])
    max_min = pd.concat([maxima, minima]).sort_index()
    max_min.index.name = 'date'
    # max_min = max_min.reset_index()
    max_min = max_min[~max_min.date.duplicated()]
    p = prices  # .reset_index()
    max_min['day_num'] = p[p['date'].isin(max_min.date)].index.values
    max_min = max_min.set_index('day_num')['close']

    return max_min


smoothing = 3
window = 15

resampled_data = pd.read_csv('EURUSD.csv')

minmax = get_max_min(resampled_data, smoothing, window)
print(minmax)

resampled_data.reset_index()['close'].plot()
plt.scatter(minmax.index, minmax.values, color='orange', alpha=.5)
plt.savefig('EURUSD_HL.png')
plt.show()
