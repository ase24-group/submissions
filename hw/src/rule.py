class Rule:
    def __init__(self, ranges) -> None:
        self.parts = {}
        self.scored = 0

        for range in ranges:
            # t = self.parts[range.txt] or {}
            t = self.parts[range.txt] if (self.parts.get(range.txt) is not None) else []
            t.append(range)
            self.parts[range.txt] = t

    @staticmethod
    def _or(ranges, row) -> bool:
        x = row.cells[ranges[0].at]

        if x == "?":
            return True

        for range in ranges:
            lo = range.x["lo"]
            hi = range.x["hi"]
            if lo == hi and lo == x or lo <= x and x < hi:
                return True

        return False

    def _and(self, row) -> bool:
        for _, ranges in self.parts.items():
            if not self._or(ranges, row):
                return False
        return True

    def selects(self, rows):
        t=[]
        for r in rows:
            if self._and(r):
                t.append(r)
        return t

    def selectss(self, rowss):
        t={}
        for y, rows in rowss.items():
            t[y] = len(self.selects(rows))
        return t

    def show(self):
        ands = []
        for _, ranges in self.parts.items():
            ors = self._show_less(ranges)
            for i, range in enumerate(ors):
                at = range.at
                ors[i] = range.show()
            ands.append(" or ".join(ors))
        return " and ".join(ands)
    
    def _show_less(self, t, ready=False):
        if not ready:
            t = t[:]
            t.sort(key=lambda a: a.x["lo"])
        i = 0
        u = []
        while i < len(t):
            a = t[i]
            if i < len(t) - 1:
                if a.x["hi"] == t[i+1].x["lo"]:
                    a = a.merge(t[i+1])
                    i += 1
            u.append(a)
            i += 1
        if len(u) == len(t):
            return t
        else:
            self._show_less(t, ready)
