'''
Data Wrangling Webscraped Data:
    Objective is to format, clean, and fill webscraped data.
    Remove Noise from all columns in the dataframe; 
        i.e. unnecessary brackets, parentheses, ect
    Spot ambiguity between values and format them respectively
    Fill empty values; NaN values are filled with average of the respective column
'''
# import required modules
import numpy as np
import pandas as pd

path = 'spacex_web_scrapedV3.csv'
df = pd.read_csv(path)

# understand the variables and values that need attention; i.e. wrangling
df.head()

# datatypes of each variable
df.dtypes

# fomatting variable names to PamelCase, as well as removing spaces
df.columns = df.columns.str.strip().str.title().str.replace(' ', '_', regex = True)
df.columns = df.columns.str.strip().str.replace('(\_)', '', regex = True)
df.columns = df.columns.str.strip().str.replace('(\(\))', '', regex = True)
# dropping variables: Payload, Customer, LaunchOutcome
df.drop(columns = ['Payload', 'Customer', 'LaunchOutcome'], inplace = True)
df.rename(columns = {'BoosterLanding':  'Outcome', 
                     'PayloadMass': 'PayloadMass_kg'}, inplace = True)

'''
cleaning rows & formatting data that contain noise; i.e. brackets, 
        unstructured paradigms, ect
'''
# remove brackets from DataTime Column
for n in ['(\[\d\d])', '(\[\d\d\d])', '(\(planned\))']:
    df.iloc[:, 0] = df.iloc[:, 0].str.replace(n,'', regex = True)

df.iloc[:, 0] = df.iloc[:, 0].str.replace('2020','2020,', regex = True)
df.iloc[:, 0] = df.iloc[:, 0].str.replace('2021','2021,', regex = True)
df.iloc[:, 0] = df.iloc[:, 0].str.replace(',,',',', regex = True)

# splitting time and date into separate columns
df[['Date', 'Time']] = df.iloc[:, 0].str.split(',', expand = True)
df.drop(columns = ['DateAndTime'], inplace = True)

# remove brackets from LaunchSite column
df.iloc[:, 0] = df.iloc[:, 0].str.replace('(\[\d\d\d])','', regex = True)

# cleaning and formatting Orbit column
df.iloc[:, 2] = df.iloc[:, 2].str.replace('(\[\d\d\d])','', regex = True)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('LEO (ISS)', 'ISS', regex = False)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('Polar orbit LEO', 'PO', regex = False)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('Polar LEO', 'PO', regex = False)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('Heliocentric0.99–1.67 AU(close to Mars transfer orbit)', 'HEO', regex = False)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('HEO for P/2 orbit', 'HEO', regex = False)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('HEO(Sun–Earth L1 insertion)','ES-L1', regex = False)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('LEO / MEO','VLEO', regex = False)
df.iloc[:, 2] = df.iloc[:, 2].str.replace('Sub-orbital', 'SO', regex = False)

'''
removing noise from Outcome column; turning values to categorical variables 
0 for Failure Landing, 1 for Successful Landing
'''
for n in ['(\[\d\d\d])', '(\[\d\d])', '(\[\d])', '(\[d\])', 
          '(\[i\])', '(\(drone ship\))', '(\(ground pad\))', 
          '(\(parachute\))', '(\(ocean\))']:
    df.iloc[:, 4] = df.iloc[:, 4].str.strip().str.replace(n,'', regex = True)

for n in ['Precluded', 'Uncontrolled', 
          'Failure', 'No attempt']:
    df.iloc[:, 4] = df.iloc[:, 4].str.strip().str.replace(n, '0', regex = True)

for n in ['Success', 'Controlled']:
    df.iloc[:, 4] = df.iloc[:, 4].str.strip().str.replace(n, '1', regex = True)

# stripping all values after 2 in column VersionBooster;
df.iloc[:, 3] = df.iloc[:, 3].str[:2]
# based off Wiki, Falcon Heavy uses three Falcon 9 (F9) boosters; for simplicity we will name Fa ---> Falcon 9
for n in ['Fa', 'F9']:
    df.iloc[:, 3] = df.iloc[:, 3].str.replace(n, 'Falcon 9', regex = True)

# stripping length to 10 due to the abundance of noise in column 'LaunchSite'
df.iloc[:, 1] = df.iloc[:, 1].str[:10]
for n in ['(\(\))', 'kg', ',', '\xa0', 'xa0 79', 
          '~', '–600', '(', ' 1', ' 79']:
    df.iloc[:, 1] = df.iloc[:, 1].str.strip().str.replace(n, '', regex = True)

df.iloc[:, 1] = df.iloc[:, 1].str.strip().str.replace('Classified', '0', regex = True)

df.iloc[:, 1] = df.iloc[:, 1].astype('float')

# na values before and after
print("Before: ", df.isna().sum())
mean = df.iloc[:, 1].mean()

df.iloc[:, 1].fillna(mean, inplace = True)
print("\nAfter: ", df.isna().sum())

# datatypes before and after
print("Before: \n", df.dtypes)

df.Outcome = df.Outcome.astype('int')
df.Date = pd.to_datetime(df['Date'])
df.drop(columns = 'Time', inplace = True)

print("\nAfter: \n", df.dtypes)

# flight number column, one flight per row
df['FlightNo'] = list(range(1, 126))

'''
four launch facilities: 
---- Cape Canaveral Space Launch Complex 40 (SLC-40)
---- Vandenberg Space Force Base Space Launch Complex 4E (SLC-4E)
---- Kennedy Space Center Launch Complex 39A (LC-39A)
'''
# format ambiguous values 
for n in ['CCSFS,SLC-40', 'Cape Canaveral,SLC-40', 'CCAFSSLC-40', 'CCAFS,SLC-40', 'Cape Canaveral,LC-40']:
    df.iloc[:, 0] = df.iloc[:, 0].str.strip().str.replace(n, 'CCAFS, SLC-40', regex = True)
df.iloc[:, 0].unique()

# number of launches on each site
df.groupby(['FlightNo'])['LaunchSite'].unique().value_counts(normalize=False)

# number and occurrences of each orbit
df.groupby(['FlightNo'])['Orbit'].unique().value_counts()

# calculate the number and occurrences of mission outcome per orbit type
outcome_perOrbit = pd.DataFrame(df.groupby(['Orbit'])['Outcome'].value_counts(normalize = True))
outcome_perOrbit['OrbitCount'] = pd.DataFrame(df.groupby(['Orbit'])['Outcome'].value_counts())
outcome_perOrbit

# convert post-data wrangled dataframe into csv for EDA
df.to_csv("spacex_data_wrangled_V5.csv", index=False)