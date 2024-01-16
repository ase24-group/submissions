import ast

def output(x):
    class_name = x.__class__.__name__
    items = ", ".join([f"{k}:{v}" for k, v in x.items() if k[0] != "_"])
    return f"{class_name} {{{items}}}"

def coerce(x):
   try: return ast.literal_eval(x)
   except Exception: return x.strip()
