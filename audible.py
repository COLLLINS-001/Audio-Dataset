import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# Load the audible_raw.csv file
audible = pd.read_csv('data/audible_raw.csv')

audible['author'] = audible['author'].str.replace('Writtenby:', '')
audible['narrator'] = audible['narrator'].str.replace('Narratedby:', '')

audible.stars.replace('Not rated yet', np.nan, inplace=True)

# Extract number of stars into rating_stars and turn into float
audible['rating_stars']= audible['stars'].str.extract('^([\d.]+)').astype(float)

# Replace the comma, extract number of ratings into n_ratings and turn into float
audible['n_ratings']= audible['stars'].str.replace(',', '').str.extract('(\d+) rating').astype(float)

# Drop the stars column
audible.drop('stars', axis=1, inplace=True)

# Explore the price column
# Replace the comma with ''
audible['price'] = audible.price.str.replace(',', '')

# Replace 'Free' with 0
audible['price'] = audible.price.str.replace('Free', '0')
# Turn price to float
audible['price']= audible['price'].astype(float)

audible['rating_stars']= audible['rating_stars'].astype('category')
#audible['releasedate']= pd.to_datetime(audible['releasedate'], format='yyyy-mm-dd')

# Replace hrs, mins, and 'Less than 1 minute'
audible['time'] = audible['time'].str.replace('hrs', 'hr')
audible['time'] = audible['time'].str.replace('mins', 'min')
audible['time'] = audible['time'].str.replace('Less than 1 minute', '1 min')

# Extract the number of hours, turn to integer
hours = audible['time'].str.extract('(\d+) hr').fillna(0).astype(int)

# Extract the number of minutes, turn to integer
mins = audible['time'].str.extract('(\d+) min').fillna(0).astype(int)

# Combine hours and minutes into the time_mins column
audible['time_mins'] = 60 * hours + mins

audible.drop('time', axis=1, inplace=True)

# Plot histograms of all the numerical columns
#audible.hist(figsize=(10,10), bins=100)
#plt.show()

# Look at the numeric columns
#audible.describe()

# Look at the non numeric columns
#audible.describe(exclude=[np.number])

# Transform prices to USD (multiply times 0.012)
audible['price'] = audible.price * 0.012

# Look for duplicate rows
audible['language'] = audible['language'].str.capitalize()

# Create a list of our subset columns and assign to subset_cols
subset_cols = ['name', 'author', 'narrator', 'time_mins', 'price']

# Check for duplicates using our subset of columns
audible.duplicated(subset=subset_cols).sum()
# Check the duplicated rows keeping the duplicates and order by the name column
#print(audible[audible.duplicated(subset=subset_cols, keep=False)].sort_values(by=['name']))

# Drop duplicated rows keeping the last release date
audible.drop_duplicates(subset=subset_cols, keep='last', inplace=True)
# Check again for duplicates using our subset of columns
#print(audible[audible.duplicated(subset=subset_cols, keep=False)].sort_values(by=['name']))

# Check for null values
#print(audible.isna().sum())

audible.to_csv('data/audible_cleaned.csv', index=False)

#print(audible['time_mins'].head(10))

#audible['time']=audible['time'].str.replace('category')


#print(audible.head())