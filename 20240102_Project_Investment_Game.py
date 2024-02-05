# Download packages
import requests
import pandas as pd

# Key Veerle
#key_Veerle = "FQJG0MA1QHQ7U9EL"

# Define URL for API and retrieving stock information
response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=FQJG0MA1QHQ7U9EL")

# Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code) #get an error?

# The service sends JSON data, we parse that into a Python datastructure    
raw_data = response.json()

# Exploration of the data
print(raw_data)

print(type(raw_data))
print(raw_data.keys())
 

# Creating a dataframe with stock prices
data = raw_data['Time Series (5min)']
df = pd.DataFrame(data).T.apply(pd.to_numeric)
print(df.info())
print(df.head())

# Set index
df.index = pd.DatetimeIndex(df.index)

# Rename columns
df.rename(columns=lambda s: s[3:], inplace=True)

# Create dataframe with available stocks
available_stocks = ['MFST', 'APPL'] # Fill tomorrow with more stocks

# Ask stock preference
def stock_preference(self):
    while True:
        desired_stock = input("What stock do you want")
        if desired_stock.upper() in available_stocks:
            return desired_stock.upper()
        else:
            print("That stock is not available. Please try again.")
            

# Asks how many stocks the user want to buy (volume)
def amount_stocks(self):
    while True:
        try:
            num_stocks = int(input("How many stocks do you want to buy? "))
            if num_stocks < 0:
                print("The number of stocks cannot be negative. Please enter again.")
                continue
            return num_stocks
        except ValueError:
            print("Invalid input. Please enter a number.")


