"""場景 003：小型討論室＋電話亭（4 人討論桌＋2 座單人電話亭）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

R = math.radians
S = Scene("003", "huddle_booths", "小型討論室／電話亭", "Huddle Room & Phone Booths", "meeting", (6, 4),
          tags=["meeting", "huddle", "phone-booth", "focus", "4-seats", "2-booths"])

# ---- 結構：南北對穿門（x=3），南牆窗
S.add_door("S", 3)
S.add_door("N", 3)
S.add_window("S", 1.3, width=1.6)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})
S.ceiling_panel(1.5, 2.0, power=140)
S.ceiling_panel(3.3, 2.0, w=0.6, d=0.6, power=60)

# ---- 西半：4 人討論桌（短邊朝西牆螢幕）
TX, TY = 1.55, 2.0
F.rug(S, TX, TY, 2.4, 2.4, "rug_blue")
F.table(S, TX, TY, 0, w=1.3, d=0.8, top="wood_light", name="HuddleTable")
n = 0
for dx in (-0.3, 0.35):
    n += 1
    F.chair(S, TX + dx, TY - 0.72, 0, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "huddle", TX + dx, TY - 0.72, 0, n=n)
for dx in (-0.3, 0.35):
    n += 1
    F.chair(S, TX + dx, TY + 0.72, math.pi, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "huddle", TX + dx, TY + 0.72, 180, n=n)
F.laptop(S, TX - 0.3, TY - 0.15, 0, z=0.74)
F.laptop(S, TX + 0.35, TY + 0.15, math.pi, z=0.74)
cb = Piece(S, "ConfSpeaker", TX + 0.2, TY, 0.74, coll="PROPS")
cb.cyl(0, 0, 0.02, 0.09, 0.04, "plastic_black", seg=16)
cb.finish(obstacle=False)

# 西牆：大螢幕＋下方矮櫃（視訊會議）
F.screen_wall(S, 0.2, TY, 1.5, h=0.86, yaw=R(90), z=1.05, name="DisplayScreen")
cam = Piece(S, "VideoBar", 0.24, TY, 1.98, coll="PROPS")
cam.box(0, 0, 0, 0.06, 0.6, 0.07, "plastic_black")
cam.finish(obstacle=False)
F.cabinet(S, 0.425, TY, R(90), w=1.2, d=0.45, h=0.6, color="wood_dark", name="MediaCredenza")
S.anchor("STAND", "screen", 0.95, 3.25, -90, n=1)

# 北牆：白板（西段）；南牆窗下：植栽
F.whiteboard(S, 1.45, 3.8, 0, w=1.6, h=1.0, z=1.0, name="Whiteboard_N")
S.anchor("STAND", "whiteboard", 1.45, 3.25, 0, n=1)
F.plant(S, 2.65, 0.55, h=1.0)

# ---- 東半：兩座單人電話亭（背靠東牆，玻璃門朝西）
BW, BD = 1.3, 1.2
bx = 5.8 - BD / 2
for k, by in enumerate((1.05, 2.85)):
    F.phone_booth(S, bx, by, R(-90), w=BW, d=BD, color=("fabric_teal", "fabric_orange")[k],
                  name="PhoneBooth_%02d" % (k + 1))
    # 亭內凳（人面向東牆桌板）
    F.stool(S, bx + 0.05, by, R(-90), h=0.45, color="fabric_grey", name="BoothStool_%02d" % (k + 1))
    F.laptop(S, bx + 0.26, by, R(-90), z=0.755, name="BoothLaptop_%02d" % (k + 1))
    S.anchor("SEAT", "booth", bx + 0.05, by, -90, n=k + 1)
    S.anchor("POI", "booth_door", bx - BD / 2 - 0.45, by + 0.15, -90, n=k + 1)
    S.anchor("STATUS", "", bx, by, n=2 + k, z=2.45)
    F.status_lamp(S, bx - 0.3, by, z=2.3, name="StatusLamp_%02d" % (2 + k),
                  color=((0.2, 0.9, 0.3), (0.95, 0.25, 0.2))[k])
    # 導航：打通亭門到座位（門在亭正面偏南側之外，寬 0.5）
    S.extra_free.append((bx - BD / 2 - 0.3, by - 0.25, bx + 0.1, by + 0.25))

# 走道東側：吸音板（北牆東段）＋外套掛勾
F.acoustic_panels(S, 3.95, 3.8, 0, cols=2, rows=3, size=0.42, z=0.7, name="AcousticPanels_N")
F.wall_shelf(S, 4.45, 0.2, math.pi, w=0.7, z=1.5, n=1, name="Shelf_S")
S.anchor("POI", "shelf", 4.45, 0.75, 180, n=1)

# ---- 狀態標籤：討論桌上方
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

S.finish(HERE, plan_px_per_m=120)
