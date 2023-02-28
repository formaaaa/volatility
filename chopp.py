import numpy as np
import pandas as pd

# Define the period
period = 14

# Load the data into a Pandas dataframe
data = pd.read_csv("data/EURUSD/EURUSD1440.csv",
                   names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
data.set_index('date', inplace=True)
data.drop(columns=['time', 'volume'], inplace=True)

data_norm = (data - data.min()) / (data.max() - data.min())


# Calculate the True Range (TR)
data['TR'] = np.maximum(data['high'] - data['low'], np.abs(data['high'] - data['close'].shift(1)),
                        np.abs(data['low'] - data['close'].shift(1)))

# Calculate the Average True Range (ATR)
data['ATR'] = data['TR'].rolling(period).mean()

# Calculate the Normalized ATR (NATR)
data['NATR'] = data['ATR'] / data['close']

# Calculate the choppiness index
denominator = np.abs(data['high'].rolling(period).max() - data['low'].rolling(period).min())
data['CHOP'] = 100 * np.log10(
    np.maximum(data['ATR'].rolling(period, min_periods=1).sum(), 0.0001) /
    np.abs(data['high'].rolling(period, min_periods=1).max() - data['low'].rolling(period, min_periods=1).min())
)


# Print the last 10 rows of the data
print(data.tail(10))

data.to_csv('EURUSD_chop.csv')

