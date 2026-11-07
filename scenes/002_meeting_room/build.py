"""場景 002：中型會議室（12 人，白板、投影）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("002", "meeting_room", "中型會議室", "Medium Meeting Room", "meeting", (8, 6),
          tags=["meeting", "whiteboard", "projector", "12-seats"])

# ---- 結構：門、窗
S.add_door("S", 5)
S.add_door("E", 3)
S.add_window("E", 5, width=1.6)
S.add_window("W", 1, width=1.2)
S.add_window("W", 5, width=1.6)
S.build_shell(floor="floor_wood", accent={"N": "wall_accent"})
S.light_grid(3, 2, margin=1.6, power=120)

TX, TY = 4.0, 2.9
F.rug(S, TX, TY, 5.6, 3.4, "rug_blue")

# ---- 會議長桌（兩段拼接，中間走線盒）
F.table(S, TX, TY, 0, w=4.2, d=1.4, top="wood_light", name="MeetingTable")
p = Piece(S, "TableBox", TX, TY, 0.74, coll="PROPS")
p.box(0, 0, 0.01, 0.35, 0.25, 0.02, "metal_dark")
p.finish(obstacle=False)

# ---- 12 席：長邊各 5、兩端各 1
n = 0
for i, dx in enumerate((-1.6, -0.8, 0.0, 0.8, 1.6)):
    n += 1  # 南側，面向北
    cx, cy = TX + dx, TY - 1.15
    F.chair(S, cx, cy, 0, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", cx, cy, 0, n=n)
for i, dx in enumerate((-1.6, -0.8, 0.0, 0.8, 1.6)):
    n += 1  # 北側，面向南
    cx, cy = TX + dx, TY + 1.15
    F.chair(S, cx, cy, math.pi, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", cx, cy, 180, n=n)
n += 1  # 西端，面向東
F.chair(S, TX - 2.6, TY, -math.pi / 2, color="chair_green", name="Chair_%02d" % n)
S.anchor("SEAT", "meeting", TX - 2.6, TY, -90, n=n)
n += 1  # 東端，面向西
F.chair(S, TX + 2.6, TY, math.pi / 2, color="chair_green", name="Chair_%02d" % n)
S.anchor("SEAT", "meeting", TX + 2.6, TY, 90, n=n)
# 桌面小物：筆電與水杯
for k, (lx, ly, yw) in enumerate(((-1.6, -0.35, 0), (0.0, -0.35, 0), (1.6, 0.35, 180))):
    F.laptop(S, TX + lx, TY + ly, math.radians(yw), z=0.74)

# ---- 北牆：投影布幕 + 簡報站位；天花板投影機
F.screen_wall(S, 4.0, 5.8, 3.2, h=1.8, yaw=0, z=0.9, name="ProjectionScreen")
pj = Piece(S, "Projector", TX, 2.0, 2.72, coll="PROPS")
pj.box(0, 0, 0.0, 0.34, 0.28, 0.11, "plastic_white")
pj.cyl(0, 0.16, 0.0, 0.045, 0.06, "plastic_black", seg=12, axis="Y")
pj.box(0, 0, 0.14, 0.05, 0.05, 0.17, "metal_dark")
pj.finish(obstacle=False)
S.anchor("STAND", "screen", 6.3, 4.9, 180, n=1)
S.anchor("STAND", "screen", 1.7, 4.9, 180, n=2)

# ---- 西牆：白板
F.whiteboard(S, 0.2, 4.4, math.radians(90), w=2.4, name="Whiteboard_W")
S.anchor("STAND", "whiteboard", 0.9, 4.4, -90, n=1)
S.anchor("STAND", "whiteboard", 0.9, 5.0, -90, n=2)

# ---- 南牆：低櫃（茶點／文具）
for i in range(2):
    F.cabinet(S, 1.3 + 0.9 * i, 0.2 + 0.225, math.pi, h=0.9, name="Credenza_%d" % (i + 1))
S.anchor("POI", "credenza", 1.75, 1.3, 180, n=1)

# ---- 東牆：飲水機、植栽
F.water_dispenser(S, 7.5, 5.0, math.radians(-90))
S.anchor("POI", "water", 6.7, 5.0, -90, n=1)
F.plant(S, 0.7, 0.7)
F.plant(S, 7.3, 0.7)

# ---- 狀態標籤（桌面中央上方）與燈座
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

S.finish(HERE)
