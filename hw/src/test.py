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

    def test_count_classes(self) -> None:
        data_obj = Data(self.config.file)
        class_counts = data_obj.cols.klass.has

        # Number of classes in each file
        number_of_classes = len(class_counts)
        out = "{0}:\n".format(self.config.file.split("/")[-1].split(".")[0])
        out += f"number of classes: {number_of_classes}\n"

        # Number of rows for each class
        col_widths = [len(x) for x in class_counts.keys()]

        out += " ".join(
            "{:<{}}".format(x, width)
            for x, width in zip(class_counts.keys(), col_widths)
        )
        out += "\n"
        out += " ".join(
            "{:<{}}".format(x, width)
            for x, width in zip(class_counts.values(), col_widths)
        )

        print(out)

        if self.config.file == "hw/data/diabetes.csv":
            return (
                out
                == "diabetes:\nnumber of classes: 2\npositive negative\n268      500     "
            )

        elif self.config.file == "hw/data/soybean.csv":
            return (
                out
                == "oybean:\nnumber of classes: 19\ndiaporthe-stem-canker charcoal-rot rhizoctonia-root-rot "
                "phytophthora-rot brown-stem-rot powdery-mildew downy-mildew brown-spot bacterial-blight "
                "bacterial-pustule purple-seed-stain anthracnose phyllosticta-leaf-spot alternarialeaf-spot "
                "frog-eye-leaf-spot diaporthe-pod-&-stem-blight cyst-nematode 2-4-d-injury herbicide-injury\n"
                "20                    20           20                   88               44             "
                "20             20           92         20               20                20                "
                "44          20                     91                  91                 "
                "15                          14            16           8               "
            )
