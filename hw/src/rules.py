import utils
from config import config
from rule import Rule


class Rules:
    def __init__(self, ranges, goal, rowss):
        for k, v in rowss.items():
            print(k, "\t", len(v))
        self.sorted = {}
        self.goal = goal
        self.rowss = rowss
        self.LIKE, self.HATE = 0, 0

        self.like_hate()
        for range in ranges:
            range.scored = self.score(range.y)
        self.sorted = self.top(self._try(self.top(ranges)))

    def like_hate(self):
        for y, rows in self.rowss.items():
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        return utils.score(t, self.goal, self.LIKE, self.HATE, config.value.Support)

    def _try(self, ranges):
        u = []
        for subset in utils.powerset(ranges):
            if len(subset) > 0:
                rule = Rule(subset)
                rule.scored = self.score(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(self, t):
        t = sorted(t, key=lambda x: x.scored, reverse=True)
        u = []
        for x in t:
            if x.scored >= t[0].scored * config.value.Cut:
                u.append(x)
        return utils.slice(u, 0, config.value.Beam)
