"""場景 004：茶水間／咖啡吧（流理台、咖啡機、冰箱、販賣機、吧台與小圓桌）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("004", "pantry", "茶水間／咖啡吧", "Pantry & Coffee Bar", "social", (8, 6),
          tags=["social", "pantry", "coffee", "break"])

# ---- 結構
S.add_door("S", 5)
S.add_door("W", 3)
S.add_door("E", 3)
S.add_window("E", 5, width=1.6)
S.add_window("S", 1.5, width=1.6)
S.build_shell(floor="floor_wood", accent={"N": "wall_accent"})
S.light_grid(3, 2, margin=1.6, power=60)

NY = S.D - WALL_T  # 北牆內側 y = 5.8
cy = NY - 0.3      # 流理台中心 y（深 0.6）

# ---- 北牆：冰箱 → 流理台（4 段，含水槽、咖啡機、微波爐）→ 販賣機
F.fridge(S, 1.0, NY - 0.35, 0)
S.anchor("POI", "fridge", 1.0, 4.9, 0, n=1)
xs = [2.2, 3.4, 4.6, 5.8]
for i, x in enumerate(xs, 1):
    F.kitchen_counter(S, x, cy, 0, w=1.2, name="Counter_%d" % i)
F.sink(S, 2.2, cy, 0)
F.coffee_machine(S, 3.6, cy, 0)
F.microwave(S, 5.6, cy, 0)
F.vending_machine(S, 7.0, NY - 0.4, 0)
S.anchor("POI", "sink", 2.2, 4.8, 0, n=1)
S.anchor("POI", "coffee", 3.6, 4.8, 0, n=1)
S.anchor("POI", "coffee", 4.2, 4.8, 0, n=2)
S.anchor("POI", "microwave", 5.6, 4.8, 0, n=1)
S.anchor("POI", "vending", 7.0, 4.8, 0, n=1)

# ---- 中央吧台（高桌）＋6 張吧凳
BX, BY = 5.0, 2.6
F.rug(S, BX, BY, 3.4, 2.2, "rug")
F.table(S, BX, BY, 0, w=2.4, d=0.7, h=1.05, top="wood_light", name="BarTable")
n = 0
for sy, yaw in ((-1, 0), (1, 180)):
    for dx in (-0.8, 0.0, 0.8):
        n += 1
        y = BY + sy * 0.65
        F.stool(S, BX + dx, y, h=0.75, color=("fabric_orange", "fabric_teal")[n % 2], name="BarStool_%02d" % n)
        S.anchor("SEAT", "bar", BX + dx, y, yaw, n=n)
S.anchor("STATUS", "", BX, BY, n=1)

# ---- 西側：兩張小圓桌＋4 張椅（休憩聊天）
n = 0
for k, ty in enumerate((1.6, 4.0), 1):
    tx = 1.9
    F.round_table(S, tx, ty, r=0.5, h=0.74, top="wood_light", name="CafeTable_%d" % k)
    for ox, oy, yaw in ((-0.75, 0.0, -90), (0.75, 0.0, 90)):
        n += 1
        F.chair(S, tx + ox, ty + oy, math.radians(yaw), color=("chair_green", "chair_red", "chair_seat", "fabric_teal")[n % 4], name="CafeChair_%02d" % n)
        S.anchor("SEAT", "cafe", tx + ox, ty + oy, yaw, n=n)
S.anchor("STATUS", "", 1.9, 2.8, n=2)

# ---- 植栽
F.plant(S, 0.7, 0.8)
F.plant(S, 7.3, 0.8)
F.plant(S, 7.3, 4.0)

S.finish(HERE)
