import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
import fuzzy_pandas as fpd

def func_one():
    char_df = pd.read_csv('characters_all.csv')
    imdb_df = pd.read_csv('imdb_all.csv')

    char_df.drop_duplicates(inplace=True)
    char_df = char_df[char_df['mbti'] != 'XXXX']
    char_df['temp_info'] = char_df['movie'].str.extract('\((.*?)\)', expand=False)
    char_df['movie'] = char_df['movie'].str.replace(r"\(.*\)", "", regex=True)
    char_df['year'] = char_df['temp_info'].str.extract('(\d{4})', expand=False)
    char_df['year'] = pd.to_numeric(char_df['year'], errors='coerce')
    char_df['notes'] = np.where(char_df['temp_info'].str.isdigit(), np.nan, char_df['temp_info'])
    char_df.drop('temp_info', axis=1, inplace=True)

    char_df['movie'] = char_df['movie'].str.lower().str.strip()
    imdb_df['movie'] = imdb_df['movie'].str.lower().str.strip()

    char_df.to_csv("characters_all_v2.csv", index=False)
    imdb_df.to_csv("imdb_all_v2.csv", index=False)

    #merged_df = fpd.fuzzy_merge(char_df, imdb_df, left_on='movie', right_on='movie', method='levenshtein', threshold=0.8)
    merged_df = pd.merge(char_df, imdb_df, on=['movie', 'year'], how='outer') # change 'outer' to 'inner' if you want only matching rows


    print(merged_df)

    merged_df.to_csv("merged_data_v5.csv", index=False)

def func_two():
    df = pd.read_csv('merged_data_v5.csv')
    df_good = df.dropna(subset=[col for col in df.columns if col != 'notes'])
    df_bad = df[df.drop('notes', axis=1).isna().any(axis=1)]

    df_good.to_csv("matched_data_v2.csv", index=False)
    df_bad.to_csv("unmatched_data_v2.csv", index=False)


func_two()