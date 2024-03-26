import math
from config import config


class Sym:
    def __init__(self, s, n):
        self.txt = s or " "
        self.at = n or 0
        self.n = 0
        self.has = {}
        self.mode = None
        self.most = 0

    def add(self, x):
        if x != "?":
            self.n = self.n + 1
            self.has[x] = 1 + self.has.get(x, 0)
            if self.has[x] > self.most:
                self.most, self.mode = self.has[x], x

    def mid(self):
        return self.mode

    def div(self):
        entropy = 0
        for value in self.has.values():
            entropy = entropy - value / self.n * math.log(value / self.n, 2)
        return entropy

    def like(self, x: str, prior: float):
        likelihood = 0.0
        try:
            likelihood = (self.has.get(x, 0) + config.value.m * prior) / (
                self.n + config.value.m
            )
        except:
            likelihood = None
        return likelihood

    def dist(self, x, y):
        return 1 if (x == "?" and y == "?") else (0 if x == y else 1)

    def bin(self, x):
        return x
