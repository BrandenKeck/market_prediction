# Standard Imports
import json
import requests
import numpy as np

# Stock Model Imports
import yfinance as yf
import quandl

# Crypto Model Imports
from coinbase.wallet.client import Client
from Historic_Crypto import HistoricalData

# Webscraper Imports
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Reddit Scraper Imports
import praw

# Database Library Imports
from firebase import Firebase

# Init Global Dictionary of API Keys and other sensitive information
# External File 'keys.json' containing this information will not be included in public repo
global keys
with open('keys.json') as file:
    keys = json.load(file)

# Database Handling Class
class itfdb():

    # Connect to firebase dataset
    def __init__(self):
        self.config = {
                  "apiKey": keys['firebase_api_key'],
                  "authDomain": keys['firebase_auth_domain'],
                  "databaseURL": keys['firebase_address'],
                  "storageBucket": keys['firebase_storage_bucket']
                }
        self.firebase = Firebase(self.config)
        self.conn = self.firebase.database()

    # Returns a list of keys from the database
    def get_nodes(self, path):
        return list(self.conn.child(path).get().val().keys())

    # Returns a dict() structure from the database
    def get_data(self, path):
        return self.conn.child(path).get().val()

    # Add an item to the firebase dataset
    def create_node(self, path, data):
        self.conn.child(path).set(data)

    # Delete an item from the firebase dataset
    def destroy_node(self, path):
        self.conn.child(path).remove()

# YFinance Agent Class
class yfin_agent():

    def __init__(self):
        pass

    def gather_data(self, ticker):
        return yf.Ticker(ticker)

# FinnHub Agent Class
class finnhub_agent():

    def __init__(self):
        self.tickers = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=' + keys['finnhub_token']).json()
        self.cryptos = requests.get('https://finnhub.io/api/v1/crypto/symbol?exchange=coinbase&token=' + keys['finnhub_token']).json()
    
    def get_news(self, ticker, start="2020-01-01", end="2021-01-01"):
        return requests.get('https://finnhub.io/api/v1/company-news?symbol='+ticker+'&from='+start+'&to='+end+'&token='+keys['finnhub_token']).json()

    def get_sentiment(self, ticker):
        return requests.get('https://finnhub.io/api/v1/news-sentiment?symbol='+ticker+'&token='+keys['finnhub_token']).json()

# Quandl Agent Class
class quandl_agent():

    def __init__(self):
        quandl.ApiConfig.api_key = keys['quandl_api_key']
        self.bond_yields = quandl.get("USTREASURY/YIELD")
        self.unemployment = quandl.get("FRED/NROUST")
        self.nominal_gdp = quandl.get("FRED/NGDPPOT")
        self.real_gdp = quandl.get("FRED/GDPPOT")
        self.consumer_sentiment = quandl.get("UMICH/SOC1")

    def update(self):
        self.bond_yields = quandl.get("USTREASURY/YIELD")
        self.unemployment = quandl.get("FRED/NROUST")
        self.nominal_gdp = quandl.get("FRED/NGDPPOT")
        self.real_gdp = quandl.get("FRED/GDPPOT")
        self.consumer_sentiment = quandl.get("UMICH/SOC1")

# Webscraper Class
class webscraper():

    def __init__(self):
        pass

    def get_soup(self, url):
        self.soup = BeautifulSoup(urlopen(url), 'html.parser')
        #print(self.soup.find_all('article'))


# Reddit Agent Class
class reddit_agent():

    def __init__(self):
        self.agent = praw.Reddit(client_id=keys['reddit_client_id'],
                                 client_secret=keys['reddit_client_secret'],
                                 user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0")

    # TODO TODO TODO
    def get_subreddit_hot_posts(self, sub):
        page = ra.agent.subreddit(sub)
        top_posts = page.hot(limit=None)
        for post in top_posts:
            print(post.title, post.ups)

# Historic Crypto Agent Class
class crypto_history_agent():

    def __init__(self):
        pass

    def gather_data(self, coin):
        return HistoricalData(coin + '-USD',86400,'2010-01-01-00-00').retrieve_data()


# Coinbase Agent Class
class coinbase_agent():

    def __init__(self):
        self.agent = Client(keys['coinbase_client_id'], keys['coinbase_client_secret'], api_version='2021-03-01')


# Stocktwits Agent
class stocktwits_agent():

    def __init__(self):
        self.trending_streams = requests.get("https://api.stocktwits.com/api/2/streams/trending.json").json()
        self.trending_stocks = requests.get("https://api.stocktwits.com/api/2/trending/symbols.json").json()

    def update(self):
        self.trending_streams = requests.get("https://api.stocktwits.com/api/2/streams/trending.json").json()
        self.trending_stocks = requests.get("https://api.stocktwits.com/api/2/trending/symbols.json").json()


# Stock News Agent
''' TODO '''


# News API Agent
''' TODO '''


# City Falcon Agent
''' TODO '''


# Edgar Agent
''' TODO '''
