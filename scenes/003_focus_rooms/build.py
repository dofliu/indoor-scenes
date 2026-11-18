"""場景 003：小型討論室＋電話亭（4 人討論區＋2 座單人電話亭）。執行：python3 build.py"""
import sys, os, math
import bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "focus_rooms", "小型討論室／電話亭", "Focus Room & Phone Booths", "meeting", (6, 4),
          tags=["meeting", "phone-booth", "focus", "small", "4-seats"])

# ---- 結構：南門（中央）、西門（拼接走廊用）、西窗
S.add_door("S", 3)
S.add_door("W", 1)
S.add_window("W", 3, width=1.2)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.ceiling_panel(1.9, 2.1, power=150)
S.ceiling_panel(3.6, 1.2, power=90)

# ---- 西側：4 人圓桌討論區
TX, TY = 1.9, 2.1
F.rug(S, TX, TY, 2.6, 2.4, "rug_blue")
F.round_table(S, TX, TY, r=0.55, h=0.74, top="wood_light", name="RoundTable")
seats = [  # (dx, dy, chair_yaw, anchor_yaw, color)
    (0, -0.85, 0, 0, "chair_seat"),
    (0, 0.85, math.pi, 180, "chair_seat"),
    (-0.85, 0, -math.pi / 2, -90, "fabric_orange"),
    (0.85, 0, math.pi / 2, 90, "fabric_orange"),
]
for n, (dx, dy, cy, ay, col) in enumerate(seats, 1):
    F.chair(S, TX + dx, TY + dy, cy, color=col, name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", TX + dx, TY + dy, ay, n=n)
F.laptop(S, TX - 0.12, TY - 0.22, 0, z=0.74)
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

# 北牆：壁掛螢幕（討論區）＋小白板（站立）
F.screen_wall(S, TX, 3.8, 1.4, h=0.8, yaw=0, z=1.1, name="WallScreen")
F.whiteboard(S, 3.6, 3.8, 0, w=1.2, h=1.0, z=1.0, name="Whiteboard_N")
S.anchor("STAND", "whiteboard", 3.6, 3.2, 0, n=1)

# 南牆：門旁預約平板
F.wall_tablet(S, 2.15, 0.2, math.pi, name="BookingTablet")
S.anchor("POI", "booking", 2.15, 0.75, 180, n=1)

# ---- 東側：兩座單人電話亭（開口朝西）
for k, by in enumerate((1.0, 3.0), 1):
    F.phone_booth(S, 5.2, by, yaw=-math.pi / 2, color=("fabric_teal" if k == 1 else "fabric_grey"),
                  name="PhoneBooth_%02d" % k)
    F.chair(S, 4.95, by, -math.pi / 2, color="chair_green", name="BoothChair_%02d" % k)
    S.anchor("SEAT", "booth", 4.95, by, -90, n=k)
    F.laptop(S, 5.5, by, math.pi / 2, z=0.755, name="BoothLaptop_%02d" % k)
    S.anchor("STATUS", "", 5.2, by, n=k + 1, z=2.35)
    F.status_lamp(S, 5.2, by, z=2.26, name="StatusLamp_%02d" % (k + 1),
                  color=(0.2, 0.9, 0.3) if k == 1 else (0.95, 0.25, 0.15))
    ld = bpy.data.lights.new("BoothLight_%02d" % k, "AREA")
    ld.energy, ld.size = 25, 0.5
    lo = bpy.data.objects.new("BoothLight_%02d" % k, ld)
    lo.location = (5.2, by, 2.0)
    S.coll["LIGHTS"].objects.link(lo)

# 兩亭之間：邊桌＋植栽
F.side_table(S, 5.0, 2.0, r=0.22)
F.plant(S, 5.5, 2.0, h=1.0)
F.plant(S, 0.55, 3.45, h=1.0)

S.finish(HERE, plan_px_per_m=110)
