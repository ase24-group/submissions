import utils
from row import Row
from cols import Cols
import random


class Data:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None
        if type(src) == str:
            for _, x in utils.csv(src):
                self.add(x, fun)
        else:
            self.add(src, fun)

    def add(self, t, fun=None):
        row = t if hasattr(t, "cells") else Row(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = Cols(row)

    def mid(self, cols=None):
        u = []
        for col in cols or self.cols.all:
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

    def best_rest(self, rows, want, best=None, rest=None):
        rows.sort(key=lambda x: x.d2h(self))
        best, rest = Data(self.cols.names), Data(self.cols.names)
        for i in range(len(rows)):
            if i <= want:
                best.add(rows[i])
            else:
                rest.add(rows[i])
        return best, rest

    def gate(self, budget0: int, budget, some):
        y_indices = self.cols.y.keys()

        # print("1. top6", y values of first 6 examples in ROWS)  #baseline1
        top6_1 = [[row.cells[y] for y in y_indices] for row in self.rows[:6]]
        # print("2. top50", y values of first 50 examples in ROWS)  #baseline2
        top50_2 = [[row.cells[y] for y in y_indices] for row in self.rows[:50]]

        # Sort rows on "distance to heaven"
        self.rows.sort(key=lambda x: x.d2h(self))
        # print("3. most", y values of ROW[1])
        most_3 = [self.rows[0].cells[y] for y in y_indices]

        random.shuffle(self.rows)
        lite = utils.slice(self.rows, 0, budget0)
        dark = utils.slice(self.rows, budget0 + 1)

        rand_4 = []
        stats = []
        bests = []

        for i in range(budget):
            best, rest = self.best_rest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)
            # print("4: rand", y values of centroid of (from DARK, select BUDGET0+i rows at random))
            rand_4.append(
                [
                    [row.cells[y] for y in y_indices]
                    for row in random.sample(dark, budget0 + 1)
                ]
            )
            stats.append(selected.mid())
            bests.append(best.rows[0])

            lite.append(dark.pop(todo))

        return stats, bests, top6_1, top50_2, most_3, rand_4
