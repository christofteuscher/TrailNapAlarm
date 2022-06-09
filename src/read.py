# Sample code for pipe commands

import sys
import numpy as np
import os

os.environ["PYTHONUNBUFFERED"] = "1"

for line in sys.stdin:
    match line.split():
        case ["QUIT"]:
            os.exit()
        case ["RESET"]:
            print("Do Reset")
        case ["FILE", filename]:
            print("Do File", filename)

# py -3 send.py | py -3 -u read.py