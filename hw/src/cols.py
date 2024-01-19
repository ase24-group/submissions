import re
from sym import Sym
from num import Num


class Cols:
    def __init__(self, row):
        self.x, self.y = {}, {}
        self.all = []
        self.klass = None
        self.names = row.cells
        for at in range(len(row.cells)):
            txt = row.cells[at]
            if re.match(r"^[A-Z]", txt):
                col = Num(txt, at)
            else:
                col = Sym(txt, at)
            self.all.append(col)
            if not re.match(r".*X$", txt):
                if re.match(r".*!$", txt):
                    self.klass = col
                self.temp = self.y if re.match(r".*[!+-]$", txt) else self.x
                if re.match(r".*[!+-]$", txt):
                    self.y[at] = col
                else:
                    self.x[at] = col

    def add(self, row):
        for _, col in self.x.items():
            col.add(row.cells[col.at])

        for _, col in self.y.items():
            col.add(row.cells[col.at])
        return row
