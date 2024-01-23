import os
from utils import coerce, output
from data import Data
from box import Box
from config import config

class Test:
    def __init__(self):
        pass

    def stats(self):
        # Test stats correct
        stats = output(Data("../data/auto93.csv").stats())
        print(stats)
        return stats == "{.N: 398, Acc+: 15.57, Lbs-: 2970.42, Mpg+: 23.84}"

    def coerce(self):
        # Test string is converted to python dictionary
        dict_ex = coerce("{'a': 1, 'b': 2}")
        print(dict_ex)
        return type(dict_ex) == dict

    def output(self):
        # Test ' is removed from dict for string representation
        out = output({"a": 1, "b": 2})
        print(out)
        return out == "{a: 1, b: 2}"

    def count_classes(self) -> None:
        files = ["diabetes.csv", "soybean.csv"]
        success = True

        for file in files:
            file_name, _ = os.path.splitext(file)
            data = Data(f"../data/{file}")
            class_counts = data.cols.klass.has

            # Number of classes in each file
            number_of_classes = len(class_counts)
            out = f"{file_name}:\n"
            out += f"number of classes: {number_of_classes}\n"

            table_data = list(class_counts.items())
            total_rows = len(data.rows)

            # Max width for each column
            class_column_width = max(
                len(str(class_name)) for class_name, _ in table_data
            )
            count_column_width = max(len(str(count)) for _, count in table_data)
            percent_column = [((count / total_rows) * 100) for _, count in table_data]
            percent_column_width = max(
                len(f"{percent:05.2f} %") for percent in percent_column
            )

            out += "{:<{}}\t{:<{}}\t{:<{}}\n".format(
                "Class",
                class_column_width,
                "Count",
                count_column_width,
                "Percentage",
                percent_column_width,
            )
            for class_name, count in table_data:
                percent = (count / total_rows) * 100
                out += "{:<{}}\t{:<{}}\t{:<{}}\n".format(
                    class_name,
                    class_column_width,
                    count,
                    count_column_width,
                    f"{percent:05.2f} %",
                    percent_column_width,
                )

            print(out)

            with open(
                f"../test_assets/expected_{file_name}_count_classes.txt", "r"
            ) as f:
                if f.read() != out:
                    success = False

        return success

    def bayes(self):
        wme = Box({"acc": 0, "datas": {}, "tries": 0, "n": 0})
        Data("../data/diabetes.csv", lambda data, t: learn(data, t, wme))
        return wme.acc / (wme.tries) > 0.72
    
    def km(self):
        print("#{:<4s}\t{}\t{}".format("acc", "k", "m"))
        for k in range(4):
            for m in range(4):
                # if k != 0 or m != 0:
                config.value.k = k
                config.value.m = m
                wme = Box({"acc":0, "datas":{}, "tries": 0, "n": 0})
                Data("../data/soybean.csv", lambda data, t: learn(data, t, wme))
                print("{:05.2f}%\t{}\t{}".format(wme.acc * 100 / wme.tries, k, m))


def learn(data, row, my) -> None:
    my.n += 1
    kl = row.cells[data.cols.klass.at]
    if my.n > 10:
        my.tries += 1
        my.acc += 1 if kl == row.likes(my.datas)[0] else 0
    my.datas[kl] = my.datas.get(kl, Data(data.cols.names))  # default value --> new data
    my.datas[kl].add(row, None)
