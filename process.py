import os
import pandas as pd

# Define the folder containing the CSV files
folder_path = 'crawl'

# List to hold dataframes
dfs = []

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        # Read the CSV file into a dataframe
        df = pd.read_csv(file_path)
        # Drop the 'page' and 'name' columns
        df = df.drop(columns=['page', 'name', 'link', 'image'])
        # Append the dataframe to the list
        dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined dataframe to a new CSV file
combined_df.to_csv('combined.csv', index=False)