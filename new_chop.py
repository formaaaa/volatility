import pandas as pd
import numpy as np

df = pd.read_csv("data/USDJPY/USDJPY1440.csv", names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
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

lenght = 22
start_date = None
mid_date = None

# Find periods of trending market
for i in range(1, len(df)):
    if df['CI'].iloc[i] < 61.8 <= df['CI'].iloc[i - 1]:
        start_date = df.index[i]
        mid_date = None
    elif df['CI'].iloc[i] < 38.2 and start_date is not None and mid_date is None:
        for j in range(i + 1, min(i + lenght + 1, len(df))):
            if df['CI'].iloc[j] > 38.2:
                mid_date = df.index[j]
                break
        if mid_date is not None:
            for j in range(j + 1, min(j + lenght + 1, len(df))):
                if df['CI'].iloc[j] < 61.8:
                    end_date = df.index[j]
                    df.loc[start_date:end_date, 'trend'] = 1
                    start_date = None
                    mid_date = None
                    break
    elif df['CI'].iloc[i] > 38.2 and mid_date is not None:
        mid_date = None

df.to_csv('USDJPY_choppiness_index_new.csv')
