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
        return (self.n < 2 and 0) or ((self.m2 / (self.n - 1)) ** 0.5)

    def like(self, x: float) -> float:
        """
        How much a NUM (self) likes a number (x)
        """
        sd = self.div() + 1e-30
        nom = 2.718 ** (-0.5 * (x - self.mid()) ** 2 / sd**2)
        denom = sd * 2.5 + 1e-30
        return nom / denom
