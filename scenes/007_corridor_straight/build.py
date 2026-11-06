"""場景 007：走廊（直線）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F
import corridor as C

S = C.build("007", "corridor_straight", "走廊（直線）", "Corridor - Straight", (8, 2), [("W", 1), ("E", 1), ("S", 3), ("S", 7), ("N", 3), ("N", 7)], ["straight"])
C.extinguisher(S, 5.0, 0.2, 90, "Extinguisher_1")
C.exit_sign(S, 7.7, 1.0, 2.35, 90, "ExitSign_1")
S.anchor("STATUS", "", 4.0, 1.0, n=1)
S.anchor("STATUS", "", 6.0, 1.0, n=2)
S.finish(HERE)
