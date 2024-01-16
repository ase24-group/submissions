from data import Data
from utils import output

class Test:
    def __init__(self, config):
        self.config = config

    def stats(self):
        stats = output(Data(self.config.file).stats())
        print(stats)
        return stats == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"
