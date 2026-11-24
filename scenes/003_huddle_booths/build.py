"""場景 003：小型討論室＋電話亭（4 人討論區＋2 座單人電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "huddle_booths", "小型討論室／電話亭", "Huddle Room & Phone Booths", "meeting", (6, 4),
          tags=["meeting", "huddle", "phone-booth", "focus", "4-seats"])

# ---- 結構：南門（主入口）、西門（可接走廊）；西窗
S.add_door("S", 3)
S.add_door("W", 1)
S.add_window("W", 3, width=1.2)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.ceiling_panel(1.8, 2.2, power=140)
S.ceiling_panel(3.4, 1.2, w=0.6, d=0.6, power=60)

# ---- 討論區：圓桌＋4 椅
TX, TY, TR = 1.8, 2.25, 0.55
F.rug(S, TX, TY, 2.6, 2.4, "rug_blue")
F.round_table(S, TX, TY, r=TR, h=0.74, top="wood_light", name="HuddleTable")
seats = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # 南、東、北、西
cols = ["chair_seat", "chair_green", "chair_seat", "chair_green"]
for n, ((ux, uy), c) in enumerate(zip(seats, cols), start=1):
    cx, cy = TX + ux * (TR + 0.38), TY + uy * (TR + 0.38)
    yaw = math.atan2(ux, -uy)  # 椅子面向桌心
    F.chair(S, cx, cy, yaw, color=c, name="Chair_%02d" % n)
    S.anchor("SEAT", "huddle", cx, cy, math.degrees(yaw), n=n)
F.laptop(S, TX - 0.12, TY - 0.2, 0, z=0.74)
F.laptop(S, TX + 0.2, TY + 0.15, math.pi * 0.8, z=0.74)

# ---- 北牆：壁掛螢幕、白板、吸音板
F.screen_wall(S, TX, 3.8, 1.4, h=0.8, yaw=0, z=1.05, name="WallDisplay")
S.anchor("STAND", "display", 0.95, 3.15, 180, n=1)
F.whiteboard(S, 3.25, 3.8, 0, w=1.0, h=1.0, z=1.0, name="Whiteboard_N")
S.anchor("STAND", "whiteboard", 3.25, 3.2, 0, n=1)
F.acoustic_panels(S, 0.62, 3.8, 0, n=2, pw=0.3, ph=0.7, z=1.65)

# ---- 東側：2 座電話亭（門朝西，背貼東牆）
BX = 6 - 0.2 - 0.7 - 0.02
for k, by in enumerate((1.1, 2.9), start=1):
    F.phone_booth(S, BX, by, -math.pi / 2, color=("fabric_teal" if k == 1 else "fabric_orange"), name="PhoneBooth_%02d" % k)
    # 亭內：凳子面向東（桌板在東側背牆）
    sy = by - 0.3  # 門洞在亭的南半部（世界 y = by-0.64 … by+0.05）
    F.stool(S, BX + 0.05, sy, color=("fabric_orange" if k == 1 else "fabric_teal"), name="Stool_%02d" % k)
    F.laptop(S, BX + 0.5, sy, -math.pi / 2, z=0.755)
    S.anchor("SEAT", "booth", BX + 0.05, sy, -90, n=k)
    S.anchor("POI", "booth_door", BX - 1.05, sy, -90, n=k)
    S.add_nav_passage(BX - 1.1, by - 0.55, BX + 0.15, by - 0.05)  # 門口→座位通道
    S.anchor("STATUS", "", BX - 0.4, by, n=k + 1, z=2.45)
    F.status_lamp(S, BX - 0.55, by + 0.35, z=2.36, name="StatusLamp_%02d" % (k + 1),
                  color=(0.95, 0.25, 0.2) if k == 1 else (0.2, 0.9, 0.3))

# ---- 桌心狀態標籤（討論區）
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

# ---- 角落：植栽、飲水
F.plant(S, 0.55, 3.45)
F.water_dispenser(S, 3.8, 0.42, math.pi)
S.anchor("POI", "water", 3.8, 1.0, 180, n=1)

S.finish(HERE, plan_px_per_m=90)
