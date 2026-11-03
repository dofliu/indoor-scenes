"""場景 002：中型會議室（12 人，白板、投影）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("002", "meeting_room", "中型會議室", "Medium Meeting Room", "meeting", (10, 8),
          tags=["meeting", "whiteboard", "projector", "12-seats"])

# ---- 結構：門、窗
S.add_door("S", 3)
S.add_door("E", 1)
S.add_window("S", 7, width=2.4)
for off in (3, 7):
    S.add_window("W", off, width=2.4)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.light_grid(3, 2, margin=1.8, power=110)

# ---- 會議桌（5.0×1.6）與 12 把椅
TX, TY = 5.0, 4.0
F.conference_table(S, TX, TY)
F.rug(S, TX, TY, 7.0, 3.6, "rug_blue")
seats = []
for i, dx in enumerate((-1.9, -0.95, 0, 0.95, 1.9)):       # 南側 5 席，面向北
    seats.append((TX + dx, TY - 1.2, 0))
for i, dx in enumerate((-1.9, -0.95, 0, 0.95, 1.9)):       # 北側 5 席，面向南
    seats.append((TX + dx, TY + 1.2, 180))
seats.append((TX - 3.1, TY, -90))                          # 西端，面向東
seats.append((TX + 3.1, TY, 90))                           # 東端，面向西
cols = ("chair_seat", "chair_seat", "chair_green", "chair_seat")
for n, (cx, cy, yaw) in enumerate(seats, 1):
    F.chair(S, cx, cy, math.radians(yaw), color=cols[n % 4], name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", cx, cy, yaw, n=n)
    S.anchor("STATUS", "", cx, cy, n=n)
F.conference_phone(S, TX, TY, yaw=0)
for dx in (-1.6, 1.6):
    for sy in (-0.45, 0.45):
        F.laptop(S, TX + dx, TY + sy, math.radians(0 if sy < 0 else 180))

# ---- 北牆：投影布幕＋投影機
F.projector_screen(S, TX, 7.8, w=3.0, h=1.7, z=0.9)
F.projector(S, TX, TY - 0.2, S.H)
S.anchor("STAND", "presenter", TX + 2.2, 6.9, 180, n=1)
S.anchor("POI", "screen", TX, 6.9, 180, n=1)

# ---- 東牆：白板
F.whiteboard(S, 9.8, 5.2, math.radians(90), w=2.4)
S.anchor("STAND", "whiteboard", 8.8, 4.6, 90, n=1)
S.anchor("STAND", "whiteboard", 8.8, 5.8, 90, n=2)

# ---- 南牆：置物櫃與咖啡區（門在 S3，櫃從 x=5.2 起）
for i in range(4):
    F.cabinet(S, 5.65 + 0.9 * i, 0.2 + 0.25, math.radians(180), w=0.9, d=0.5, h=0.8, name="Credenza_%d" % (i + 1))
F.coffee_machine(S, 6.1, 0.45, yaw=math.radians(180))
F.coffee_machine(S, 7.0, 0.45, yaw=math.radians(180))
S.anchor("POI", "coffee", 6.5, 1.3, 180, n=1)
S.anchor("POI", "cabinet", 8.3, 1.3, 180, n=2)

# ---- 植栽
for (px, py) in ((0.7, 7.2), (9.3, 7.2), (0.7, 0.9)):
    F.plant(S, px, py)

S.finish(HERE)
