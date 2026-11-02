"""場景 002：中型會議室（12 人，白板、投影）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("002", "meeting_room", "中型會議室", "Medium Meeting Room", "meeting", (8, 6),
          tags=["meeting", "12-seats", "whiteboard", "projector"])

# ---- 結構：門、窗
S.add_door("S", 3)
S.add_door("W", 3)
S.add_window("E", 4.2, width=2.4)
S.add_window("S", 6, width=1.8)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.light_grid(3, 2, margin=1.8, power=110)

# ---- 會議桌與 12 張椅子
TX, TY = 4.0, 3.0
F.rug(S, TX, TY, 5.4, 3.4, "rug_blue")
F.conference_table(S, TX, TY, 0, w=4.0, d=1.4)
cols = ("chair_seat", "chair_green", "chair_red", "fabric_teal")
n = 0
xs = [2.4, 3.2, 4.0, 4.8, 5.6]
for side, yy, yaw in (("S", TY - 1.15, 0), ("N", TY + 1.15, 180)):
    for x in xs:
        n += 1
        F.chair(S, x, yy, math.radians(yaw), color=cols[n % 4], name="Chair_%02d" % n)
        S.anchor("SEAT", "meeting", x, yy, yaw, n=n)
for x, yaw in ((TX - 2.5, -90), (TX + 2.5, 90)):
    n += 1
    F.chair(S, x, TY, math.radians(yaw), color=cols[n % 4], name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", x, TY, yaw, n=n)

# 桌上筆電（部分座位）
for x in (2.4, 4.0, 5.6):
    F.laptop(S, x, TY - 0.4, 0, z=0.77, name="Laptop_S_%d" % int(x * 10))
for x in (3.2, 4.8):
    F.laptop(S, x, TY + 0.4, math.radians(180), z=0.77, name="Laptop_N_%d" % int(x * 10))

# ---- 北牆：投影布幕＋吊掛投影機＋簡報位
F.projector_screen(S, 4.0, 5.8, 0, w=3.0, h=1.7)
F.projector(S, TX, TY - 0.2, 2.75, 0)
S.anchor("STAND", "presenter", 4.0, 5.0, 180, n=1)
S.anchor("POI", "projector", 5.8, 5.0, 180, n=1)  # 投影遙控/連接點（站在布幕旁）

# ---- 東牆：白板
F.whiteboard(S, 7.8, 1.6, math.radians(-90), w=2.4)
S.anchor("STAND", "whiteboard", 6.8, 1.6, -90, n=1)
S.anchor("STAND", "whiteboard", 6.8, 0.9, -90, n=2)

# ---- 西牆：邊櫃（茶水／文具）與北牆角植栽
F.credenza(S, 0.2 + 0.225, 5.0, math.radians(-90), w=1.6)
S.anchor("POI", "credenza", 1.3, 5.0, 90, n=1)
F.plant(S, 7.3, 5.3)
F.plant(S, 0.8, 0.8)

# ---- 狀態標籤
S.anchor("STATUS", "", TX, TY, n=1)
S.anchor("STATUS", "", 4.0, 5.0, n=2)

S.finish(HERE)
