class Rule:
    def __init__(self, ranges, t) -> None:
        self.parts = {}
        self.scored = 0

        for range in ranges:
            t = self.parts[range.txt] or {}
            t.append(range)
            self.parts[range.txt] = t

    @staticmethod
    def _or(ranges, row, x, lo, hi) -> bool:
        x = row.cells[ranges[0].at]

        if x == "?":
            return True

        for range in ranges:
            lo = range.x.lo
            hi = range.x.hi
            if lo == hi and lo == x or lo <= x and x < hi:
                return True

        return False

    def _and(self, row) -> bool:
        for ranges in self.parts:
            if not self._or(ranges, row):
                return False
        return True

    def selects(self, rows, t={}):
        for r in rows:
            if self._and(r):
                t.append(r)
        return t

    def selectss(self, rowss, t={}):
        for y, rows in enumerate(rowss):
            t[y] = len(self.selects(rows))
        return t
