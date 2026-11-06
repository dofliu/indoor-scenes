"""場景 010：走廊（十字路口）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F
import corridor as C

S = C.build("010", "corridor_cross", "走廊（十字路口）", "Corridor - Cross Junction", (2, 2), [("W", 1), ("E", 1), ("S", 1), ("N", 1)], ["cross", "junction"])
S.anchor("STATUS", "", 1.0, 1.0, n=1)
S.finish(HERE)
