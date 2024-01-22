"""
gate: guess, assess, try, expand
(c) 2023, Tim Menzies, BSD-2
Learn a little, guess a lot, try the strangest guess, learn a little more, repeat

USAGE:
  lua gate.lua [OPTIONS]

OPTIONS:
  -c --cohen    small effect size               = .35
  -f --file     csv data file name              = ../data/diabetes.csv
  -h --help     show help                       = false
  -k --k        low class frequency kludge      = 1
  -m --m        low attribute frequency kludge  = 2
  -s --seed     random number seed              = 31210
  -t --todo     start up action                 = help
"""

from config import get_config
from test import Test
from box import Box
import random, sys
from data import Data

config = get_config(__doc__)
test = Test(config)


def run(todo):
    b4 = Box(test.config.copy())
    random.seed(test.config.seed)
    test_fun = getattr(test, todo, None)

    oops = test_fun() == False
    if oops:
        print(f"❌ FAIL {todo}")
        sys.exit(1)
    else:
        print(f"✅ PASS {todo}")

    test.config = b4

    return oops


def run_all():
    all_attributes = dir(test)
    methods = [
        attr
        for attr in all_attributes
        if callable(getattr(test, attr)) and (not attr.startswith("_"))
    ]

    bad = 0
    for method in methods:
        if run(method):
            bad += 1

    print(f'{"❌ FAIL" if bad > 0 else "✅ PASS"} {bad} fail(s)')
    sys.exit(bad)


def learn(data, row, my, kl) -> None:
    my.n += 1
    kl = row.cells[data.cols.klass.at]
    if my.n > 10:
        my.tries += 1
        my.acc = 1 if kl == row.likes(my.datas) else 0
    my.datas[kl] = my.datas.get(kl, Data(data.cols.names))  # default value --> new data
    my.datas[kl].add(row)


if config.todo == "all":
    run_all()
else:
    run(config.todo)
