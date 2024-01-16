from utils import output


class Box(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __repr__ = lambda x: output(x)
