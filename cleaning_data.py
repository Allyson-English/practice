import pandas as pd
import numpy as np
import csv

# Read in full path starting with '/Users...' if the file is not in the present working directory

path = **FILE PATH HERE**

# Read in dataset and display first 5 rows
# Get a sense of what has commonly been input for missing data (Na, --, NaN, etc)

dataset = pd.read_csv(path)
dataset.head(10)

# Create a list of missing values and re-read in the dataset 
# Set na_values equal to list of missing values to ensure non-standard missing values are read in correctly

missing_values = ["n/a", "na", "--", "NaN"]
dataset = pd.read_csv(path, na_values = missing_values)

# Determine what the data type in each column is
# If available, crosscheck this against a list of what the expected value type is
# If expected value types are not available:
# use intutition to determine if column header suggests a consistent variable type with what is found

dataset.dtypes

# This will return a boolean value indicating whether any null values exist in the dataset
print(dataset.isnull().values.any())

# This will return the total sum of null values identified
print(dataset.isnull().sum().sum())

# This will indicate how many values in a given column are a standard null value
# Note that this will not indicate whether the value included is incorrect 

dataset.isnull().sum()


# Replacing values where a character has been input but an int or float is expected
# Note: be sure to adjust int or float as needed

cnt = 0

for row in dataset['NUM_BATH']:
    try:
        float(row)
    except ValueError:
        dataset.loc[cnt, 'NUM_BATH'] = np.nan
    cnt += 1
    
    
# Replacing values where a number has been input but characters were expected

cnt = 0

for row in dataset['OWN_OCCUPIED']:
    try:
        float(row)
        dataset.loc[cnt, 'OWN_OCCUPIED'] = np.nan
    except ValueError:
        pass
    cnt += 1


# Replacing null values in number columns with median value

median_beds = dataset['NUM_BEDROOMS'].median()
median_baths = dataset['NUM_BATH'].median()
median_sqft = dataset['SQ_FT'].median()


dataset['NUM_BEDROOMS'].fillna(median_beds, inplace=True)
dataset['NUM_BATH'].fillna(median_baths, inplace=True)
dataset['SQ_FT'].fillna(median_sqft, inplace=True)
