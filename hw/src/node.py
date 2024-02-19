class Node:
    def __init__(self, data):
        self.here = data

    # Walks over the tree and calls 'fun' on each node of the tree
    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun, depth+1)
        if self.rights:
            self.rights.walk(fun, depth+1)


