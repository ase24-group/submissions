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
            self.add(src, fun)

    def add(self, t, fun):
        row = t if hasattr(t, "cells") else Row(t)
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

    def split(self, best, rest, lite, dark):
        selected = Data(self.cols.names)
        max = 1e30
        out = 1

        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            if b > r:
                selected.add(row)

            tmp = abs(b + r) / abs(b - r + 1e-300)
            if tmp > max:
                out, max = i, tmp
        return out, selected
