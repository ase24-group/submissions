import os, random
from datetime import datetime
from utils import coerce, output, output_gate20_info, align_list
from data import Data
from box import Box
from num import Num
from config import config
from stats import Sample, eg0
import sys


class TestGate:
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
        print("Accuracy: ", wme.acc / (wme.tries))
        return wme.acc / (wme.tries) > 0.72

    def km(self):
        print("#{:<4s}\t{}\t{}".format("acc", "k", "m"))
        for k in range(4):
            for m in range(4):
                # if k != 0 or m != 0:
                config.value.k = k
                config.value.m = m
                wme = Box({"acc": 0, "datas": {}, "tries": 0, "n": 0})
                Data("../data/soybean.csv", lambda data, t: learn(data, t, wme))
                print("{:05.2f}%\t{}\t{}".format(wme.acc * 100 / wme.tries, k, m))

    def gate20(self):
        print("#best, mid")
        for i in range(20):
            d = Data("../data/auto93.csv")
            stats, bests, _ = d.gate(4, 16, 0.5)
            stat, best = stats[-1], bests[-1]
            print(f"{round(best.d2h(d), 2)}\t{round(stat.d2h(d), 2)}")

    def gate20_info(self):
        info = {}

        for i in range(20):
            if i != 0:
                # Increment seed by 1 to set a new seed for each run
                config.value.seed += 1
            d = Data("../data/auto93.csv")
            _, _, info = d.gate(4, 10, 0.5, info)

        output_gate20_info(info)

    def smo_no_stats(self):
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        file = "../data/auto93.csv"
        repeats = 20

        data = Data(file, fun=None, sortD2H=False)

        label_width = 10
        print(f"date    : {date}")
        print(f"file    : {file}")
        print(f"repeats : {repeats}")
        print(f"seed    : {config.value.seed}")
        print(f"rows    : {len(data.rows)}")
        print(f"cols    : {len(data.cols.names)}")

        names = f"{'names':{label_width}}{align_list(data.cols.names)}"
        print(names)

        mid = f"{'mid':{label_width}}{align_list(data.mid().cells)}"
        print(mid)

        div = f"{'div':{label_width}}{align_list(data.div().cells)}"
        print(div)

        print("#")

        smo9s = [data.smo(score=lambda b, r: 2 * b - r) for _ in range(repeats)]
        smo9s = sorted(smo9s, key=lambda row: row.d2h(data))
        for row in smo9s:
            label = f"smo{config.value.budget0 + config.value.Budget}"
            smo9 = f"{label:{label_width}}{align_list(row.cells)}"
            print(smo9)

        print("#")

        any50s = []
        for _ in range(repeats):
            random.shuffle(data.rows)
            any50s += [data.clone(data.rows[:50], sortD2H=True).rows[0]]
        for row in sorted(any50s, key=lambda row: row.d2h(data)):
            label = "any50"
            any50 = f"{label:{label_width}}{align_list(row.cells)}"
            print(any50)

        print("#")

        all = f"{'100%':{label_width}}{align_list(data.clone(data.rows, sortD2H=True).rows[0].cells)}"
        print(all)

    def smo_stats(self):
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        file = "../data/auto93.csv"
        repeats = 20

        data = Data(file, fun=None, sortD2H=False)
        stats = []

        print(f"date    : {date}")
        print(f"file    : {file}")
        print(f"repeats : {repeats}")
        print(f"seed    : {config.value.seed}")
        print(f"rows    : {len(data.rows)}")
        print(f"cols    : {len(data.cols.names)}")

        d2h_values = Num("d2h_values", 0)
        for row in data.clone(data.rows, sortD2H=True).rows:
            d2h_values.add(row.d2h(data))
        print(f"best    : {round(d2h_values.lo, 2)}")
        print(f"tiny    : {round(d2h_values.div() * config.value.cohen, 2)}")
        sorted_d2hs = sorted([row.d2h(data) for row in data.rows])
        print("#base", end=" ")
        stats.append(Sample(sorted_d2hs, txt="base"))

        for budget in [9, 15, 20]:
            config.value.Budget = budget - config.value.budget0
            print("#bonr" + str(budget), end=" ")
            stats.append(
                Sample(
                    [
                        data.smo(
                            score=lambda b, r: abs(b + r)
                            / abs(b - r + sys.float_info.min)
                        ).d2h(data)
                        for _ in range(repeats)
                    ],
                    txt="#bonr" + str(budget),
                )
            )
            print("#rand" + str(budget), end=" ")
            stats.append(
                Sample(
                    [
                        data.clone(shuffle(data.rows[:budget]), sortD2H=True)
                        .rows[0]
                        .d2h(data)
                        for _ in range(repeats)
                    ],
                    txt="#rand" + str(budget),
                )
            )
        print("#rand" + str(int(0.9 * len(data.rows))), end=" ")
        stats.append(
            Sample(
                [
                    data.clone(
                        shuffle(data.rows[: int(0.9 * len(data.rows))]), sortD2H=True
                    )
                    .rows[0]
                    .d2h(data)
                    for _ in range(repeats)
                ],
                txt="#rand" + str(int(0.9 * len(data.rows))),
            )
        )

        print("\n#report" + str(len(stats)))
        eg0(stats)


def learn(data, row, my) -> None:
    my.n += 1
    kl = row.cells[data.cols.klass.at]
    if my.n > 10:
        my.tries += 1
        my.acc += 1 if kl == row.likes(my.datas)[0] else 0
    my.datas[kl] = my.datas.get(kl, Data(data.cols.names))  # default value --> new data
    my.datas[kl].add(row, None)


def shuffle(rows):
    random.shuffle(rows)
    return rows
