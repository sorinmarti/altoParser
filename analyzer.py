import pandas as pd
import numpy as np
import os
import csv

# create a dataframe from the csv files in the output_1922 folder
def create_dataframe():
# create a list of all the files in the output_1922 folder
    files = os.listdir('output_1922')
    # create a list of all the csv files in the output_1922 folder
    csv_files = [file for file in files if file.endswith('.csv')]
    # create a list of all the dataframes from the csv files
    dataframes = [pd.read_csv('output_1922/' + file) for file in csv_files]
    # create a dataframe from the list of dataframes
    df = pd.concat(dataframes)
    return df
    print(df)
