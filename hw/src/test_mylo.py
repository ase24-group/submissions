from data import Data


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
