import sys
from test_gate import TestGate
from test_mylo import TestMylo


test = None
if sys.argv[0] == "gate.py":
    test = TestGate()
elif sys.argv[0] == "mylo.py":
    test = TestMylo()
else:
    print("Test is being called from an unknown file")
    sys.exit(1)
