"""場景 008：走廊（L 型轉角）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F
import corridor as C

S = C.build("008", "corridor_L", "走廊（L 型轉角）", "Corridor - L Corner", (2, 2), [("W", 1), ("N", 1)], ["L", "corner"])
S.anchor("STATUS", "", 1.0, 1.0, n=1)
S.finish(HERE)
