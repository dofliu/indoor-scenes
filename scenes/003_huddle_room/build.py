"""場景 003：小型討論室／電話亭（4 人討論桌 + 2 座 1 人電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "huddle_room", "小型討論室／電話亭", "Huddle Room & Phone Booths", "meeting", (6, 4),
          tags=["meeting", "huddle", "phone-booth", "focus", "4-seats"])

# ---- 結構：南門（中央）、西門（拼接用）、東窗
S.add_door("S", 3)
S.add_door("W", 1)
S.add_window("E", 1.6, width=1.2)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.ceiling_panel(1.5, 2.2, power=140)
S.ceiling_panel(3.6, 1.2, power=120)

# ---- 西側：4 人討論桌（長軸南北），北牆壁掛螢幕
TX, TY = 1.5, 2.2
F.rug(S, TX, TY, 2.4, 2.4, "rug_blue")
F.table(S, TX, TY, 0, w=0.8, d=1.4, top="wood_light", name="HuddleTable")
n = 0
for sx, yaw_c, yaw_a in ((-1, -math.pi / 2, -90), (1, math.pi / 2, 90)):
    for dy in (-0.35, 0.35):
        n += 1
        cx, cy = TX + sx * 0.68, TY + dy
        F.chair(S, cx, cy, yaw_c, color="chair_green" if sx < 0 else "chair_seat", name="Chair_%02d" % n)
        S.anchor("SEAT", "huddle", cx, cy, yaw_a, n=n)
F.laptop(S, TX - 0.15, TY - 0.35, math.radians(-90), z=0.74)
F.laptop(S, TX + 0.15, TY + 0.35, math.radians(90), z=0.74)
F.screen_wall(S, TX, 3.8, 1.3, h=0.75, yaw=0, z=1.1, name="WallScreen")
S.anchor("STAND", "screen", TX + 0.85, 3.35, 0, n=1)

# ---- 南牆（門西側）：小白板
F.whiteboard(S, 1.2, 0.2, math.pi, w=1.4, h=1.0, z=1.0, name="Whiteboard_S")
S.anchor("STAND", "whiteboard", 1.2, 0.85, 180, n=1)

# ---- 東北：兩座電話亭（開口朝南）
booths = []
for k, bx in enumerate((3.95, 5.2)):
    sx_, sy_ = F.phone_booth(S, bx, 3.18, 0, w=1.2, d=1.1, name="PhoneBooth_%02d" % (k + 1))
    booths.append((bx, sx_, sy_))
    S.anchor("SEAT", "booth", sx_, sy_, 0, n=k + 1)
    S.anchor("POI", "booth", bx, 2.25, 0, n=k + 1)

# ---- 東南：等候沙發（背靠南牆，門東側）、衣架、植栽
F.sofa(S, 4.75, 0.6, 0, w=1.5, d=0.75, color="fabric_teal", name="WaitSofa")
S.anchor("SEAT", "wait", 4.4, 0.9, 0, n=1)
S.anchor("SEAT", "wait", 5.1, 0.9, 0, n=2)
F.coat_rack(S, 0.5, 3.45)
F.plant(S, 5.55, 2.15)

# ---- 狀態標籤：討論桌上方、各電話亭頂上
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")
for k, (bx, sx_, sy_) in enumerate(booths):
    S.anchor("STATUS", "", bx, 3.18, n=k + 2, z=2.5)
    F.status_lamp(S, bx, 3.18, z=2.38, name="StatusLamp_%02d" % (k + 2))

S.finish(HERE, plan_px_per_m=110)
