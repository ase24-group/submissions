from data import Data
from utils import coerce, output


class Test:
    def __init__(self, config):
        self.config = config

    def stats(self):
        # Test stats correct
        stats = output(Data(self.config.file).stats())
        print(stats)
        return stats == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"

    def test_coerce(self):
        # Test string is converted to python dictionary
        dict_ex = coerce("{'a': 1, 'b': 2}")
        print(dict_ex)
        return type(dict_ex) == dict

    def test_output(self):
        # Test ' is removed from dict for string representation
        out = output({"a": 1, "b": 2})
        print(out)
        return out == "{a: 1, b: 2}"

    def test_count_classes(self, class_column: int = -1):
        diabetes_data = Data(self.config.file)
        class_counts = diabetes_data.cols.all[class_column].has
        
        # Number of classes in each file
        number_of_classes = len(class_counts)
        
        # Number of rows for each class
        number_of_rows = class_counts
    
    
