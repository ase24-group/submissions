import math
from config import config


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
            if (most is None) or (tmp > most):
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
