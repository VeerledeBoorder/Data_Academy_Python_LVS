# Download packages
from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Create new user with a username and an initial balance. Default initial balance is set to 10,000 virtual coins.

class User:
    def __init__(self, username, initial_balance=10000):
        self.username = username
        self.balance = initial_balance

    def subtract_funds(self, amount):
        if amount < 0:
            raise ValueError("Cannot subtract a negative amount.")
        if amount > self.balance:
            raise ValueError("Insufficient balance.")
        self.balance -= amount

    def get_balance(self):
        return self.balance

user = User("Seb")

"""
# Data Exploration

# Define URL for API and retrieving stock information
response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=MSFT&interval=5min&outputsize=full&apikey=4H4XGZE8HAY85MW6")

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
"""
def fetch_sp500_symbols():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_table = tables[0]  # The first table contains the S&P 500 list
    return sp500_table[['Symbol', 'Security']]  # We need only the stock symbols and company names

# Fetch and store the S&P 500 symbols and names
sp500_dataset = fetch_sp500_symbols()

def search_stock(sp500_dataset, query):
    matches = sp500_dataset[sp500_dataset['Security'].str.contains(query, case=False) |
                            sp500_dataset['Symbol'].str.contains(query, case=False)]
    return matches


def stock_selection():
    sp500_dataset = fetch_sp500_symbols()
    query = input("Enter the stock symbol or company name to search: ")
    matches = search_stock(sp500_dataset, query)

    # Check if there are matches
    if matches.empty:
        print("No matches found.")
        return None

    print("Search Results:\n", matches)

    # Let the user select a stock if multiple matches are found
    if len(matches) > 1:
        selected_index = int(input("Enter the index of the stock you want to select: "))
        selected_symbol = matches.iloc[selected_index]['Symbol']
    else:
        selected_symbol = matches.iloc[0]['Symbol']

    return selected_symbol

symbol = stock_selection()

def stock_preference(symbol):
    """Fetch stock data for a given symbol using Alpha Vantage API."""
    api_key = "4H4XGZE8HAY85MW6"  # This should be an environment variable or securely stored
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&outputsize=full&apikey={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Could not retrieve data, code:", response.status_code)

    raw_data = response.json()

    if "Time Series (5min)" not in raw_data:
        raise ValueError("Invalid stock symbol or no data available.")

    return raw_data




#I ask the user what stock they bought and when
StockChoice = symbol
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

"""# The service sends JSON data, we parse that into a Python datastructure
raw_data_symbol = response.json()
#I want to print the symbol of the 1st Best Match
symbol = raw_data_symbol['bestMatches'][0]['1. symbol']
print(f"The accompying symbol for {StockChoice} is {symbol}")
"""

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

# Calculate the profit or loss
profit_loss = (float(current_price) - float(historical_price)) * number_of_stocks
# Calculate the original investment
original_investment = float(historical_price) * number_of_stocks
# Calculate the profit or loss percentage
profit_loss_percentage = round((profit_loss / original_investment) * 100, 2)
# Check if the result is positive or negative
if profit_loss > 0:
    print(f"You made a profit of: {profit_loss} which is a {profit_loss_percentage}% gain.")
else:
     print(f"You incurred a loss of: {-profit_loss} which is a {-profit_loss_percentage}% loss.")

# Check the final balance for the specific user
final_balance = user.balance-profit_loss
print(f"The current balance is: {final_balance}")

# Create line graph to show balance at the beginning and the and
plt.plot(['Time of Purchase', 'Current Time'], [user.balance, final_balance])
plt.xlabel('Time')
plt.ylabel('Balance')
plt.title('Line Graph of Balance Over Time')
plt.show()

# Create line graph to show stock prices at the beginning and the and
plt.plot(['Time of Purchase', 'Current Time'], [historical_price, current_price])
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.title('Line Graph of Stock Price Over Time')
plt.show()

