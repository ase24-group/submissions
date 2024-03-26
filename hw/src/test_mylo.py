from data import Data
from utils import pad_numbers, slice, oo, rnd, o, as_list
import random
from config import config
from range import Range


class TestMylo:
    def __init__(self):
        pass

    def dist(self):
        d = Data("../data/auto93.csv")
        r1 = d.rows[0]
        rows = r1.neighbors(d)
        for i, row in enumerate(rows):
            if i % 30 == 0:
                index = f"{i + 1:<8}"
                cells = f"{{{', '.join(map(str, row.cells))}}}"
                cells = f"{cells:<40}"
                dist = f"{round(row.dist(r1, d), 2):<10}"
                print(f"{index}{cells}{dist}")

    def far(self):
        d = Data("../data/auto93.csv")
        a, b, dist, evals = d.farapart(d.rows, True)
        print(f"far1:     {a.cells}")
        print(f"far2:     {b.cells}")
        print(f"distance: {round(dist, 2)}")
        print(f"evals:    {evals}")

    def tree(self):
        d = Data("../data/auto93.csv")
        t, evals = d.tree(True)
        t.show()
        print(evals)

    def branch(self):
        d = Data("../data/auto93.csv")
        best, rest, evals = d.branch()
        print("Centroid of output cluster:")
        print(pad_numbers(best.mid().cells), pad_numbers(rest.mid().cells))
        print("Evals: " + str(evals))

    def doubletap(self):
        d = Data("../data/auto93.csv")
        best1, rest, evals1 = d.branch(32)
        best2, _, evals2 = best1.branch(4)
        print(pad_numbers(best2.mid().cells), pad_numbers(rest.mid().cells))
        print(evals1 + evals2)

    def bins(self):
        bins("../data/auto93.csv", config.value.Beam)


def bins(file_path, Beam):
    d = Data(file_path)
    best, rest = d.branch()
    LIKE = best.rows
    random.shuffle(rest.rows)
    HATE = slice(rest.rows, 0, 3 * len(LIKE))

    def score(range):
        return range.score("LIKE", len(LIKE), len(HATE))

    t = []
    for col in d.cols.values():
        print("")
        for range in _ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
            oo(range)
            t.append(range)
    t.sort(key=lambda a, b: score(a) > score(b))
    max = score[0]

    print("\n#scores:\n")

    for v in slice(t, 0, Beam):
        if score(v) > max * 0.1:
            print(rnd(score(v)), o(v))
    oo({"LIKE": len(LIKE), "HATE": len(HATE)})


def _ranges(cols, rowss):
    t = []
    for col in cols:
        for range in _ranges1(col, rowss):
            t.append(range)
    return t


def _mergeds(ranges, too_few):
    i = 1
    t = {}

    while i <= len(ranges):
        a = ranges[i]
        if i < len(ranges):
            both = a.merged(ranges[i], too_few)
            if both:
                a = both
                i += 1
            t.append(a)
            i += 1

    if len(t) < len(ranges):
        return _mergeds(t, too_few)

    for i in range(2, len(t) + 1):
        t[i].x.lo = t[i - 1].x.hi
    t[i].x.lo = -1 * float("inf")
    t[-1].x.hi = float("inf")

    return t


def _ranges1(col, rowss):
    out = {}
    nrows = 0

    for y, rows in rowss.items():
        nrows += len(rows)

        for row in rows.values():
            x = row.cells[col.at]

            if x != "?":
                bin = col.bin(x)
                out[bin] = out[bin] if out[bin] else Range(col.at, col.txt, x)
                out[bin].add(x, y)
    out = as_list(out)
    out.sort(key=lambda a, b: a.x.lo < b.x.lo)
    return col.has if out else _mergeds(out, nrows / config.value.bins)
