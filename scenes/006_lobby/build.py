"""場景 006：大廳接待區（接待櫃台、等候沙發、訪客登記機、閘機）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("006", "lobby", "大廳接待區", "Lobby & Reception", "service", (12, 8),
          tags=["lobby", "reception", "waiting", "turnstile", "entrance"])

# 入口（南牆雙門）、西側內部門、東側閘機後內部門、北側門
for wall, off in (("S", 5), ("S", 7), ("W", 7), ("E", 3), ("E", 5), ("N", 11)):
    S.add_door(wall, off)
S.add_window("S", 2.0, width=2.0)
S.add_window("S", 10.0, width=2.0)
S.add_window("W", 3.0, width=2.4)
S.add_window("N", 2.0, width=1.6)
S.build_shell(floor="floor_concrete", accent={"N": "wall_accent"})
S.light_grid(4, 3, margin=1.6, power=70)

NY = S.D - WALL_T  # 7.8

# ---- 接待櫃台（北側中央）＋背景牆
F.feature_wall(S, 6.0, NY, 0, w=4.4)
F.reception_desk(S, 6.0, 6.45, 0, w=4.0)
for n, x in enumerate((5.1, 6.9), 1):
    F.chair(S, x, 7.2, math.radians(180), color="chair_seat", name="StaffChair_%d" % n)
    F.monitor(S, x, 6.65, math.radians(180), name="StaffMonitor_%d" % n)
    F.keyboard(S, x, 6.35 + 0.0, math.radians(180), name="StaffKeyboard_%d" % n)
    S.anchor("SEAT", "reception", x, 7.2, 180, n=n)
S.anchor("POI", "reception", 6.0, 5.4, 0, n=1)
S.anchor("STAND", "visitor", 4.9, 5.3, 0, n=1)
S.anchor("STAND", "visitor", 7.1, 5.3, 0, n=2)
S.anchor("STATUS", "", 6.0, 6.45, n=1)
F.plant(S, 3.2, 7.2)
F.plant(S, 8.8, 7.2)

# ---- 等候區（西側）：兩張對坐沙發＋茶几＋扶手椅
F.rug(S, 2.6, 4.0, 3.8, 3.6, "rug_blue")
F.sofa(S, 2.5, 2.7, 0, w=2.0, color="fabric_grey", name="WaitSofa_1", seat_clear=True)
F.sofa(S, 2.5, 5.3, math.radians(180), w=2.0, color="fabric_grey", name="WaitSofa_2", seat_clear=True)
F.coffee_table(S, 2.5, 4.0, 0, w=1.2, d=0.6)
F.armchair(S, 4.35, 4.0, math.radians(90), color="fabric_orange", name="WaitArmchair")
for n, (x, y, yaw) in enumerate(((1.9, 2.7, 0), (3.1, 2.7, 0), (1.9, 5.3, 180), (3.1, 5.3, 180), (4.35, 4.0, 90)), 1):
    S.anchor("SEAT", "waiting", x, y, yaw, n=n)
S.anchor("STATUS", "", 2.5, 4.0, n=2)
F.plant(S, 0.7, 0.8)
F.plant(S, 0.7, 5.6)

# ---- 入口內側：訪客登記機、長凳
F.info_kiosk(S, 9.2, 1.5, 0, name="Kiosk_1")
S.anchor("POI", "kiosk", 9.2, 0.9, 0, n=1)
F.bench(S, 4.8, 0.6, math.radians(0), w=1.6, name="EntryBench")
S.anchor("SEAT", "bench", 4.8, 0.6, 0, n=1)
S.anchor("STAND", "entrance", 5.0, 1.3, 0, n=1)
S.anchor("STAND", "entrance", 7.0, 1.3, 0, n=2)

# ---- 東側閘機線（4 柱形成 3 條通道，通道沿 X 向通往東側內部門）
for i, y in enumerate((2.2, 3.5, 4.8, 6.1), 1):
    F.turnstile(S, 9.6, y, math.radians(90), name="Turnstile_%d" % i)
for n, y in enumerate((2.85, 4.15, 5.45), 1):
    S.anchor("POI", "gate", 9.0, y, -90, n=n)
S.anchor("STATUS", "", 9.6, 4.15, n=3)
F.plant(S, 11.3, 7.2)
F.plant(S, 11.3, 0.8)

S.finish(HERE)
