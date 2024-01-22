from data import Data
from utils import coerce, output


class Test:
    def __init__(self, config):
        self.config = config

    def stats(self):
        # Test stats correct
        stats = output(Data("../data/auto93.csv").stats())
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

    def test_count_classes(self) -> None:
        data_obj = Data(self.config.file)
        class_counts = data_obj.cols.klass.has

        # Number of classes in each file
        number_of_classes = len(class_counts)
        out = "{0}:\n".format(self.config.file.split("/")[-1].split(".")[0])
        out += f"number of classes: {number_of_classes}\n"

        table_data = list(class_counts.items())

        # Max width for each column
        class_column_width = max(len(str(class_name)) for class_name, _ in table_data)
        count_column_width = max(len(str(count)) for _, count in table_data)

        out += "{:<{}}\t{:<{}}\n".format(
            "Class", class_column_width, "Count", count_column_width
        )
        for class_name, count in table_data:
            out += "{:<{}}\t{:<{}}\n".format(
                class_name, class_column_width, count, count_column_width
            )

        print(out)

        if self.config.file == "hw/data/diabetes.csv":
            with open("hw/test_assets/expected_diabetes_count_classes.txt", "r") as f:
                return f.read() == out

        elif self.config.file == "hw/data/soybean.csv":
            with open("hw/test_assets/expected_soybean_count_classes.txt", "r") as f:
                return f.read() == out
