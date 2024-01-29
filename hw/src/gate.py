"""
gate: guess, assess, try, expand
(c) 2023, Tim Menzies, BSD-2
Learn a little, guess a lot, try the strangest guess, learn a little more, repeat
"""

import random, sys
from test import Test
from box import Box
from config import config

test = Test()


def run(todo):
    b4 = Box(config.value.copy())
    random.seed(config.value.seed)
    test_fun = getattr(test, todo, None)

    oops = test_fun() == False
    if oops:
        print(f"❌ FAIL {todo}\n")
    else:
        print(f"✅ PASS {todo}\n")

    config.value = b4

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
        try:
            if run(method):
                bad += 1
        except Exception as err:
            print(f"Python Error: {err}")

    print(f'{"❌ FAIL" if bad > 0 else "✅ PASS"} {bad} fail(s)')
    if bad > 0:
        sys.exit(1)


if config.value.todo == "all":
    run_all()
else:
    run(config.value.todo)
