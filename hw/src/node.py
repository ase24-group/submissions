import utils


class Node:
    def __init__(
        self, data, left=None, right=None, C=None, cut=None, lefts=None, rights=None
    ):
        self.here = data
        self.left = left
        self.right = right
        self.C = C
        self.cut = cut
        self.lefts = lefts
        self.rights = rights

    # Walks over the tree and calls 'fun' on each node of the tree
    def walk(self, fun, depth=0):
        fun(self, depth, not (self.lefts or self.rights))
        if self.lefts:
            self.lefts.walk(fun, depth + 1)
        if self.rights:
            self.rights.walk(fun, depth + 1)

    # Prints a tree by printing each node in order
    def show(self):
        def d2h(data):
            return f" {round(data.mid().d2h(self.here), 2):<3}"

        max_depth = 0

        def _show(node, depth, leafp):
            nonlocal max_depth
            post = (
                (str(d2h(node.here)) + "\t" + utils.pad_numbers(node.here.mid().cells))
                if leafp
                else ""
            )
            max_depth = max(max_depth, depth)
            print(("|.. ") * depth + post)

        self.walk(_show)
        print(
            "\n"
            + ("    ") * max_depth
            + str(d2h(self.here))
            + "\t"
            + utils.pad_numbers(self.here.mid().cells)
        )
        print(("    ") * max_depth + " _      " + str(self.here.cols.names))
