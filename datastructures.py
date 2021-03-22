class timeseries():

    def __init__(self, times, data):
        self.time = self.str_list_to_datetime(times)
        self.data = self.str_list_to_float(data)

    def str_list_to_datetime(self, xx):
        return [datetime.strptime(x, '%Y-%m-%d') for x in xx]

    def str_list_to_float(self, xx):
        return [float(x) for x in xx]
