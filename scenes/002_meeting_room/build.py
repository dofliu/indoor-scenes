"""場景 002：中型會議室（12 人，白板、投影）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("002", "meeting_room", "中型會議室", "Medium Meeting Room", "meeting", (8, 6),
          tags=["meeting", "whiteboard", "projector", "12-seats"])

# ---- 結構：兩個南門、窗
S.add_door("S", 3)
S.add_door("S", 7)
S.add_window("S", 5, width=2.4)
S.add_window("E", 3, width=2.4)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.light_grid(3, 2, margin=1.5, power=110)

TX, TY = 4.2, 3.2  # 會議桌中心
F.rug(S, TX, TY, 5.6, 3.4, "rug_blue")
F.conference_table(S, TX, TY, 0, w=4.0, d=1.4)

# ---- 12 個座位：南北各 5、東西各 1
n = 0
seats = []
for i in range(5):
    x = 2.6 + 0.8 * i
    seats.append((x, TY - 1.25, 0))      # 南側，面向北
    seats.append((x, TY + 1.25, 180))    # 北側，面向南
seats.append((TX - 2.6, TY, -90))        # 西端，面向東
seats.append((TX + 2.6, TY, 90))         # 東端，面向西
cols = ("chair_seat", "chair_green", "chair_red", "fabric_teal")
for k, (x, y, yaw) in enumerate(seats, 1):
    F.chair(S, x, y, math.radians(yaw), color=cols[k % 4], name="Chair_%02d" % k)
    S.anchor("SEAT", "meeting", x, y, yaw, n=k)
S.anchor("STATUS", "", TX, TY, n=1, z=2.2)

# ---- 北牆東側：投影布幕＋吊掛投影機（會議桌上方）
F.projector_screen(S, 5.0, 5.8, w=2.8, h=1.6, z=1.1)
F.projector(S, 4.6, TY, S.H, yaw=0)
S.anchor("STAND", "presenter", 5.0, 5.2, 180, n=1)

# ---- 北牆西側：白板
F.whiteboard(S, 1.8, 5.8, 0, w=2.0)
S.anchor("STAND", "whiteboard", 1.3, 5.2, 180, n=1)
S.anchor("STAND", "whiteboard", 2.3, 5.2, 180, n=2)

# ---- 東牆：服務櫃（下方）＋飲水機
for i, yc in enumerate((2.2, 3.1, 4.0), 1):
    F.cabinet(S, 7.8 - 0.225, yc, math.radians(-90), w=0.9, d=0.45, h=0.85, name="Credenza_%d" % i)
F.water_dispenser(S, 7.55, 5.1, math.radians(-90))
S.anchor("POI", "credenza", 6.9, 3.1, -90, n=1)
S.anchor("POI", "water", 6.9, 5.1, -90, n=1)

# ---- 植栽
for (px, py) in ((0.7, 0.7), (7.3, 0.7), (0.7, 5.3)):
    F.plant(S, px, py)

S.finish(HERE)
