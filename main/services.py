
import pandas as pd

def csv_to_df(file_uploaded, columns):
    df = pd.read_csv(file_uploaded,
                     usecols=columns)
    if df.isnull().values.any():
        raise Exception("Found a null value, please re-upload")
    return df
