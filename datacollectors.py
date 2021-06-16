# Standard Imports
import json
import numpy as np
import urllib.request
from requests import Request, Session

# API Imports
import quandl
import yfinance as yf
from Historic_Crypto import HistoricalData

# Init Global Dictionary of API Keys and other sensitive information
# External File 'keys.json' containing this information will not be included in public repo
global keys
with open('keys.json') as file:
    keys = json.load(file)

# Crypto Quant Agent
class coin_market_cap_agent():

    def __init__(self):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {'start':'1', 'limit':'5000', 'convert':'USD'}
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': keys['coin_market_cap_api_key']}
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
        self.data = json.loads(response.text)

# Nomics Agent
class nomics_api_agent():

    def __init__(self):
        url = "https://api.nomics.com/v1/volume/history?key=" + keys['nomics_api_key'] + "&start=2018-04-14T00%3A00%3A00Z&end=2018-05-14T00%3A00%3A00Z&convert=EUR"
        #print(urllib.request.urlopen(url).read())

# Historic Crypto Agent Class
class crypto_history_agent():

    def __init__(self):
        pass

    def gather_data(self, coin):
        return HistoricalData(coin + '-USD',86400,'2010-01-01-00-00').retrieve_data()

# Quandl Agent Class
class quandl_agent():

    def __init__(self):
        quandl.ApiConfig.api_key = keys['quandl_api_key']
        self.bond_yields = quandl.get("USTREASURY/YIELD").dropna(how='all')
        self.unemployment = quandl.get("FRED/NROUST").dropna(how='all')
        self.nominal_gdp = quandl.get("FRED/NGDPPOT").dropna(how='all')
        self.real_gdp = quandl.get("FRED/GDPPOT").dropna(how='all')
        self.consumer_sentiment = quandl.get("UMICH/SOC1").dropna(how='all')

    def update(self):
        self.bond_yields = quandl.get("USTREASURY/YIELD").dropna(how='all')
        self.unemployment = quandl.get("FRED/NROUST").dropna(how='all')
        self.nominal_gdp = quandl.get("FRED/NGDPPOT").dropna(how='all')
        self.real_gdp = quandl.get("FRED/GDPPOT").dropna(how='all')
        self.consumer_sentiment = quandl.get("UMICH/SOC1").dropna(how='all')

# YFinance Agent Class
class yfin_agent():

    def __init__(self):
        pass

    def gather_data(self, ticker):
        return yf.Ticker(ticker)
