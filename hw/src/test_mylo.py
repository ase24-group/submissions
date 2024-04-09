import math
from data import Data
from utils import pad_numbers, slice, as_list, powerset
import random
from config import config
from range import Range
from sym import Sym
from rules import Rules


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

    def rules(self):
        d = Data("../data/auto93.csv")

        best0, rest, evals1 = d.branch(config.value.d)
        best, _, evals2 = best0.branch(config.value.D)
        print(f"evals: {evals1 + evals2 + config.value.D - 1}")
        LIKE = best.rows
        random.shuffle(rest.rows)
        HATE = slice(rest.rows, 0, 3 * len(LIKE))
        rowss = {"LIKE": LIKE, "HATE": HATE}
        rules = Rules(_ranges(d.cols.x, rowss), "LIKE", rowss).sorted

        print(f"{'score':<{9}}{'mid selected':<{64}}{'rule':<{10}}")
        for _, rule in enumerate(rules):
            result = d.clone(rule.selects(rest.rows))
            if len(result.rows) > 0:
                result.rows = sorted(result.rows, key=lambda a: a.d2h(d))
                print(
                    round(rule.scored, 2),
                    "\t",
                    pad_numbers(result.mid().cells),
                    "\t",
                    rule.show(),
                )

    def rules2(self):
        d = Data("../data/auto93.csv")
          
        tmp = random.sample(d.rows, len(d.rows))
        train = d.clone(tmp[:math.floor(len(tmp)/2)])
        test  = d.clone(tmp[math.floor(len(tmp)/2) + 1:])
        test.rows = sorted(test.rows, key=lambda a: a.d2h(d))
        print("base",  round(test.mid().d2h(d)), round(test.rows[0].d2h(d)),"\n")
        random.shuffle(test.rows)
        
        best0, rest, evals1 = train.branch(config.value.d)
        best, _, evals2 = best0.branch(config.value.D)
        print(f"evals: {evals1 + evals2 + config.value.D - 1}")
        LIKE = best.rows
        random.shuffle(rest.rows)
        HATE = slice(rest.rows, 0, 3 * len(LIKE))
        rowss = {"LIKE": LIKE, "HATE": HATE}

        random.shuffle(test.rows)

        rand = test.clone(slice(test.rows, 1, evals1 + evals2 + config.value.D - 1))
        rand.rows = sorted(rand.rows, key=lambda a: a.d2h(d))
        rules = Rules(_ranges(train.cols.x, rowss), "LIKE", rowss).sorted

        for _, rule in enumerate(rules):
            result = train.clone(rule.selects(test.rows))
            if len(result.rows) > 0:
                result.rows = sorted(result.rows, key=lambda a: a.d2h(d))
                print(
                    round(rule.scored, 2),
                    "\t",
                    pad_numbers(result.mid().cells),
                    "\t",
                    rule.show(),
                )
                # print(l.rnd(rule.scored), l.rnd(result:mid():d2h(d)), l.rnd(result.rows[1]:d2h(d)),
                #                         l.rnd(rand:mid():d2h(d)), l.rnd(rand.rows[1]:d2h(d)),
                #                          l.o(result:mid().cells),"\t",rule:show()) end

def bins(file_path, Beam):
    d = Data(file_path)
    best, rest, _ = d.branch()
    LIKE = best.rows
    random.shuffle(rest.rows)
    HATE = slice(rest.rows, 0, 3 * len(LIKE))

    def score(range):
        return range.score("LIKE", len(LIKE), len(HATE))

    t = []
    for col in d.cols.x.values():
        print("")
        for range in _ranges1(col, {"LIKE": LIKE, "HATE": HATE}):
            print(vars(range))
            t.append(range)

    t.sort(key=lambda x: score(x), reverse=True)
    max = score(t[0])

    print("\n#scores:\n")

    for v in slice(t, 0, Beam):
        if score(v) > max * 0.1:
            print(round(score(v), 2), "\t", vars(v))
    print({"LIKE": len(LIKE), "HATE": len(HATE)})


def _ranges(cols, rowss):
    t = []
    for _, col in cols.items():
        for range in _ranges1(col, rowss):
            t.append(range)
    return t


def _mergeds(ranges, too_few):
    i = 0
    t = []

    # for i, range in enumerate(ranges.values()):
    #     if i != len(ranges) - 1:
    #         both = range.merged(ranges[i + 1], too_few)
    #         if both:
    #             range = both
    while i < len(ranges):
        a = ranges[i]
        if i < len(ranges) - 1:
            both = a.merged(ranges[i + 1], too_few)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1

    if len(t) < len(ranges):  # and len(t) > 2:
        return _mergeds(t, too_few)

    for i in range(1, len(t)):
        t[i].x["lo"] = t[i - 1].x["hi"]

    if len(t) > 0:
        t[0].x["lo"] = -1 * float("inf")
        t[-1].x["hi"] = float("inf")

    return t


def _ranges1(col, rowss):
    out = {}
    nrows = 0

    for y, rows in rowss.items():
        nrows += len(rows)

        for row in rows:
            x = row.cells[col.at]

            if x != "?":
                bin = col.bin(x)
                out[bin] = out[bin] if out.get(bin) else Range(col.at, col.txt, x)
                out[bin].add(x, y)

    out = as_list(out)
    out.sort(key=lambda x: x.x["lo"])

    if type(col) == Sym:
        return out
    else:
        return _mergeds(out, nrows / config.value.bins)
