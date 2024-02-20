import utils
from row import Row
from cols import Cols
import random
from config import config


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

    def gate(self, budget0: int, budget, some, info=None):
        stats = []
        bests = []

        if not info:
            info = {
                "top6": [],
                "top50": [],
                "most": [],
                "rand": [],
                "mid": [],
                "top": [],
            }

        y_indices = self.cols.y.keys()

        random.shuffle(self.rows)

        info["top6"].append(
            [[row.cells[y] for y in y_indices] for row in self.rows[:6]]
        )
        info["top50"].append(
            [[row.cells[y] for y in y_indices] for row in self.rows[:50]]
        )

        self.rows.sort(key=lambda x: x.d2h(self))
        info["most"].append([self.rows[0].cells[y] for y in y_indices])

        random.shuffle(self.rows)
        lite = utils.slice(self.rows, 0, budget0)
        dark = utils.slice(self.rows, budget0 + 1)

        for i in range(budget):
            best, rest = self.best_rest(lite, len(lite) ** some)
            todo, selected = self.split(best, rest, lite, dark)
            stats.append(selected.mid())
            bests.append(best.rows[0])

            rand = Data(self.cols.names)
            for row in random.sample(dark, budget0 + 1):
                rand.add(row)

            info["rand"].append([rand.mid().cells[y] for y in y_indices])
            info["mid"].append([selected.mid().cells[y] for y in y_indices])
            info["top"].append([best.rows[0].cells[y] for y in y_indices])

            lite.append(dark.pop(todo))

        return stats, bests, info

    def farapart(self, rows, sortp=None, a=None):
        far = int((len(rows) * config.value.Far))
        evals = 1 if a else 2
        a = a or utils.any(rows).neighbors(self, rows)[far]
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a
        return a, b, a.dist(b, self), evals

    def branch(self, stop=None, rest=None, _branch=None, evals=None):
        if evals is None:
            evals = [1]
        else:
            evals[0] = 1
        if rest is None:
            rest = []

        stop = stop if stop else (2 * (len(self.rows) ** 0.5))

        def _branch(data, above=None, left=None, lefts=None, rights=None):
            if len(data.rows) > stop:
                lefts, rights, left = self.half(data.rows, True, above)
                evals[0] += 1
                for row1 in rights:
                    rest.append(row1)
                return _branch(self.clone(lefts), left)
            else:
                return self.clone(data.rows), self.clone(rest), evals

        return _branch(self)
