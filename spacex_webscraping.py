# required modules
import sys
import requests
import re
import unicodedata
from bs4 import BeautifulSoup
import pandas as pd

def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell 
    Input: the  element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    colunm_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name    
    
'''
To keep the lab tasks consistent, you will be asked to scrape the 
data from a snapshot of the List of Falcon 9 and Falcon Heavy 
launches Wikipage updated on 9th June 2021
'''
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

'''
use requests.get() method with the provided static_url
assign the response to a object
'''
response = requests.get(static_url)

# use BeautifulSoup() to fetch html data
soup = BeautifulSoup(response.text, 'html.parser')

# store all tables in 'html_tables' variable
html_tables = soup.find_all('table')

# print the second table and check its content; store it to first_launch_table
''' Variables: 
            Flight No., Date and time ( ), Launch site, Payload, 
            Payload mass, Orbit, Customer, Launch outcome 
'''

column_names = []
firstLaunch_table = html_tables[2]
th = firstLaunch_table.find_all('th')

for n in range(0, 15):
    name = extract_column_from_header(th[n])
    if name != None and len(name) > 0:
        column_names.append(name)
        
'''
create a hashtable with empty arrays for values, use variable names
we will store values into arrays by webscraping data via Wiki
'''
launch_dict = dict.fromkeys(column_names)
# Let's initial the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Launch site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
# Added some new columns
launch_dict['Version Booster']=[]
launch_dict['Booster landing']=[]
launch_dict['Date and time ( )'] = []

# webscraping launch data (2010 - 2013)
i = 8
n = 0
while n <= 73:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[2].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    
    elif n != 39:
        n+=1
        i += 10
    
    else:
        if n == 39:
            n += 5
            i += 5
            
# webscraping launch data (2014)
i = 8
n = 0
while n <= 58:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[3].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    
    else:
        n+=1
        i += 10
        
# webscraping launch data (2015) 
i = 8
n = 0
while n <= 68:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[4].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    else:
        n+=1
        i += 10
        
# webscraping launch data (2016)
i = 8
n = 0
while n <= 88:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[5].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    
    else:
        n+=1
        i += 10
        
# webscraping launch data (2017) 
i = 8
n = 0
while n <= 178:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[6].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    
    else:
        n+=1
        i += 10
# webscraping launch data (2018)    
i = 8
n = 0
while n <= 212:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[7].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    
    elif n != 29:
        n+=1
        i += 10
   
    else:
        n += 5
        i += 14
# webscraping launch data (2019)
n = 0
i = 8
while n <= 136:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                    'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                    'Customer', 'Launch outcome', 'Booster landing']:
            if n > 136:
                break
            name = html_tables[8].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n+=1
    
    elif n == 39 or n == 83:
        n+=5
        i+=14
    
    else:
        n+=1
        i+=10
# webscraping launch data (2020)   
i = 8
n = 0
while n <= 258:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[9].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    
    else:
        n+=1
        i += 10
# webscraping launch data (2021)   
i = 8
n = 0
while n <= 178:
    if n <= i:
        for col in ['Date and time ( )', 'Version Booster', 
                      'Launch site', 'Payload', 'Payload mass', 'Orbit', 
                      'Customer', 'Launch outcome', 'Booster landing']:
            name = html_tables[10].tbody.find_all('td')[n].text.strip()
            launch_dict[col].append(name)
            n += 1
    
    else:
        n+=1
        i += 10

# now that data is scraped, create a dataframe object from our new webscraped hashtable
del launch_dict['Flight No.']
df = pd.DataFrame(launch_dict)

# df is created and ready for Data Wrangling
df.head()

# save dataframe object as a csv if you do not wish to start wrangling
df.to_csv('spacex_web_scrapedV3.csv', index=False)
