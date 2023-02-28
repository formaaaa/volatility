import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

roll = 252 * 1
st_dev1 = 2
st_dev2 = 3
period = '1D'

df = pd.read_csv("data/EURUSD/EUR_USD_1D.csv",
                 names=['date', 'time', 'open', 'high', 'low', 'close', 'volume'])
df.set_index('date', inplace=True)
df.drop(columns=['time', 'volume'], inplace=True)

df['move'] = df['close'] - df['close'].shift()
df['abs_move'] = abs(df['close'] - df['close'].shift())
df['st_dev'] = df['move'].rolling(roll).std()
df['avg_move'] = df['abs_move'].rolling(roll).mean()
df['st_dev_move'] = abs(df['move'] / df['st_dev'])

df['pct_move'] = (df['close'] - df['close'].shift()) / df['close'].shift()
df['abs_pct_move'] = abs((df['close'] - df['close'].shift()) / df['close'].shift())
df['st_dev_pct'] = df['pct_move'].rolling(roll).std()
df['st_dev_pct_move'] = abs(df['pct_move'] / df['st_dev_pct'])

df['diff'] = df['high'] - df['low']
df['avg_diff'] = df['diff'].rolling(roll).mean()
df['avg_diff_multiple'] = df['diff'] / df['avg_diff']

df['2_st_dev_move'] = np.where(df['st_dev_move'] >= st_dev1, 1, 0)
df['3_st_dev_move'] = np.where(df['st_dev_move'] >= st_dev2, 1, 0)
df['2_st_dev_pct_move'] = np.where(df['st_dev_pct_move'] >= st_dev1, 1, 0)
df['3_st_dev_pct_move'] = np.where(df['st_dev_pct_move'] >= st_dev2, 1, 0)
df['2_mean_diff'] = np.where(df['avg_diff_multiple'] >= st_dev1, 1, 0)
df['3_mean_diff'] = np.where(df['avg_diff_multiple'] >= st_dev2, 1, 0)

df['2_st_dev_move_price'] = np.where(df['2_st_dev_move'] == 1, df['close'], np.NAN)
df['3_st_dev_move_price'] = np.where(df['3_st_dev_move'] == 1, df['close'], np.NAN)
df['2_st_dev_pct_move_price'] = np.where(df['2_st_dev_pct_move'] == 1, df['close'], np.NAN)
df['3_st_dev_pct_move_price'] = np.where(df['3_st_dev_pct_move'] == 1, df['close'], np.NAN)
df['2_mean_diff_move_price'] = np.where(df['2_mean_diff'] == 1, df['close'], np.NAN)
df['3_mean_diff_move_price'] = np.where(df['3_mean_diff'] == 1, df['close'], np.NAN)

df.index = pd.to_datetime(df.index)

# from_ts = '2019-12-31'
# df = df[(df.index > from_ts)]
# print(df)

df2_move = df.query("`2_st_dev_move` == 1")
print(df2_move)
df3_move = df.query("`3_st_dev_move` == 1")
df2_pct_move = df.query("`2_st_dev_pct_move` == 1")
df3_pct_move = df.query("`3_st_dev_pct_move` == 1")
df2_diff = df.query("`2_mean_diff` == 1")
df3_diff = df.query("`3_mean_diff` == 1")

with open('GBPUSD.txt', 'w') as f:
    f.write(df.to_string())
with open('GBPUSD_2st_dev_move.txt', 'w') as f:
    f.write(df2_move.to_string())
with open('GBPUSD_3st_dev_move.txt', 'w') as f:
    f.write(df3_move.to_string())
with open('GBPUSD_2st_dev_pct_move.txt', 'w') as f:
    f.write(df2_move.to_string())
with open('GBPUSD_3st_dev_pct_move.txt', 'w') as f:
    f.write(df3_move.to_string())
with open('GBPUSD_2mean_diff.txt', 'w') as f:
    f.write(df2_move.to_string())
with open('GBPUSD_3mean_diff.txt', 'w') as f:
    f.write(df3_move.to_string())

df.to_csv('GBPUSD.csv')
df2_move.to_csv('GBPUSD_2st_dev_move.csv')
df3_move.to_csv('GBPUSD_3st_dev_move.csv')
df2_pct_move.to_csv('GBPUSD_2st_dev_pct_move.csv')
df3_pct_move.to_csv('GBPUSD_3st_dev_pct_move.csv')
df2_diff.to_csv('GBPUSD_2mean_diff.csv')
df3_diff.to_csv('GBPUSD_3mean_diff.csv')

df[['close']].plot()
plt.xlabel('date', fontsize=18)
plt.ylabel('close', fontsize=18)
plt.scatter(df.index, df['2_st_dev_move_price'], color='purple', label='2_st', marker='^', alpha=1)
plt.savefig('GBPUSD_2st_dev_move.png')
plt.show()
df[['close']].plot()
plt.xlabel('date', fontsize=18)
plt.ylabel('close', fontsize=18)
plt.scatter(df.index, df['3_st_dev_move_price'], color='red', label='3_st', marker='v', alpha=1)
plt.savefig('GBPUSD_3st_dev_move.png')
plt.show()

df[['close']].plot()
plt.xlabel('date', fontsize=18)
plt.ylabel('close', fontsize=18)
plt.scatter(df.index, df['2_st_dev_pct_move_price'], color='purple', label='2_st', marker='^', alpha=1)
plt.savefig('GBPUSD_2st_dev_pct_move.png')
plt.show()
df[['close']].plot()
plt.xlabel('date', fontsize=18)
plt.ylabel('close', fontsize=18)
plt.scatter(df.index, df['3_st_dev_pct_move_price'], color='red', label='3_st', marker='v', alpha=1)
plt.savefig('GBPUSD_3st_dev_pct_move.png')
plt.show()

df[['close']].plot()
plt.xlabel('date', fontsize=18)
plt.ylabel('close', fontsize=18)
plt.scatter(df.index, df['2_mean_diff_move_price'], color='purple', label='2_st', marker='^', alpha=1)
plt.savefig('GBPUSD_2mean_diff.png')
plt.show()
df[['close']].plot()
plt.xlabel('date', fontsize=18)
plt.ylabel('close', fontsize=18)
plt.scatter(df.index, df['3_mean_diff_move_price'], color='red', label='3_st', marker='v', alpha=1)
plt.savefig('GBPUSD_3mean_diff.png')
plt.show()


"""
1. weekly data for the last 10 years on GBP, GBP, GBP, JPY
4. since when we have a new regimen?
*FED Funds rates started moving up in FEB 2022
*In July inflation searches in Google started rising steadily
3. hourly and 4h data for the last regime change
5. try to identify tops and bottoms and clear trends (maybe a move of a certain distance within some period of time
between tops and bottoms

2022 - most of the time VIX between 20-30
2021 - most of the time VIX below 20
2020 - pandemic
2019 - most of the time VIX below 20
2018 - 2/3 of the time below 20
2017 - most of the time below 15


"""
