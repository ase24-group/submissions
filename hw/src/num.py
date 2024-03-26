import math
from config import config


class Num:
    def __init__(self, s, n):
        self.txt = s or " "
        self.at = n or 0
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.hi = -1e30
        self.lo = 1e30
        self.heaven = 0 if self.txt.endswith("-") else 1

    def add(self, x):
        if x != "?":
            self.n = self.n + 1
            d = x - self.mu
            self.mu = self.mu + (d / self.n)
            self.m2 = self.m2 + (d * (x - self.mu))
            self.lo = min(x, self.lo)
            self.hi = max(x, self.hi)

    def mid(self):
        return self.mu

    def div(self):
        return 0 if self.n < 2 else (self.m2 / (self.n - 1)) ** 0.5

    def like(self, x: float, _) -> float:
        """
        How much a NUM (self) likes a number (x)
        """
        sd = self.div() + 1e-30
        nom = 2.718 ** (-0.5 * (x - self.mid()) ** 2 / sd**2)
        denom = sd * 2.5 + 1e-30
        return nom / denom

    def norm(self, x):
        return x if x == "?" else (x - self.lo) / (self.hi - self.lo + 1e-30)

    def dist(self, x, y):
        if x == "?" and y == "?":
            return 1

        x, y = self.norm(x), self.norm(y)

        if x == "?":
            x = 1 if y < 0.5 else 0

        if y == "?":
            y = 1 if x < 0.5 else 0

        return abs(x - y)

    def bin(self, x: float):
        tmp = (self.hi - self.lo) / (config.value.bins - 1)
        return self.hi == self.lo and 1 or math.floor(x / tmp + 0.5) * tmp
