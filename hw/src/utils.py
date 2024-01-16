import fileinput, re, ast

# Reference: https://discord.com/channels/1191838787219759154/1192507528882438247/1195863830136377345
# Returns the values in the next row of the CSV as a list along with the row number of the next
def csv(filename="-"):
    i = 0
    with fileinput.FileInput(None if filename=="-" else filename) as src:
        for line in src:
            line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
            if line:
                i += 1
                yield i, [coerce(x) for x in line.split(",")]

def output(x):
    items = ", ".join([f"{k}: {v}" for k, v in sorted(x.items()) if k[0] != "_"])
    return f"{{{items}}}"

def coerce(s):
   try: return ast.literal_eval(s)
   except Exception: return s.strip()
