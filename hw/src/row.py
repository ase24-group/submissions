import math
from config import config
import sys


class Row:
    def __init__(self, t):
        self.cells = t

    def likes(self, datas):
        n, nHypothesis = 0, 0
        most, out = None, None
        for data in datas.values():
            n += len(data.rows)
            nHypothesis += 1
        for k, data in datas.items():
            tmp = self.like(data, n, nHypothesis)
            if tmp is not None and ((most is None) or (tmp > most)):
                most, out = tmp, k
        return out, most

    def like(self, data, n, nHypothesis):
        k = config.value.k
        prior = (len(data.rows) + k) / (n + k * nHypothesis)
        out = math.log(prior)
        for col in data.cols.x.values():
            v = self.cells[col.at]
            if v != "?":
                inc = col.like(v, prior)
                try:
                    out += math.log(inc)
                except:
                    return float("-inf")

        return math.exp(out)

    def d2h(self, data=None):
        d, n = 0, 0

        for col in data.cols.y.values():
            try:
                x = self.cells[col.at]
                n = n + 1
                d = d + abs(col.heaven - col.norm(self.cells[col.at])) ** 2
            except IndexError:
                sys.stderr.write("?")

        return (d**0.5) / (n**0.5)

    def dist(self, other, data, d: int = 0, n: int = 0, p=config.value.p):
        for col in data.cols.x.values():
            n += 1
            d += col.dist(self.cells[col.at], other.cells[col.at]) ** 2
        return (d / n) ** (1 / p)

    def neighbors(self, data, rows=None):
        rows = rows if rows else data.rows
        return sorted(rows, key=lambda row: self.dist(row, data))
