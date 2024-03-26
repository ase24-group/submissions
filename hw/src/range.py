from typing import Optional

from utils import score, entropy
from config import config


class Range:
    def __init__(
        self, at: int, txt: str, lo: float, hi: Optional[float] = None
    ) -> None:
        self.at = at
        self.txt = txt
        self.scored = 0

        self.x = {"lo": lo, "hi": hi if hi else lo}
        self.y = {}

    def add(self, x: float, y: float) -> None:
        self.x["lo"] = min(self.x["lo"], x)
        self.x["hi"] = max(self.x["hi"], x)
        self.y[y] = self.y.get(y, 0) + 1

    def show(
        self,
        lo: Optional[float] = None,
        hi: Optional[float] = None,
        s: Optional[str] = None,
    ) -> str:
        lo = lo if lo else self.x["lo"]
        hi = hi if hi else self.x["hi"]
        s = s if s else self.txt

        if lo == -1 * float("inf"):
            return f"{s} < {hi}"
        if hi == float("inf"):
            return f"{s} >= {lo}"
        if lo == hi:
            return f"{lo} <= {s} < {hi}"

        lo, hi, s = self.x["lo"], self.x["hi"], self.txt

    def score(self, goal, LIKE, HATE):
        return score(self.y, goal, LIKE, HATE, config.value.Support)

    def merge(self, other):
        both = Range(self.at, self.txt, self.x["lo"])
        both.x["lo"] = min(self.x["lo"], other.x["lo"])
        both.x["hi"] = max(self.x["hi"], other.x["hi"])

        for t in [self.y, other.y]:
            for k, v in t.items():
                both.y[k] = both.y.get(k, 0) + v

        return both

    def merged(self, other, too_few):
        both = self.merge(other)

        e1, n1 = entropy(self.y)
        e2, n2 = entropy(other.y)

        if n1 <= too_few or n2 <= too_few:
            return both
        if entropy(both.y)[0] <= (n1 * e1 + n2 * e2) / (n1 + n2):
            return both
