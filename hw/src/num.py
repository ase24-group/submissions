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
