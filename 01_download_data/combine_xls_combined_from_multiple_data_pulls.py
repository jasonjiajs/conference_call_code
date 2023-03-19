import pandas as pd
from pathlib import Path
import os, sys, glob

inputfilepath1 = Path(sys.argv[1])
inputfilepath2 = Path(sys.argv[2])
outputfilepath = Path(sys.argv[3])

# Load in files
print("Reading in df1:", inputfilepath1)
df1 = pd.read_csv(inputfilepath1, low_memory=False)
print("Reading in df2:", inputfilepath2)
df2 = pd.read_csv(inputfilepath2, low_memory=False)

# Drop the last column '0' which contains no information if it is present:
if df1.columns[-1] == '0':
    df1 = df1.drop(columns=['0'])
if df2.columns[-1] == '0':
    df2 = df2.drop(columns=['0'])

# Rename first column ('Unnamed: 0') as 'index'
df1 = df1.rename(columns = {'Unnamed: 0': 'index'})
df2 = df2.rename(columns = {'Unnamed: 0': 'index'})

# Confirm that the 2 dfs have the same columns
assert(df1.columns.tolist() == df2.columns.tolist())

# Combine the 2 dfs
df = pd.concat([df1, df2])
print("Number of rows of df1:", df1.shape[0])
print("Number of rows of df2:", df2.shape[0])
print("Number of rows of df:", df.shape[0])
assert(df1.shape[0] + df2.shape[0] == df.shape[0])
print("df.columns:", df.columns)

# Drop duplicates (if any)
df = df.drop_duplicates(subset=df.columns.drop('index'))
print("Number of rows of df (after dropping duplicates):", df.shape[0])

# Save df to .csv
df.to_csv(outputfilepath, index=False)
print("Saved df to:", outputfilepath)