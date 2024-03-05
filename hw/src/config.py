GATE_DOC = """
gate: guess, assess, try, expand
(c) 2023, Tim Menzies, BSD-2
Learn a little, guess a lot, try the strangest guess, learn a little more, repeat

USAGE:
  python3 gate.py [OPTIONS]

OPTIONS:
  -b --budget0  initial evals                   = 4
  -B --Budget   subsequent evals                = 5
  -c --cohen    small effect size               = .35
  -f --file     csv data file name              = ../data/diabetes.csv
  -h --help     show help                       = false
  -k --k        low class frequency kludge      = 1
  -m --m        low attribute frequency kludge  = 2
  -s --seed     random number seed              = 31210
  -t --todo     start up action                 = help
  -T --Top      best section                    = .5
"""

MYLO_DOC = """
mylo: recursive bi-clustering via random projections (lo is less. less is more. go lo)
(c) 2023, Tim Menzies, BSD-2

USAGE:
  python3 mylo.py [OPTIONS]

OPTIONS:
  -b --bins   max number of bins              = 16
  -B --Beam   max number of ranges            = 10
  -c --cohen  small effect size               = .35
  -C --Cut    ignore ranges less than C*max   = .1
  -d --d      frist cut                       = 32
  -D --D      second cut                      = 4
  -f --file   csv data file name              = ../data/diabetes.csv
  -F --Far    how far to search for faraway?  = .95
  -h --help   show help                       = false
  -H --Half   #items to use in clustering     = 256
  -p --p      weights for distance            = 2
  -s --seed   random number seed              = 31210
  -S --Support coeffecient on best            = 2
  -t --todo   start up action                 = help
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


config = None
if sys.argv[0] == "gate.py":
    config = Config(GATE_DOC)
elif sys.argv[0] == "mylo.py":
    config = Config(MYLO_DOC)
else:
    print("Config is being called from an unknown file")
    sys.exit(1)
