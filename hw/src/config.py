import re, sys
from box import Box
from utils import coerce

def doc(docstring):
    return Box(**{m[1]:coerce(m[2]) for m in re.finditer(r"--(\w+)[^=]*=\s*(\S+)", docstring)}), docstring

def cli(doc, docstring):
    for k, v in doc.items():
        v = str(v)
        for i, arg in enumerate(sys.argv):
            if arg in ["-h", "--help"]:
                sys.exit(print(docstring))
            if arg in ["-"+k[0], "--"+k]:
                v = "false" if v=="true" else ("true" if v=="false" else sys.argv[i+1])
                doc[k] = coerce(v)
    return doc

def get_config(docstring):
    return cli(*doc(docstring))
