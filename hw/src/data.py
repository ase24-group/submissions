import utils
from row import Row
from cols import Cols


class Data:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None
        if type(src) == str:
            for _, x in utils.csv(src):
                self.add(x, fun)
        else:
            for _, x in src or []:
                self.add(x, fun)

    def add(self, t, fun):
        row = Row(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = Cols(row)

    def mid(self, cols):
        u = []
        for _, col in cols or self.cols.all:
            u.append(col.mid())
        return Row(u)

    def div(self, cols):
        u = []
        for _, col in cols or self.cols.all:
            u.append(col.div())
        return Row(u)

    def stats(self, cols=None, fun=None, ndivs=2):
        u = {".N": len(self.rows)}
        for _, col in self.cols.y.items():
            u[col.txt] = round(col.mid(), ndivs)
        return u
