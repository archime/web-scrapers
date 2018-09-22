"""
Web scraper for crypto prices from Coinmarketcap.com
First attempt. Refactor could pull from main page once and get all prices.
"""

# Web scraping packages

import urllib.request
from bs4 import BeautifulSoup

# Global variables

TICKER_LOOKUP = {'BTC': 'bitcoin',
                 'ETH': 'ethereum',
                 'XRP': 'ripple',
                 'BCH': 'bitcoin-cash',
                 'BCC': 'bitcoin-cash',
                 'EOS': 'eos'}

# Helper functions

def get_crypto_price(ticker):
    """
    Takes string of cryptocurrency ticker symbol as input, returns price from Coinmarketcap if available
    """
    
    if ticker not in TICKER_LOOKUP.keys():
        return 'ERROR: Ticker ' + str(ticker) + ' not in TICKER_LOOKUP'
    else:
        ticker_string = TICKER_LOOKUP[ticker]
        
    coinmarketcap_raw = urllib.request.urlopen('https://coinmarketcap.com/currencies/' + ticker_string + '/#markets').read()
    coinmarketcap_parsed = BeautifulSoup(coinmarketcap_raw, 'html.parser') 
    
    for span in coinmarketcap_parsed.select('span'):
        if 'id' in span.attrs:
            if 'data-usd' in span.attrs:
                return span['data-usd']
            
def run_price_report(ticker_list):
    """
    Given list of crypto tickers, prints tickers and current price from Coinmarketcap.com
    """
    for ticker in ticker_list:
        price = get_crypto_price(ticker)
        print("Ticker: " + str(ticker) + ", Price: " + str(price))
    return None
            
# Run program

run_price_report(['BTC', 'ETH', 'XRP', 'BCH', 'EOS'])