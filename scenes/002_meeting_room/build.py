"""場景 002：中型會議室（12 人，白板、投影）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("002", "meeting_room", "中型會議室", "Medium Meeting Room", "meeting", (10, 8),
          tags=["meeting", "12-seats", "whiteboard", "projector"])

# ---- 結構
S.add_door("S", 7)
S.add_door("W", 5)
for off in (2, 8):
    S.add_window("N", off, width=1.6, sill=1.0, height=1.4)
S.add_window("W", 1.5 + 0.5, width=1.6, sill=1.0, height=1.4)
S.add_window("S", 3, width=2.0, sill=1.0, height=1.4)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.light_grid(3, 2, power=110)

CX, CY = 5.0, 4.0
F.rug(S, CX, CY, 6.8, 3.8, "rug_blue")

# ---- 會議桌 4.8 x 1.4 ＋ 12 椅
F.table(S, CX, CY, 0, w=4.8, d=1.4, h=0.74, top="wood_dark", name="ConferenceTable")
n = 0
for i in range(5):
    x = CX - 1.8 + 0.9 * i
    for yy, yaw, tag in ((CY - 1.15, 0, "S"), (CY + 1.15, 180, "N")):
        n += 1
        F.chair(S, x, yy, math.radians(yaw), color=("chair_seat", "chair_green")[n % 2], name="Chair_%02d" % n)
        S.anchor("SEAT", "meeting", x, yy, yaw, n=n)
        F.laptop(S, x, CY + (-0.45 if yaw == 0 else 0.45), math.radians(yaw), z=0.74, name="Laptop_%02d" % n) if n in (1, 4, 7) else None
for ex, yaw in ((CX - 3.1, -90), (CX + 3.1, 90)):
    n += 1
    F.chair(S, ex, CY, math.radians(yaw), color="chair_red", name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", ex, CY, yaw, n=n)

# ---- 桌上設備：會議電話、水瓶、筆記本
p = Piece(S, "ConfPhone", CX, CY, 0.76, coll="PROPS")
p.cyl(0, 0, 0.0, 0.14, 0.03, "plastic_black", seg=20)
p.finish(footprint=None, obstacle=False)
for dx in (-1.4, 1.4):
    F.round_table  # 保留共用函式參照
    q = Piece(S, "Carafe_%s" % ("L" if dx < 0 else "R"), CX + dx, CY, 0.76, coll="PROPS")
    q.cyl(0, 0, 0.1, 0.05, 0.2, mat("water_blue", (0.5, 0.75, 0.95), rough=0.1, alpha=0.6), seg=12)
    q.finish(footprint=None, obstacle=False)

# ---- 北牆：投影布幕（可收起白色布幕）＋吸頂投影機
sc = Piece(S, "ProjectorScreen", CX, S.D - 0.2, 1.0, coll="PROPS")
sc.box(0, -0.02, 0.9, 3.2, 0.03, 1.8, "metal")
sc.box(0, -0.04, 0.9, 3.1, 0.005, 1.7, "whiteboard")
sc.box(0, -0.03, 1.82, 3.3, 0.08, 0.08, "metal_dark")
sc.finish(obstacle=False)
pj = Piece(S, "Projector", CX, CY, S.H - 0.35, coll="PROPS")
pj.box(0, 0, 0.1, 0.36, 0.3, 0.12, "plastic_white")
pj.cyl(0, 0.17, 0.1, 0.04, 0.05, "plastic_black", seg=12, axis="Y")
pj.box(0, 0, 0.2, 0.04, 0.04, 0.2, "metal_dark")
pj.finish(obstacle=False)
S.anchor("POI", "projector", CX, 1.8, 0, n=1)

# ---- 東牆：白板（雙面板）
F.whiteboard(S, S.W - 0.2, CY, math.radians(-90), w=3.0)
S.anchor("STAND", "whiteboard", S.W - 1.1, CY - 0.8, -90, n=1)
S.anchor("STAND", "whiteboard", S.W - 1.1, CY + 0.8, -90, n=2)
S.anchor("STAND", "present", CX - 2.0, S.D - 1.2, 0, n=1)
S.anchor("POI", "screen", CX, S.D - 1.0, 0, n=1)

# ---- 南牆：飲水與低櫃
for i in range(3):
    F.cabinet(S, 1.3 + 0.9 * i, 0.2 + 0.225, math.radians(180), h=0.9, name="Credenza_%d" % (i + 1)) if False else None
for i in range(3):
    F.cabinet(S, 5.0 + 0.9 * i, 0.2 + 0.225, math.radians(180), name="Cabinet_%d" % (i + 1))
F.water_dispenser(S, 9.4, 0.7, math.radians(180))
S.anchor("POI", "water", 9.4, 1.4, 180, n=1)
S.anchor("POI", "cabinet", 6.4, 1.2, 180, n=1)

# ---- 植栽
for (px, py) in ((0.7, 0.7), (9.3, 7.3), (0.7, 7.3)):
    F.plant(S, px, py)

# ---- 狀態標示
S.anchor("STATUS", "", CX, CY, n=1)
S.anchor("STATUS", "", S.W - 1.1, CY, n=2)
S.anchor("STATUS", "", CX - 2.0, S.D - 1.2, n=3)
F.status_lamp(S, CX, 1.6 + 0.0, z=2.0, name="StatusLamp_Door")

S.finish(HERE)
