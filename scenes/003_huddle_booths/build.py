"""場景 003：小型討論室／電話亭（4 人討論區＋2 座單人電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "huddle_booths", "小型討論室／電話亭", "Huddle Room & Phone Booths", "meeting", (8, 4),
          tags=["meeting", "huddle", "phone-booth", "4-seats", "focus"])

# ---- 結構：門（南牆 x=5、東牆 y=1）、窗（南牆西段）
S.add_door("S", 5)
S.add_door("E", 1)
S.add_window("S", 2.2, width=1.8)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.ceiling_panel(2.4, 2.0, power=110)
S.ceiling_panel(5.6, 1.2, power=70)
S.ceiling_panel(7.0, 1.2, w=0.6, power=40)

# ---- 西側：4 人討論桌（面向西牆大螢幕）
TX, TY = 2.5, 2.0
F.rug(S, TX - 0.2, TY, 3.2, 2.4, "rug_blue")
F.table(S, TX, TY, 0, w=1.4, d=0.8, top="wood_light", name="HuddleTable")
n = 0
for dx in (-0.35, 0.35):
    n += 1  # 南側，面向北
    F.chair(S, TX + dx, TY - 0.68, 0, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "huddle", TX + dx, TY - 0.68, 0, n=n)
for dx in (-0.35, 0.35):
    n += 1  # 北側，面向南
    F.chair(S, TX + dx, TY + 0.68, math.pi, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "huddle", TX + dx, TY + 0.68, 180, n=n)
F.laptop(S, TX - 0.35, TY - 0.15, 0, z=0.74)
F.laptop(S, TX + 0.35, TY + 0.15, math.pi, z=0.74)
cb = Piece(S, "ConfSpeaker", TX, TY, 0.74, coll="PROPS")
cb.cyl(0, 0, 0.02, 0.09, 0.04, "plastic_black", seg=16)
cb.finish(obstacle=False)

# 西牆大螢幕（面向東）＋簡報站位
F.screen_wall(S, 0.2, TY, 1.6, h=0.95, yaw=math.radians(90), z=1.0, name="HuddleScreen")
cab = F.cabinet(S, 0.2 + 0.2, TY, math.radians(-90), w=1.6, d=0.4, h=0.6, name="MediaConsole")
S.anchor("STAND", "screen", 0.95, 0.95, -90, n=1)

# 北牆白板
F.whiteboard(S, 2.6, 3.8, 0, w=1.8, h=1.1, name="Whiteboard_N")
S.anchor("STAND", "whiteboard", 1.4, 3.25, 0, n=1)

# 南牆預約平板
tb = Piece(S, "BookingPanel", 3.75, 0.2, 1.25, coll="PROPS")
tb.box(0, 0.01, 0, 0.26, 0.02, 0.18, "plastic_black")
tb.box(0, 0.021, 0, 0.23, 0.002, 0.15, mat("screen_glow", (0.05, 0.15, 0.3), emit=(0.08, 0.3, 0.6)))
tb.finish(obstacle=False)
S.anchor("POI", "booking", 3.75, 0.85, 180, n=1)

# 討論區狀態標籤
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

# ---- 東側：兩座電話亭（背貼北牆，入口朝南）
for k, bx in enumerate((4.9, 6.55)):
    b = F.phone_booth(S, bx, 3.8 - 0.7, 0, name="PhoneBooth_%02d" % (k + 1))
    S.anchor("SEAT", "booth", b["seat"][0], b["seat"][1], 0, n=k + 1)
    S.anchor("STATUS", "", b["status"][0], b["status"][1], n=k + 2, z=b["status"][2])
    F.status_lamp(S, b["status"][0], b["status"][1], z=b["status"][2], name="StatusLamp_%02d" % (k + 2))

# ---- 東南：等候長凳＋植栽
bench = Piece(S, "WaitingBench", 6.6, 0.2 + 0.23)
bench.box(0, 0, 0.21, 1.2, 0.42, 0.06, "wood_light")
for sx in (-1, 1):
    bench.box(sx * 0.52, 0, 0.09, 0.06, 0.38, 0.18, "metal_dark")
bench.finish(footprint=(1.2, 0.42))
S.anchor("SEAT", "wait", 6.3, 0.65, 0, n=1)
S.anchor("SEAT", "wait", 6.9, 0.65, 0, n=2)
F.plant(S, 4.0, 3.5, h=1.0)

S.finish(HERE, plan_px_per_m=90)
