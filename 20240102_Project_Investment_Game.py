# Hi Laura I am testing this file 
##
print("hello Laura")

# Download packages
import requests
import pandas as pd

# Define URL for API and retrieving stock information
response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=demo")

# Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code) #get an error?

# The service sends JSON data, we parse that into a Python datastructure    
raw_data = response.json()

# Exploration of the data
print(type(raw_data))
print(raw_data.keys())
print(raw_data['Meta Data'])

# Creating a dataframe
data = raw_data['Time Series (5min)']
df = pd.DataFrame(data).T.apply(pd.to_numeric)
df.info()
df.head()