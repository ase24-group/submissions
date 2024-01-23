"""
gate: guess, assess, try, expand
(c) 2023, Tim Menzies, BSD-2
Learn a little, guess a lot, try the strangest guess, learn a little more, repeat

USAGE:
  python3 gate.py [OPTIONS]

OPTIONS:
  -c --cohen    small effect size               = .35
  -f --file     csv data file name              = ../data/diabetes.csv
  -h --help     show help                       = false
  -k --k        low class frequency kludge      = 1
  -m --m        low attribute frequency kludge  = 2
  -s --seed     random number seed              = 31210
  -t --todo     start up action                 = help
"""

import re, sys
from utils import coerce
from box import Box


class Config:
    def __init__(self, docstring):
        self.docstring = docstring
        self.set_config()

    def doc(self):
        return Box(
            **{
                m[1]: coerce(m[2])
                for m in re.finditer(r"--(\w+)[^=]*=\s*(\S+)", self.docstring)
            }
        )

    def cli(self, doc):
        for k, v in doc.items():
            v = str(v)
            for i, arg in enumerate(sys.argv):
                if arg in ["-h", "--help"]:
                    sys.exit(print(self.docstring))
                if arg in ["-" + k[0], "--" + k]:
                    v = (
                        "false"
                        if v == "true"
                        else ("true" if v == "false" else sys.argv[i + 1])
                    )
                    doc[k] = coerce(v)
        return doc

    def set_config(self):
        self.value = self.cli(self.doc())


config = Config(__doc__)
