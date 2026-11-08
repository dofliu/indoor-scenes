"""場景 011：主管辦公室（辦公桌、訪客座、沙發洽談區、書櫃）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("011", "executive_office", "主管辦公室", "Executive Office", "office", (6, 6),
          tags=["office", "executive", "private", "sofa-area"])
R = math.radians

S.add_door("S", 1)
S.add_door("E", 5)
S.add_window("N", 3, width=2.4)
S.add_window("N", 5, width=1.2)
S.add_window("E", 1.8, width=1.6)
S.build_shell(floor="floor_wood", accent={"N": "wall_accent"})
S.light_grid(2, 2, power=100)

# 主管桌（使用者坐北側，面南）
DX, DY = 3.0, 4.2
F.rug(S, 2.65, 3.7, 2.7, 3.0, "rug_blue")
F.desk(S, DX, DY, R(180), w=2.0, d=0.9, h=0.74, top="wood_dark", name="ExecDesk")
F.monitor(S, DX - 0.4, DY + 0.1, R(180), name="Monitor_01")
F.monitor(S, DX + 0.4, DY + 0.1, R(180), name="Monitor_02")
F.keyboard(S, DX - 0.4, DY - 0.15, R(180), name="Keyboard_01")
F.laptop(S, DX + 0.5, DY - 0.2, R(180), name="Laptop_01")
F.chair(S, DX, DY + 0.75, R(180), color="chair_red", name="ExecChair")
S.anchor("SEAT", "desk", DX, DY + 0.75, 180, n=1)
S.anchor("STATUS", "", DX, DY, n=1)

# 訪客座（面北）
for i, vx in enumerate((DX - 0.55, DX + 0.55), 1):
    F.chair(S, vx, 3.0, 0, color="chair_seat", name="VisitorChair_%d" % i)
    S.anchor("SEAT", "visitor", vx, 3.0, 0, n=i)

# 北牆：低櫃
F.cabinet(S, 1.6, 5.575, 0, w=0.9, h=0.9, name="Credenza_1")
F.cabinet(S, 4.4, 5.575, 0, w=0.9, h=0.9, name="Credenza_2")
S.anchor("POI", "credenza", 1.6, 5.0, 180, n=1)

# 西牆：書櫃（4 組）
for i in range(4):
    F.cabinet(S, 0.425, 2.0 + 0.9 * i, R(90), h=1.1, color="wood_light", name="Bookshelf_%d" % (i + 1))
S.anchor("POI", "bookshelf", 1.3, 3.4, 90, n=1)

# 東側：洽談區（沙發＋茶几＋單人椅）
F.rug(S, 4.8, 2.3, 1.6, 2.4, "rug")
F.sofa(S, 5.3, 2.3, R(90), w=2.0, d=0.9, color="fabric_grey", name="Sofa", seat_clear=True)
for i, sy in enumerate((1.8, 2.8), 1):
    S.anchor("SEAT", "sofa", 5.25, sy, 90, n=i)
F.coffee_table(S, 4.4, 2.3, R(90), w=1.0, d=0.5, name="CoffeeTable")
F.armchair(S, 4.1, 0.95, 0, color="fabric_teal", name="Armchair")
S.anchor("SEAT", "armchair", 4.1, 0.95, 0, n=1)
S.anchor("STATUS", "", 5.25, 2.3, n=2)

# 南牆：白板；植栽
F.whiteboard(S, 3.0, 0.2, R(180), w=1.8)
S.anchor("STAND", "whiteboard", 3.0, 1.1, 0, n=1)
for (px, py) in ((5.3, 5.3), (0.7, 5.3), (5.3, 0.65)):
    F.plant(S, px, py)

S.finish(HERE)
