"""場景 001：開放式工位辦公區（16 工位）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("001", "open_office", "開放式工位辦公區", "Open-plan Office", "office", (16, 12),
          tags=["office", "workstation", "open-plan", "16-seats"])


def loc(x, y, yaw, lx, ly):
    c, s = math.cos(yaw), math.sin(yaw)
    return x + lx * c - ly * s, y + lx * s + ly * c


# ---- 結構：門、窗
for wall, off in (("S", 3), ("S", 13), ("W", 5), ("E", 7), ("N", 15)):
    S.add_door(wall, off)
for off in (4, 8, 12):
    S.add_window("N", off, width=2.4)
for off in (3, 10.5):
    S.add_window("E", off, width=2.4)
S.add_window("W", 2, width=2.4)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.light_grid(4, 3, power=90)

# ---- 兩個島型工位區（每區 2 排 × 2 桌 × 2 = 8 工位）
n = 0
for pcx in (5.5, 10.5):
    for yc in (3.9, 8.1):
        F.rug(S, pcx, yc, 3.8, 3.4, "rug_blue")
        for side, yaw in ((-1, 0.0), (1, math.pi)):
            for sx in (-0.75, 0.75):
                n += 1
                dx, dy = pcx + sx, yc + side * 0.4
                F.desk(S, dx, dy, yaw, name="Desk_%02d" % n)
                mx, my = loc(dx, dy, yaw, 0, 0.12)
                F.monitor(S, mx, my, yaw, name="Monitor_%02d" % n)
                kx, ky = loc(dx, dy, yaw, 0, -0.12)
                F.keyboard(S, kx, ky, yaw, name="Keyboard_%02d" % n)
                cx, cy = loc(dx, dy, yaw, 0, -0.75)
                F.chair(S, cx, cy, yaw, color=("chair_seat", "chair_green", "chair_red", "fabric_teal")[n % 4], name="Chair_%02d" % n)
                sx_, sy_ = loc(dx, dy, yaw, 0, -0.75)
                S.anchor("SEAT", "desk", sx_, sy_, math.degrees(yaw), n=n)
                S.anchor("STATUS", "", dx, dy, n=n)
        F.divider(S, pcx, yc, 2.9, name="Divider_%d" % (n // 4))

# ---- 西側：協作桌（4 人）與白板
F.table(S, 2.6, 7.0, 0, w=1.6, d=0.8, name="CollabTable")
for i, (cx, cy, yaw) in enumerate(((2.2, 6.15, 0), (3.0, 6.15, 0), (2.2, 7.85, 180), (3.0, 7.85, 180)), 1):
    F.chair(S, cx, cy, math.radians(yaw), color="chair_red" if i % 2 else "chair_green", name="CollabChair_%d" % i)
    S.anchor("SEAT", "meeting", cx, cy, yaw, n=i)
    S.anchor("STATUS", "", 2.6, 7.0, n=16 + i) if i == 1 else None
F.whiteboard(S, 0.2, 9.0, math.radians(90), w=2.4)
S.anchor("STAND", "whiteboard", 1.2, 9.0, 90, n=1)
S.anchor("STAND", "whiteboard", 1.2, 9.9, 90, n=2)

# ---- 南牆：高櫃
for i in range(6):
    F.cabinet(S, 4.9 + 0.9 * i, 0.2 + 0.225, math.radians(180), name="Cabinet_%d" % (i + 1))
S.anchor("POI", "cabinet", 7.6, 1.3, 180, n=1)

# ---- 東側：影印區、茶水、站立會議
F.printer(S, 15.3, 4.5, math.radians(-90))
S.anchor("POI", "printer", 14.4, 4.5, -90, n=1)
F.water_dispenser(S, 15.5, 2.8, math.radians(-90))
S.anchor("POI", "water", 14.7, 2.8, -90, n=1)
F.table(S, 14.0, 9.5, 0, w=1.6, d=0.8, h=1.05, top="desk_white", name="StandingTable")
S.anchor("STAND", "meeting", 13.4, 8.6, 0, n=1)
S.anchor("STAND", "meeting", 14.6, 8.6, 0, n=2)
S.anchor("STAND", "meeting", 14.0, 10.4, 180, n=3)
F.laptop(S, 13.7, 9.5, 0, z=1.05)

# ---- 植栽
for (px, py) in ((0.7, 0.7), (15.3, 0.7), (15.3, 11.3), (0.7, 11.3), (8.0, 6.0)):
    F.plant(S, px, py)

S.finish(HERE)
