import pandas as pd

class portfolio():

    def __init__(self, name):
        self.name = name
        self.assets = []
        self.asset_distribution = []
        self.data = timeseries_collection()
        

class timeseries_collection():

    def __init__(self):
        self.global_start = None
        self.global_end = None
        self.timeseries = []
        self.data_matrix = None

    def add_timeseries(self):
        pass # TODO TODO TODO

    def build_data_matrix(self):
        pass # TODO TODO TODO

class timeseries():

    def __init__(self, name, times, data):
        self.name = name
        self.time = self.str_list_to_datetime(times)
        self.data = self.str_list_to_float(data)

    def str_list_to_datetime(self, xx):
        return [datetime.strptime(x, '%Y-%m-%d') for x in xx]

    def str_list_to_float(self, xx):
        return [float(x) for x in xx]
