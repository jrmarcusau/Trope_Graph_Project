import pandas as pd
import os


rootDir = 'characters'
dataframes = []

for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
        if fname.endswith('.csv'):  # check if the file is CSV
            print('\t%s' % fname)
            df = pd.read_csv(os.path.join(dirName, fname))  # read the csv file
            dataframes.append(df)  # append the dataframe to the list

# Concatenate all dataframes
combined_df = pd.concat(dataframes, axis=0)

# Save combined dataframe to csv
combined_df.to_csv('all_characters.csv', index=False)