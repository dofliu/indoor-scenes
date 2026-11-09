"""場景 003：小型討論室／電話亭（4 人討論 + 2 個電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "huddle_room", "小型討論室／電話亭", "Huddle Room & Phone Booths", "meeting", (6, 4),
          tags=["meeting", "huddle", "phone-booth", "4-seats", "2-booths"])

# ---- 結構
S.add_door("S", 3)
S.add_door("W", 3)
S.add_window("W", 1, width=1.0)
S.build_shell(floor="floor_wood", accent={"N": "wall_accent"})
S.light_grid(2, 1, margin=1.4, power=110)

TX, TY = 2.6, 2.0
F.rug(S, TX, TY, 3.0, 2.2, "rug_blue")
F.table(S, TX, TY, 0, w=1.6, d=0.9, top="wood_light", name="HuddleTable")
n = 0
for dx in (-0.4, 0.4):
    n += 1
    F.chair(S, TX + dx, TY - 0.85, 0, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", TX + dx, TY - 0.85, 0, n=n)
for dx in (-0.4, 0.4):
    n += 1
    F.chair(S, TX + dx, TY + 0.85, math.pi, color="chair_green", name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", TX + dx, TY + 0.85, 180, n=n)
for lx, ly, yw in ((-0.4, -0.2, 0), (0.4, 0.25, 180)):
    F.laptop(S, TX + lx, TY + ly, math.radians(yw), z=0.74)

# ---- 北牆螢幕（避開門洞），站位在螢幕前
F.screen_wall(S, 2.6, 3.8, 1.5, h=0.85, yaw=0, z=1.0, name="DisplayWall")
S.anchor("STAND", "screen", 2.6, 3.0, 0, n=1)

# ---- 西牆下白板（窗間）與北牆角站位
F.whiteboard(S, 0.2, 2.0, math.radians(90), w=1.0, h=1.0, z=0.9, name="Whiteboard_W")
S.anchor("STAND", "whiteboard", 0.9, 2.0, -90, n=1)

# ---- 兩個電話亭（東側，開口朝西）
for i, by in enumerate((1.0, 3.0), 1):
    F.phone_booth(S, 5.2, by, name="PhoneBooth_%d" % i)
    S.anchor("SEAT", "booth", 5.15, by, 90, n=i)
    S.anchor("POI", "booth", 4.3, by, -90, n=i)  # 艙前等候／入口

F.plant(S, 0.7, 0.7)
F.plant(S, 1.0, 3.3)

# ---- 狀態標籤：桌上方，與各電話亭上方
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")
for i, by in enumerate((1.0, 3.0), 2):
    S.anchor("STATUS", "", 5.1, by, n=i, z=2.4)
    F.status_lamp(S, 5.1, by, z=2.4, name="StatusLamp_%02d" % i)

S.finish(HERE)
