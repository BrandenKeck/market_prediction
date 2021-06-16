import pandas as pd
from datetime import datetime

class timeseries_collection():

    def __init__(self):
        self.current_idx = -1
        self.global_start = None
        self.global_end = None
        self.data_matrix = None
        self.timeseries = []


    def add_timeseries(self, name, times, data):
        self.current_idx = self.current_idx + 1
        self.timeseries.append(timeseries(name, times, data))

        if self.global_start == None or self.timeseries[self.current_idx].oldest > self.global_start:
            self.global_start = self.timeseries[self.current_idx].oldest

        if self.global_end == None or self.timeseries[self.current_idx].newest < self.global_end:
            self.global_end = self.timeseries[self.current_idx].newest


    def build_data_matrix(self):
        pass # TODO TODO TODO

    def get_series_index(self, name):
        for idx in np.arange(self.timeseries):
            if self.timeseries[idx].name == name:
                return idx

        return "Error"

class timeseries():

    def __init__(self, name, times, data):
        self.name = name
        self.time = self.str_list_to_datetime(times)
        self.oldest = min(self.time)
        self.newest = max(self.time)
        self.data = self.str_list_to_float(data)


    def str_list_to_datetime(self, xx):
        return [datetime.strptime(x, '%Y-%m-%d') for x in xx]

    def str_list_to_float(self, xx):
        return [float(x) for x in xx]
