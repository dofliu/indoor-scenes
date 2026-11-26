"""場景 003：小型討論室／電話亭（4 人討論區 + 2 個單人電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "huddle_booths", "小型討論室／電話亭", "Huddle Room & Booths", "meeting", (8, 4),
          tags=["meeting", "huddle", "phone-booth", "4-seats", "2-booths"])

# ---- 結構：門（南 3、南 7、東 1）
S.add_door("S", 3)
S.add_door("S", 7)
S.add_door("E", 1)
S.add_window("W", 3, width=1.2)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.ceiling_panel(2.2, 2.2, power=150)
S.ceiling_panel(6.2, 1.2, power=120)

# ---- 玻璃隔間：分隔討論區（西）與電話亭區（東），南端留 1.4 m 通道
F.glass_partition(S, 4.4, 2.7, math.pi / 2, w=2.2, name="GlassPartition")

# ================= 西側：4 人討論區 =================
TX, TY = 2.2, 2.25
F.rug(S, TX, TY, 3.0, 2.8, "rug_blue")
F.round_table(S, TX, TY, r=0.55, h=0.74, name="HuddleTable")
seats = ((0, -0.95, 0), (0.95, 0, 90), (0, 0.95, 180), (-0.95, 0, -90))  # 南、東、北、西
for i, (dx, dy, yw) in enumerate(seats, 1):
    F.chair(S, TX + dx, TY + dy, math.radians(yw), color="chair_green" if i % 2 else "chair_seat",
            name="HuddleChair_%02d" % i)
    S.anchor("SEAT", "huddle", TX + dx, TY + dy, yw, n=i)
F.laptop(S, TX - 0.05, TY - 0.25, 0, z=0.74)
F.laptop(S, TX + 0.25, TY + 0.05, math.radians(90), z=0.74, name="Laptop_2")

# 北牆：共享螢幕（西段）＋白板（東段）
F.screen_wall(S, 1.25, 3.8, 1.3, h=0.75, yaw=0, z=1.15, name="ShareScreen")
S.anchor("STAND", "screen", 0.8, 3.2, 180, n=1)
F.whiteboard(S, 3.2, 3.8, 0, w=1.6, name="Whiteboard_N")
S.anchor("STAND", "whiteboard", 3.7, 3.2, 180, n=1)

# 南牆低櫃、角落植栽
F.cabinet(S, 1.2, 0.2 + 0.225, math.pi, h=0.9, name="Credenza")
S.anchor("POI", "credenza", 1.2, 1.2, 180, n=1)
F.plant(S, 0.6, 1.25)
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

# ================= 東側：2 個單人電話亭（背靠北牆，開口朝南） =================
for k, cx in enumerate((5.5, 7.0), 1):
    F.phone_booth(S, cx, 3.1, 0, name="PhoneBooth_%02d" % k)
    S.anchor("SEAT", "booth", cx, 3.0, 0, n=k)
    S.anchor("STATUS", "", cx, 2.5, n=k + 1)
    F.status_lamp(S, cx, 2.5, z=2.2, name="StatusLamp_%02d" % (k + 1), color=(0.95, 0.6, 0.1) if k == 2 else (0.2, 0.9, 0.3))

# 預約面板（東牆，門的北側）
F.wall_panel(S, 7.8, 2.0, math.radians(-90), name="BookingPanel")
S.anchor("POI", "booking", 7.2, 2.0, -90, n=1)

S.finish(HERE, plan_px_per_m=100)
