import time
from datetime import datetime
import numpy as np
from datastructures import timeseries_collection
from datacollectors import coin_market_cap_agent, nomics_api_agent, crypto_history_agent, quandl_agent, yfin_agent

# Class for the overall stock evaluation model
class in_the_fade():

    def __init__(self):

        # Connection Objects
        self.coinmarket_metrics = coin_market_cap_agent()
        self.nomics_metrics = nomics_api_agent()
        self.crypto_history = crypto_history_agent()
        self.quandl = quandl_agent()
        self.yfin = yfin_agent()

        # Master Data
        self.data = timeseries_collection()

    def default_analysis(self):

        print(">> BEGINNING DEFAULT ANALYSIS")

        # Get Crypto Prices
        print(">> IMPORTING CRYPTO PRICES")
        self.get_index_data("Ethereum", "ETH")
        self.get_index_data("Bitcoin", "BTC")

        # Create Indexes
        print(">> IMPORTING INDEX DATA")
        self.get_index_data("Dow Jones Index", "^DJI")
        self.get_index_data("Nasdaq Index", "^IXIC")
        self.get_index_data("S&P 500 Index", "^GSPC")
        self.get_index_data("Russell 2000 Index", "^RUT")
        self.get_index_data("NYSE American Composite Index", "^XAX")
        self.get_index_data("Hang Seng Index", "^HSI")
        self.get_index_data("Nikkei 225", "^N225")
        self.get_index_data("FTSE 100 Index", "^FTSE")
        self.get_index_data("DAX Performance Index", "^GDAXI")
        self.get_index_data("OTC Markets Group Inc", "OTCM")

        # Misc Datasets
        print(">> IMPORTING MISC METRICS")
        self.get_quandl_data()

    '''
    STOCK MARKET INDEXES
    Stock Index Timeseries..
    '''

    def get_index_data(self, name, index):

        # Extract Index Data from APIs
        indx = self.yfin.gather_data(index)
        indxhistory = indx.history(period="max")
        indxtimes = list(indxhistory.index.astype(str))
        indxdata = indxhistory["Close"].tolist()
        indxchanges = self.get_percent_changes(indxdata)
        indxvolumes = indxhistory["Volume"].tolist()
        price = indxdata[len(indxdata) - 1]

        # Add data to model
        self.data.add_timeseries(name, indxtimes, indxdata)
        self.data.add_timeseries(name + " Volumes", indxtimes, indxvolumes)
        self.data.add_timeseries(name + " Delta", indxtimes, indxchanges)

    '''
    CRYPTO ASSETS
    Crypto Asset Timeseries..
    '''

    def get_crypto_data(self, name, coin):

        # Extract Crypto Data from APIs
        crypto = self.crypto_history.gather_data(coin)
        cryptotimes = list(crypto)
        cryptodata = crypto["close"].tolist()
        cryptochanges = self.get_percent_changes(cryptodata)
        cryptovolumes = crypto["volume"].tolist()
        price = cryptodata[len(cryptodata) - 1]

        # Add data to model
        self.data.add_timeseries(name, cryptotimes, cryptodata)
        self.data.add_timeseries(name + " Volumes", cryptotimes, cryptovolumes)
        self.data.add_timeseries(name + " Delta", cryptotimes, cryptochanges)

    '''
    EXTERNAL INDICATOR METHODS
    Bond Yields, Unemployment Numbers, GDP, Etc..
    '''

    def get_quandl_data(self):
        self.quandl.update()
        self.data.add_timeseries("1 Month Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['1 MO'].astype(str)))
        self.data.add_timeseries("2 Month Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['2 MO'].astype(str)))
        self.data.add_timeseries("3 Month Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['3 MO'].astype(str)))
        self.data.add_timeseries("6 Month Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['6 MO'].astype(str)))
        self.data.add_timeseries("1 Year Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['1 YR'].astype(str)))
        self.data.add_timeseries("2 Year Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['2 YR'].astype(str)))
        self.data.add_timeseries("3 Year Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['3 YR'].astype(str)))
        self.data.add_timeseries("5 Year Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['5 YR'].astype(str)))
        self.data.add_timeseries("10 Year Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['10 YR'].astype(str)))
        self.data.add_timeseries("20 Year Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['20 YR'].astype(str)))
        self.data.add_timeseries("30 Year Bond Data", list(self.quandl.bond_yields.index.astype(str)), list(self.quandl.bond_yields['30 YR'].astype(str)))
        self.data.add_timeseries("Unemployment", list(self.quandl.unemployment.index.astype(str)), list(self.quandl.unemployment['Value'].astype(str)))
        self.data.add_timeseries("Real GDP", list(self.quandl.real_gdp.index.astype(str)), list(self.quandl.real_gdp['Value'].astype(str)))
        self.data.add_timeseries("Nominal GDP", list(self.quandl.nominal_gdp.index.astype(str)), list(self.quandl.nominal_gdp['Value'].astype(str)))
        self.data.add_timeseries("Consumer Sentiment", list(self.quandl.consumer_sentiment.index.astype(str)), list(self.quandl.consumer_sentiment['Index'].astype(str)))

    '''
    GENERAL METHODS
    Methods for general analysis of data
    '''

    def get_percent_changes(self, data):
        changes = [0]
        pt = data[0]
        for xx in np.arange(1, len(data)):
            changes.append((data[xx] - pt)/pt)
            pt = data[xx]
        return changes

    def clean_key(self, key):
        if key == "" or key == None:
            key = "blank"
        else:
            key = key.replace(".", "_")
            key = key.replace("$", "_")
            key = key.replace("#", "_")
            key = key.replace("[", "_")
            key = key.replace("]", "_")
            key = key.replace("/", "_")
        return key
