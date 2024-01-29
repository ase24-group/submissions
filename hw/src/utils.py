import fileinput, re, ast
from lua import lua


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

def shuffle(t):
    u = []
    for x in t:
        u.append(x)

    for i in range(len(u), 1, -1):
        j = lua.execute(f"return math.random(1, {i})")
        u[i-1], u[j-1] = u[j-1], u[i-1]

    return u
