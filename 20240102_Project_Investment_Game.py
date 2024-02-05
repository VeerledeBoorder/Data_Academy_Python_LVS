# Download packages
from datetime import datetime
import requests
import pandas as pd


# Data Exploration

# Define URL for API and retrieving stock information
# response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=4H4XGZE8HAY85MW6")

# Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
#if response.status_code != 200:
    #raise ValueError("Could not retrieve data, code:", response.status_code) #get an error?

# The service sends JSON data, we parse that into a Python datastructure    
# raw_data = response.json()

# Exploration of the data
# print(raw_data)

# print(type(raw_data))
# print(raw_data.keys())
 

# Creating a dataframe with stock prices
#data = raw_data['Time Series (5min)']
#df = pd.DataFrame(data).T.apply(pd.to_numeric)
#print(df.info())
#print(df.head())

# Set index
#df.index = pd.DatetimeIndex(df.index)

# Rename columns
#df.rename(columns=lambda s: s[3:], inplace=True)

# End of data exploration

##Part Veerle
# Create dataframe with available stocks
available_stocks = ['MFST', 'APPL'] # Fill tomorrow with more stocks

# Ask stock preference
#def stock_preference():
   # while True:
     #   desired_stock = input("What stock do you want")
     #   if desired_stock.upper() in available_stocks:
       #     return desired_stock.upper()
      #  else:
        #    print("That stock is not available. Please try again.")

# Call the function
#chosen_stock = stock_preference()
#print(chosen_stock)
            

   

# Start of program
    


#I ask the user what stock they bought and when
StockChoice = input ("What stock did you buy?")
# Asks how many stocks the user want to buy (volume)
# num_stocks = int(input("How many stocks did you buy? "))
def amount_stocks():
    while True:
        try:
            num_stocks = int(input("How many stocks did you buy? "))
            if num_stocks < 0:
                print("The number of stocks cannot be negative. Please enter again.")
                continue
            return num_stocks
        except ValueError:
            print("Invalid input. Please enter a number.")

# Call the function
number_of_stocks = amount_stocks()
print(number_of_stocks)  


# Now I include the name of the company in the URL with the objective of retreiving the symbol
response = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' + StockChoice + '&outputsize=full&apikey=4H4XGZE8HAY85MW6')
# Since we are retrieving stuff from a web service, it's a good idea to check for the return status code
# See: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
if response.status_code != 200:
    raise ValueError("Could not retrieve data, code:", response.status_code)

# The service sends JSON data, we parse that into a Python datastructure
raw_data_symbol = response.json()
#I want to print the symbol of the 1st Best Match
symbol = raw_data_symbol['bestMatches'][0]['1. symbol']
print(f"The accompying symbol for {StockChoice} is {symbol}")

# Asks when the user bought the stocks (time)
#time_purchase = input("When did you buy your stock?")
def ask_purchase_date():
    while True:
        date_str = input("Enter the date you bought the stocks (yyyy-mm-dd): ")
        try:
            purchase_date = datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("That's not a valid date. Please enter a date in 'yyyy-mm-dd' format.")

while True:
    # Call the function
    date_purchase = ask_purchase_date()

    # We want to retrieve historical stock prices
    historical_response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ symbol+ '&outputsize=full&apikey=4H4XGZE8HAY85MW6')
    # The service sends JSON data, we parse that into a Python data structure
    raw_data_date_purchase = historical_response.json()

    # Check if date exists in database
    try:
        historical_price = raw_data_date_purchase["Time Series (Daily)"][date_purchase]["2. high"]
        print(f"The historical price of {StockChoice} on {date_purchase} is: {historical_price}")
        break
    except KeyError:
        print("The entered date does not exist in the database. Please enter a different date.")
# We want to retrieve historical stock prices
historical_response = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ symbol+ '&outputsize=full&apikey=4H4XGZE8HAY85MW6')
# The service sends JSON data, we parse that into a Python datastructure
raw_data_date_purchase = historical_response.json()


#I want to print the symbol of the 1st Best Match
historical_price = raw_data_date_purchase["Time Series (Daily)"][date_purchase]["2. high"]
print(f"The historical price of {StockChoice} is: {historical_price}")
   
#use the symbol to create a request to get the current price
now_response = requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+ symbol+ '&outputsize=full&apikey=4H4XGZE8HAY85MW6')
# The service sends JSON data, we parse that into a Python datastructure
raw_data_price = now_response.json()
#Now I print the current price of the chosen stock
current_price = raw_data_price['Global Quote']['05. price']
print(f"The current price of {StockChoice} is: {current_price}")








    