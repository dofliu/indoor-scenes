"""場景 003：小型討論室／電話亭（4 人討論桌＋2 個單人電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "huddle_phone_booths", "小型討論室／電話亭", "Huddle Room & Phone Booths", "meeting", (6, 4),
          tags=["meeting", "huddle", "phone-booth", "focus", "4-seats", "2-booths"])

# ---- 結構：南北各一門（可當穿越式專注區），南牆開窗
S.add_door("S", 3)
S.add_door("N", 3)
S.add_window("S", 1.25, width=1.5)
S.build_shell(floor="floor_carpet", accent={"W": "wall_accent"})
S.light_grid(2, 1, margin=1.2, power=55)

# ---- 西側：4 人討論桌（桌端靠西牆螢幕）
TX, TY = 1.15, 2.0
F.rug(S, 1.45, TY, 2.3, 2.7, "rug_blue")
F.table(S, TX, TY, 0, w=1.6, d=0.9, top="wood_light", name="HuddleTable")
n = 0
for dx in (-0.35, 0.35):
    n += 1  # 南側，面向北
    F.chair(S, TX + dx, TY - 0.8, 0, color="chair_green", name="Chair_%02d" % n)
    S.anchor("SEAT", "huddle", TX + dx, TY - 0.8, 0, n=n)
for dx in (-0.35, 0.35):
    n += 1  # 北側，面向南
    F.chair(S, TX + dx, TY + 0.8, math.pi, color="chair_green", name="Chair_%02d" % n)
    S.anchor("SEAT", "huddle", TX + dx, TY + 0.8, 180, n=n)
F.laptop(S, TX + 0.35, TY - 0.2, 0, z=0.74)
F.laptop(S, TX - 0.35, TY + 0.2, math.pi, z=0.74, name="Laptop_2")
# 桌面會議麥克風
mic = Piece(S, "ConferenceMic", TX + 0.05, TY, 0.74, coll="PROPS")
mic.cyl(0, 0, 0.015, 0.09, 0.03, "plastic_black", seg=16)
mic.cyl(0, 0, 0.032, 0.03, 0.004, "panel_blue", seg=12)
mic.finish(obstacle=False)
# 西牆螢幕、北牆白板
F.screen_wall(S, 0.2, TY, 1.3, h=0.75, yaw=math.radians(90), z=1.15, name="HuddleDisplay")
F.whiteboard(S, 1.3, 3.8, 0, w=1.8, name="Whiteboard_N")
S.anchor("STAND", "whiteboard", 1.3, 3.35, 0, n=1)
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

# ---- 東側：2 個單人電話亭（開口朝西）
for i, by in enumerate((0.85, 3.15)):
    b = F.phone_booth(S, 5.15, by, yaw=math.radians(-90), w=1.2, d=1.3,
                      color=("fabric_teal", "panel_blue")[i], name="PhoneBooth_%02d" % (i + 1))
    S.anchor("SEAT", "booth", b["seat"][0], b["seat"][1], b["face_yaw_deg"], n=i + 1)
    S.anchor("STATUS", "", b["status"][0], b["status"][1], n=i + 2)

# ---- 兩亭之間：邊桌（水壺、訂位平板）與植栽
F.console(S, 5.6, 2.0, math.radians(-90), w=0.8, name="Console")
pr = Piece(S, "ConsoleProps", 5.6, 2.0, 0.85, coll="PROPS")
pr.cyl(0, 0.22, 0.11, 0.05, 0.22, mat("water_blue", (0.5, 0.75, 0.95), rough=0.1, alpha=0.6), seg=14)
for k in range(2):
    pr.cyl(0.02, 0.05 - 0.1 * k, 0.045, 0.035, 0.09, "plastic_white", seg=12)
pr.box(-0.02, -0.25, 0.08, 0.02, 0.2, 0.14, "plastic_black", rz=0)
pr.finish(obstacle=False)
S.anchor("POI", "console", 4.9, 2.0, -90, n=1)
F.plant(S, 0.5, 0.5, h=1.0)
F.plant(S, 2.15, 0.5, h=0.8, name="Plant_2")

S.finish(HERE, plan_px_per_m=150)
