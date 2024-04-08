import fileinput, re, ast
import random
import math
from typing import Tuple


# Reference: https://discord.com/channels/1191838787219759154/1192507528882438247/1195863830136377345
# Returns the values in the next row of the CSV as a list along with the row number of the next
def csv(filename: str = "-"):
    i = 0
    with fileinput.FileInput(None if filename == "-" else filename) as src:
        for line in src:
            line = re.sub(r'([\n\t\r"\' ]|#.*)', "", line)
            if line:
                i += 1
                yield i, [coerce(x) for x in line.split(",")]


def output(x):
    items = ", ".join([f"{k}: {v}" for k, v in sorted(x.items()) if k[0] != "_"])
    return f"{{{items}}}"


def coerce(s: str):
    # Converts string rep to python datatype
    try:
        return ast.literal_eval(s)
    except Exception:
        return s.strip()


def slice(t: list, go: int = None, stop: int = None, inc: int = None) -> list:
    go = go or 0
    stop = stop or len(t)
    inc = inc or 1

    if go < 0:
        go += len(t)
    if stop < 0:
        stop += len(t)

    return t[go:stop:inc]


def output_gate20_info(info):
    for i, (k, v) in enumerate(info.items()):
        for t in v:
            print(f"{i + 1}. {k:<5} {pad_numbers(t)}")
        print()


def pad_numbers(t):
    s = ""
    if isinstance(t[0], list):
        s = f"[{', '.join([f'{pad_numbers(v)}' for v in t])}]"
    else:
        s = f"[{', '.join([f'{v:5.2f}' for v in t])}]"
    return s


def align_list(lst, precision=2, pad=15):
    out = "["
    for i, cell in enumerate(lst):
        if isinstance(cell, (int, float)):
            cell = cell if int(cell) == cell else round(cell, precision)
        if isinstance(cell, str):
            cell = f"'{cell}'"
        out += f"{str(cell):{pad if i < (len(lst) - 1) else 0}}"
    out += "]"
    return out


def any(t):
    return random.choice(t)


def many(t, n):
    if n == None:
        n = len(t)

    u = []
    for i in range(n):
        u.append(any(t))

    return u


def oo(x):
    print(o(x))
    return x


def o(t, n=2):
    if isinstance(t, (int, float)):
        return str(round(t, n))
    if not isinstance(t, dict):
        return vars(t)

    u = []
    for k, v in t.items():
        if not str(k).startswith("_"):
            if len(t) > 0:
                u.append(o(v, n))
            else:
                u.append(f"{o(k, n)}: {o(v, n)}")

    return "{" + ", ".join(u) + "}"


def as_list(t):
    return [v for v in t.values()]


def score(t, goal, LIKE, HATE, Support):
    like = 0
    hate = 0
    tiny = 1e-30

    for klass, n in t.items():
        if klass == goal:
            like += n
        else:
            hate += n

    like = like / (LIKE + tiny)
    hate = hate / (HATE + tiny)

    if hate > like:
        return 0
    else:
        return like**Support / (like + hate)


def entropy(t: dict) -> Tuple[float]:
    n = 0
    for v in t.values():
        n += v

    e = 0
    for v in t.values():
        e -= v / n * math.log2(v / n)

    return e, n
