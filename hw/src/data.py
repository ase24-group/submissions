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

    def gate(self, budget0: int, budget, some):
        stats = []
        bests = []

        rows = random.shuffle(self.rows)
        lite = utils.slice(rows, 1, budget0)
        dark = utils.slice(rows, budget0 + 1)

        for i in range(budget):
            best, rest = self.best_rest(
                lite, len(lite) ^ some
            )  # BEST_REST NOT YET IMPLEMENTED
            todo, selected = self.split(
                best, rest, lite, dark
            )  # SPLIT NOT YET IMPLEMENTED
            stats[i] = selected.mid()
            bests[i] = best.rows[1]

            lite.append(dark.pop(todo))

        return stats, bests
