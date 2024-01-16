import re
import copy

class COLS:
    def __init__(self, row):
        self.x, self.y = {}, {}
        self.all = []
        self.klass = None
        self.names = row.cells
        for at in range(len(row.cells)):
            txt = row.cells[at]
            print(f"At: {at}, txt: {txt}")
            if re.match("^[A-Z]", txt):
                col = NUM(txt,at)
            else:
                col = SYM(txt,at)
            all.append(col)
            if not re.match(txt, "X$"):
                if re.match(txt, "X$"):
                    self.klass=col
                self.temp = self.y if re.match(txt, "[!+-]$") else self.x
                if re.match(txt, "[!+-]$"):
                    self.y[at] = col
                else:
                    self.x[at] = col
            
    def add(self, row):
        for _, cols in self.x.items():
            print("COLS: " + str(cols))
            for col in cols.items():
                print("col: " + str(col))
                col.add(row.cells[col.at])
        return row