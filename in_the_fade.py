import time
from datetime import datetime
import numpy as np
from datacollectors import itfdb, quandl_agent, finnhub_agent, yfin_agent, crypto_history_agent, coinbase_agent, stocktwits_agent

# Class for the overall stock evaluation model
class in_the_fade():

    def __init__(self):

        # Connection Objects
        self.db = itfdb()
        self.quandl = quandl_agent()
        self.finnhub = finnhub_agent()
        self.yfin = yfin_agent()
        self.crypto_history = crypto_history_agent()
        self.coinbase = coinbase_agent()
        self.stocktwits = stocktwits_agent()

        # Stock Data Objects
        self.indices = dict()
        self.stocks = dict()
        self.cryptos = dict()
        self.portfolios = dict()
        self.market_info = dict()

    '''
    PORTFOLIO FUNCTIONS
    get_subreddit_hot_posts
    '''

    # TODO TODO TODO

    '''
    INDEX / STOCK METHODS
    Methods for DJI, NASDAQ, Pink Slip, Etc.
    '''

    def get_index_data(self):

        # Update Console
        print("--- GET INDEX DATA ---")

        # Relevent indices are hardcoded, loop through the following:
        indices = ["^DJI", "^IXIC", "^GSPC", "^RUT", "^XAX", "^HSI", "^N225", "^FTSE", "^GDAXI", "OTCM"]
        for ticker in indices:

            # Update Console
            print("Current Ticker: " + str(ticker))

            # Extract Index Data from APIs
            indx = self.yfin.gather_data(ticker)
            indxhistory = indx.history(period="max")
            indxtimes = list(indxhistory.index.astype(str))
            indxdata = indxhistory["Close"].tolist()
            indxchanges = self.get_percent_changes(indxdata)
            indxvolumes = indxhistory["Volume"].tolist()
            price = indxdata[len(indxdata) - 1]

            # Build Local Datastructure
            self.indices[ticker] = dict()
            self.indices[ticker]["data"] = dict()
            self.indices[ticker]["data"]["times"] = indxtimes
            self.indices[ticker]["data"]["prices"] = indxdata
            self.indices[ticker]["data"]["volumes"] = indxvolumes
            self.indices[ticker]["data"]["changes"] = indxchanges
            self.indices[ticker]["summary"] = dict()
            self.indices[ticker]["summary"]["name"] = indx.info["shortName"]
            self.indices[ticker]["summary"]["latest_price"] = price
            self.indices[ticker]["summary"]["last_update"] = str(datetime.now())
            self.indices[ticker]["summary"]["avg_volume"] = indx.info["averageVolume"]
            self.indices[ticker]["summary"]["52wk_high"] = indx.info["fiftyTwoWeekHigh"]
            self.indices[ticker]["summary"]["52wk_low"] = indx.info["fiftyTwoWeekLow"]

            # Push to Remote Datastructure
            self.db.create_node("/index/" + ticker, self.indices[ticker])

    def get_random_stock_data(self):
        idx = np.random.randint(len(self.finnhub.tickers))
        ticker = self.finnhub.tickers[idx]["symbol"]
        self.get_stock_data(ticker)

    def update_all_stock_data(self):
        nodes = self.db.get_nodes('stocks')
        for ticker in nodes:
            self.get_stock_data(ticker)

    def delete_all_stock_data(self):
        nodes = self.db.get_nodes('stocks')
        for ticker in nodes:
            self.db.destroy_node('/stocks/' + ticker)

    def get_stock_data(self, ticker):

        # Update Console
        print("--- GET STOCK DATA ---")
        print("Current Ticker: " + str(ticker))

        # Extract Stock Data from APIs
        stock = self.yfin.gather_data(ticker)
        stockhistory = stock.history(period="max")
        stocktimes = list(stockhistory.index.astype(str))
        stockdata = stockhistory["Close"].tolist()
        stockchanges = self.get_percent_changes(stockdata)
        stockvolumes = stockhistory["Volume"].tolist()
        price = stockdata[len(stockdata) - 1]

        # Build Local Datastructure
        self.stocks[ticker] = dict()
        self.stocks[ticker]["data"] = dict()
        self.stocks[ticker]["data"]["times"] = stocktimes
        self.stocks[ticker]["data"]["prices"] = stockdata
        self.stocks[ticker]["data"]["volumes"] = stockvolumes
        self.stocks[ticker]["data"]["changes"] = stockchanges
        self.stocks[ticker]["summary"] = dict()
        self.stocks[ticker]["summary"]["name"] = stock.info["longName"]
        self.stocks[ticker]["summary"]["sector"] = stock.info["sector"]
        self.stocks[ticker]["summary"]["latest_price"] = price
        self.stocks[ticker]["summary"]["last_update"] = str(datetime.now())
        self.stocks[ticker]["summary"]["beta"] = stock.info["beta"]
        self.stocks[ticker]["summary"]["market_cap"] = stock.info["marketCap"]
        self.stocks[ticker]["summary"]["avg_volume"] = stock.info["averageVolume"]
        self.stocks[ticker]["summary"]["52wk_high"] = stock.info["fiftyTwoWeekHigh"]
        self.stocks[ticker]["summary"]["52wk_low"] = stock.info["fiftyTwoWeekLow"]

        # Push to Remote Datastructure
        self.db.create_node("/stock/" + ticker, self.stocks[ticker])

    '''
    CRYPTO METHODS
    Methods for Coinbase-tradable crypto
    '''

    def get_random_crypto_data(self):
        idx = np.random.randint(len(self.finnhub.cryptos))
        coin = self.finnhub.cryptos[idx]["symbol"].split(":")[1].split("-")[0]
        self.get_crypto_data(coin)

    def update_all_crypto_data(self):
        nodes = self.db.get_nodes('crypto')
        for coin in nodes:
            self.get_crypto_data(coin)

    def delete_all_crypto_data(self):
        nodes = self.db.get_nodes('crypto')
        for coin in nodes:
            self.db.destroy_node('/crypto/' + coin)

    def get_crypto_data(self, coin):

        # Update Console
        print("--- GET CRYPTO DATA ---")
        print("Current Coin: " + str(coin))

        # Extract Crypto Data from APIs
        crypto = self.crypto_history.gather_data(coin)
        cryptotimes = list(crypto)
        cryptodata = crypto["close"].tolist()
        cryptochanges = self.get_percent_changes(cryptodata)
        cryptovolumes = crypto["volume"].tolist()
        price = cryptodata[len(cryptodata) - 1]

        # Build Local Datastructure
        self.cryptos[coin] = dict()
        self.cryptos[coin]["data"] = dict()
        self.cryptos[coin]["data"]["times"] = cryptotimes
        self.cryptos[coin]["data"]["prices"] = cryptodata
        self.cryptos[coin]["data"]["volumes"] = cryptovolumes
        self.cryptos[coin]["data"]["changes"] = cryptochanges
        self.cryptos[coin]["summary"] = dict()
        self.cryptos[coin]["summary"]["sector"] = "crypto"
        self.cryptos[coin]["summary"]["latest_price"] = price
        self.cryptos[coin]["summary"]["last_update"] = str(datetime.now())

        # Push to Remote Datastructure
        self.db.create_node("/crypto/" + coin, self.cryptos[coin])

    '''
    EXTERNAL INDICATOR METHODS
    Bond Yields, Unemployment Numbers, GDP, Etc..
    '''
    def get_bond_yields(self):
        self.quandl.update()
        self.market_info['bond_yields'] = dict()
        self.market_info['bond_yields']['time'] = list(self.quandl.bond_yields.index.astype(str))
        self.market_info['bond_yields']['1mo'] = list(self.quandl.bond_yields['1 MO'].astype(str))
        self.market_info['bond_yields']['2mo'] = list(self.quandl.bond_yields['2 MO'].astype(str))
        self.market_info['bond_yields']['3mo'] = list(self.quandl.bond_yields['3 MO'].astype(str))
        self.market_info['bond_yields']['6mo'] = list(self.quandl.bond_yields['6 MO'].astype(str))
        self.market_info['bond_yields']['1yr'] = list(self.quandl.bond_yields['1 YR'].astype(str))
        self.market_info['bond_yields']['2yr'] = list(self.quandl.bond_yields['2 YR'].astype(str))
        self.market_info['bond_yields']['3yr'] = list(self.quandl.bond_yields['3 YR'].astype(str))
        self.market_info['bond_yields']['4yr'] = list(self.quandl.bond_yields['5 YR'].astype(str))
        self.market_info['bond_yields']['5yr'] = list(self.quandl.bond_yields['7 YR'].astype(str))
        self.market_info['bond_yields']['10yr'] = list(self.quandl.bond_yields['10 YR'].astype(str))
        self.market_info['bond_yields']['20yr'] = list(self.quandl.bond_yields['20 YR'].astype(str))
        self.market_info['bond_yields']['30yr'] = list(self.quandl.bond_yields['30 YR'].astype(str))
        self.db.create_node("/info/bond_yields", self.market_info['bond_yields'])

    def get_unemployment_data(self):
        self.quandl.update()
        self.market_info['unemployment'] = dict()
        self.market_info['unemployment']['time'] = list(self.quandl.unemployment.index.astype(str))
        self.market_info['unemployment']['value'] = list(self.quandl.unemployment['Value'].astype(str))
        self.db.create_node("/info/unemployment", self.market_info['unemployment'])

    def get_gdp_data(self):
        self.quandl.update()
        self.market_info['gdp'] = dict()
        self.market_info['gdp']['time'] = list(self.quandl.real_gdp.index.astype(str))
        self.market_info['gdp']['real'] = list(self.quandl.real_gdp['Value'].astype(str))
        self.market_info['gdp']['nominal'] = list(self.quandl.nominal_gdp['Value'].astype(str))
        self.db.create_node("/info/gdp", self.market_info['gdp'])

    def get_misc_data(self):
        self.quandl.update()
        self.market_info['misc'] = dict()
        self.market_info['misc']['umich_senitment_time'] = list(self.quandl.consumer_sentiment.index.astype(str))
        self.market_info['misc']['umich_senitment'] = list(self.quandl.consumer_sentiment['Index'].astype(str))
        # TODO
        self.db.create_node("/info/misc", self.market_info['misc'])

    '''
    NEWS METHODS
    Trending News and Seniment Analysis
    '''

    # TODO TODO TODO
    '''
    def get_finnhub_sentiment(self):
        pass

    #TODO
    def monitor_stocktwits_trending_tickers(self):
        pass

    def monitor_stocktwits_trending_streams(self):
        self.stocktwits.update()
        self.news["stocktwits"] = dict()
        self.news["stocktwits"]['ids'] = []
        self.news["stocktwits"]['tickers'] = dict()
        if("messages" in list(self.stocktwits.trending_streams.keys())):
            for stream in self.stocktwits.trending_streams["messages"]:
                if stream['id'] not in self.news['stocktwits']['ids']:
                    self.news['stocktwits']['ids'].append(stream['id'])
                    for sym in stream['symbols']:
                        ticker = self.clean_key(sym['symbol'])
                        if ticker in list(self.news['stocktwits']['tickers']):
                            self.news['stocktwits']['tickers'][ticker]['mentions'] = self.news['stocktwits']['tickers'][ticker]['mentions'] + 1
                            if stream['entities']['sentiment'] == None:
                                pass
                            elif stream['entities']['sentiment']['basic'] == "Bullish":
                                self.news['stocktwits']['tickers'][ticker]['sentiment'] = self.news['stocktwits']['tickers'][ticker]['sentiment'] + 1
                            else:
                                self.news['stocktwits']['tickers'][ticker]['sentiment'] = self.news['stocktwits']['tickers'][ticker]['sentiment'] - 1
                        else:
                            self.news['stocktwits']['tickers'][ticker] = dict()
                            self.news['stocktwits']['tickers'][ticker]['mentions'] = 1
                            if stream['entities']['sentiment'] == None:
                                self.news['stocktwits']['tickers'][ticker]['sentiment'] = 0
                            elif stream['entities']['sentiment']['basic'] == "Bullish":
                                self.news['stocktwits']['tickers'][ticker]['sentiment'] = 1
                            else:
                                self.news['stocktwits']['tickers'][ticker]['sentiment'] = -1
        else:
            print("-- STOCK TWITS ERROR: [" + self.stocktwits.trending_streams["errors"][0]["message"] + "] --")

    def delete_all_news_data(self):
        nodes = self.db.get_nodes('news')
        for news in nodes:
            self.db.destroy_node('/news/' + news)
    '''

    '''
    DOWNLOAD DATA METHODS
    Retrieve Stored Database Data
    '''

    # TODO TODO TODO
    def import_index_data(self):
        pass

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

    def interpolate_datetime_data(self, startdate, enddate, startdata, enddata):
        pass

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
