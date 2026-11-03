"""場景 003：小型討論室／電話亭（4 人討論桌＋1 人電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("003", "huddle_room", "小型討論室／電話亭", "Huddle Room & Phone Booth", "meeting", (4, 4),
          tags=["meeting", "huddle", "phone-booth", "4-seats"])

# ---- 結構
S.add_door("W", 1)
S.add_door("N", 1)
S.build_shell(floor="floor_wood", accent={"E": "wall_accent"})
S.light_grid(2, 2, margin=1.0, w=0.6, d=0.6, power=25)

# ---- 討論桌（1.4×0.8）與 4 張椅
F.rug(S, 2.0, 2.2, 2.2, 1.8, "rug_blue")
F.table(S, 2.0, 2.2, 0, w=1.4, d=0.8, h=0.74, top="desk_white", name="HuddleTable")
n = 0
for sy, yaw in ((-1, 0), (1, 180)):
    for x in (1.65, 2.35):
        n += 1
        y = 2.2 + sy * 0.7
        F.conference_chair(S, x, y, math.radians(yaw), color=("chair_green", "chair_seat")[n % 2], name="Chair_%02d" % n)
        S.anchor("SEAT", "meeting", x, y, yaw, n=n)
F.laptop(S, 1.65, 2.05, 0, z=0.74)
F.speakerphone(S, 2.35, 2.2, z=0.74)
S.anchor("STATUS", "", 2.0, 2.2, n=1)

# ---- 東牆：壁掛顯示器；北牆：小白板
F.screen_wall(S, S.W - 0.2, 2.4, w=1.4, h=0.8, yaw=math.radians(-90), z=1.0)
S.anchor("POI", "screen", 3.2, 2.4, -90, n=1)
F.whiteboard(S, 2.9, S.D - 0.2, 0, w=1.2, h=0.9, z=1.0)
S.anchor("STAND", "whiteboard", 2.9, 3.0, 0, n=1)

# ---- 東南角：電話亭（南、東為牆；北與西側玻璃，西側留 0.8 m 開口）
F.glass_panel(S, 3.1, 1.6, 1.4, yaw=0, name="BoothGlass_N")
F.glass_panel(S, 2.4, 1.3, 0.6, yaw=math.radians(90), name="BoothGlass_W")
F.table(S, 3.6, 0.9, math.radians(90), w=0.9, d=0.35, h=1.0, top="wood_light", name="BoothShelf")
F.stool(S, 3.0, 0.9)
F.laptop(S, 3.6, 0.9, math.radians(-90), z=1.0)
S.anchor("SEAT", "phone", 3.0, 0.9, -90, n=1)
S.anchor("STATUS", "", 3.0, 0.9, n=2)
F.plant(S, 0.6, 0.6)

S.finish(HERE)
