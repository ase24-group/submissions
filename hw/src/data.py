import utils

class Data:
    def __init__(self, src, fun):
        self.rows = []
        self.cols = None
        self.adds(src, fun)

    def adds(self, src, fun):
        if type(src) == "string":
            for _, x in utils.csv(src):
                self.add(x, fun)
        else:
            for _, x in (src or []):
                self.add(x, fun)
        return self

    def add(self, t, fun, row):
        row = t if t.cells else Row(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = Cols(row)   

    def mid(self, cols):
        u=[]
        for _,col in (cols or self.cols.all):
            u.append(col.mid())
        return Row(u)
    
    def div(self, cols):
        u = []
        for _, col in (cols or self.cols.all):
            u.append(col.div())
        return Row(u)
    
    def stats(self, cols, fun, ndivs):
        u = {'.N': len(self.rows)}
        for _,col in self.cols[cols or "y"]:
            u[col.txt] = utils.rnd(self.mid(col), ndivs)
        return u
    




    
