import pandas as pd

# Define a list of file names to read
file_names = ['XAUUSD_choppiness_index_new_amended.xlsx', 'EURUSD_choppiness_index_new_amended.xlsx', 'GBPUSD_choppiness_index_new_amended.xlsx', 'USDJPY_choppiness_index_new_amended.xlsx']

# Define a list of dataframes
dfs = []

# Loop over the file names and read in the data
for file_name in file_names:
    df = pd.read_excel(file_name)
    dfs.append(df[['date', 'trend']])

# Concatenate the dataframes
combined_df = pd.concat(dfs)

# Filter for trend = 0 or trend = 1
trends_df = combined_df[combined_df['trend'].isin([0, 1])]

# Remove duplicates
trends_df = trends_df.drop_duplicates()

# Filter for trend = 1
trends_df = trends_df[trends_df['trend'] == 1]

# Save to csv
trends_df.to_csv('trends_overlapping_top4_1.csv', index=False)
