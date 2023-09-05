import pandas as pd

# Load the two CSV files into pandas DataFrames
df1 = pd.read_csv('movie_names18.0.csv')
df2 = pd.read_csv('movie_names_fin.csv')

# Concatenate the two dataframes along axis=0 (which means vertically)
combined_df = pd.concat([df1, df2], axis=0)

# If you want to save the combined dataframe as a new CSV file
combined_df.to_csv('imdb_all.csv', index=False)