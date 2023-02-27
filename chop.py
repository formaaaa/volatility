import numpy as np
import pandas as pd


def adder(Data, times):
    for i in range(1, times + 1):
        z = np.zeros((len(Data), 1), dtype=float)
        Data = np.append(Data, z, axis=1)
    return Data


def deleter(Data, index, times):
    for i in range(1, times + 1):
        Data = np.delete(Data, index, axis=1)
    return Data


def jump(Data, jump):
    Data = Data[jump:, ]

    return Data


def ma(Data, lookback, what, where):
    for i in range(len(Data)):
        try:
            Data[i, where] = (Data[i - lookback + 1:i + 1, what].mean())

        except IndexError:
            pass

    return Data


def ema(Data, alpha, lookback, what, where):
    # alpha is the smoothing factor
    # window is the lookback period
    # what is the column that needs to have its average calculated
    # where is where to put the exponential moving average

    alpha = alpha / (lookback + 1.0)
    beta = 1 - alpha

    # First value is a simple SMA
    Data = ma(Data, lookback, what, where)

    # Calculating first EMA
    Data[lookback + 1, where] = (Data[lookback + 1, what] * alpha) + (Data[lookback, where] * beta)
    # Calculating the rest of EMA
    for i in range(lookback + 2, len(Data)):
        try:
            Data[i, where] = (Data[i, what] * alpha) + (Data[i - 1, where] * beta)

        except IndexError:
            pass
    return Data


def ATR(Data, lookback, high, low, close, where):
    # From exponential to smoothed moving average
    lookback = (lookback * 2) - 1
    # True Range
    for i in range(len(Data)):
        try:
            Data[i, where] = max(Data[i, high] - Data[i, low],
                                 abs(Data[i, high] - Data[i - 1, close]),
                                 abs(Data[i, low] - Data[i - 1, close]))

        except ValueError:
            pass

    Data[0, where] = 0
    Data = ema(Data, 2, lookback, where, where + 1)
    Data = deleter(Data, where, 1)
    Data = jump(Data, lookback)
    return Data


def choppiness_index(Data, lookback, high, low, where):
    # Calculating the Sum of ATR's
    for i in range(len(Data)):
        Data[i, where] = Data[i - lookback + 1:i + 1, 4].sum()

        # Calculating the range
    for i in range(len(Data)):
        try:
            Data[i, where + 1] = max(Data[i - lookback + 1:i + 1, 1] - min(Data[i - lookback + 1:i + 1, 2]))
        except:
            pass
    # Calculating the Ratio
    Data[:, where + 2] = Data[:, where] / Data[:, where + 1]

    # Calculate the Choppiness Index
    for i in range(len(Data)):
        Data[i, where + 3] = 100 * np.log(Data[i, where + 2]) * (1 / np.log(lookback))
    # Cleaning
    Data = deleter(Data, 5, 3)

    return Data


df = pd.read_csv("data/XAUUSD/XAUUSD1440.csv",
                 names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
df.set_index('date', inplace=True)
df.drop(columns=['time', 'volume'], inplace=True)

my_data = df.to_numpy()
my_data = ATR(my_data, 14, 1, 2, 3, 4)
#np.savetxt('test.txt', my_data, delimiter=',')

# Adding a few columns
my_data = adder(my_data, 10)
#print(my_data)
# Calculating a 20-period ATR
my_data = ATR(my_data, 20, 1, 2, 3, 4)
#print(my_data)

# Calculating the Sum of ATR's (atr_col is the index where the ATR is stored, in our example, it is 4)
for i in range(len(my_data)):
  my_data[i, where] = my_data[i - lookback + 1:i + 1, atr_col].sum()

my_data = choppiness_index(my_data, 20, 1, 2, 4)
