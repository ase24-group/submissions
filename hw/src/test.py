from data import Data
from utils import coerce, output


class Test:
    def __init__(self, config):
        self.config = config

    def stats(self):
        stats = output(Data(self.config.file).stats())
        print(stats)
        return stats == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"

    def test_coerce(self):
        dict_ex = coerce("{'a': 1, 'b': 2}")
        return type(dict_ex) == dict

    def test_output(self):
        return output({"a": 1, "b": 2}) == "{a: 1, b: 2}"
