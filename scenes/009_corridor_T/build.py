"""場景 009：走廊（T 型岔路）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F
import corridor as C

S = C.build("009", "corridor_T", "走廊（T 型岔路）", "Corridor - T Junction", (2, 2), [("W", 1), ("E", 1), ("N", 1)], ["T", "junction"])
S.anchor("STATUS", "", 1.0, 1.0, n=1)
S.finish(HERE)
