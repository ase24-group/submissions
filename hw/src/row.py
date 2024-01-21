from config import get_config

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