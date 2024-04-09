import utils
from config import config


class Rules:
    def __init__(self, ranges, goal, rowss):
        for k, v in enumerate(rowss):
            print(k, len(v))
        self.sorted = {}
        self.goal = goal
        self.rowss = rowss
        self.LIKE, self.HATE = 0, 0

        self.like_hate()
        for range in ranges:
            range.scored = self.scored(range.y)
        self.scored = self.top(self._try(self.top))

    def like_hate(self):
        for y, rows in enumerate(self.rowss):
            if y == self.goal:
                self.LIKE += len(rows)
            else:
                self.HATE += len(rows)

    def score(self, t):
        return utils.score(t, self.goal, self.LIKE, self.HATE)

    def _try(self, ranges):
        u = []
        for subset in utils.powerset(ranges):
            if len(subset) > 0:
                rule = Rule(subset)
                rule.scored = self.scored(rule.selectss(self.rowss))
                if rule.scored > 0.01:
                    u.append(rule)
        return u

    def top(t):
        t = sorted(t, key=lambda x: x.scored, reverse=True)
        u = []
        for x in t:
            if x.scored >= t[0].scored * config.value.Cut:
                u.append(x)
        return utils.slice(u, 0, config.value.Beam)
