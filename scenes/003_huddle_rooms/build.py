"""場景 003：小型討論室與電話亭（4 人討論室、2 人雙人室、3 人沙發洽談室、2 座電話亭）。
執行：python3 build.py（需 pip install bpy）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

R = math.radians
S = Scene("003", "huddle_rooms", "小型討論室與電話亭", "Huddle Rooms & Phone Booths", "meeting", (8, 6),
          tags=["meeting", "huddle", "phone-booth", "focus", "2-4-seats"])

# ---- 外殼：南側為共用前廊（可東西穿越），北側三間小房
S.add_door("S", 3)
S.add_door("W", 1)
S.add_door("E", 1)
S.add_window("W", 4.3, width=1.4)
S.add_window("N", 4.55, width=1.2)
S.add_window("E", 4.3, width=1.4)
S.build_shell(floor="floor_carpet")

PY = 2.65                      # 玻璃隔間中心線
XA, XB = 3.45, 5.65            # 兩道實牆隔間中心線
GA, GB, GC = (2.3, 3.2), (4.45, 5.35), (5.85, 6.75)   # 三個房門洞
F.partition(S, 0.2, PY, 7.8, PY, gaps=[GA, GB, GC], glass=True, name="GlassPartition",
            leaves=[(GA[1], 1), (GB[1], 1), (GC[0], 1)])
F.partition(S, XA, PY + 0.05, XA, 5.8, glass=False, color="wall_accent", name="Divider_A")
F.partition(S, XB, PY + 0.05, XB, 5.8, glass=False, color="wall_accent", name="Divider_B")

for (lx, ly) in ((1.7, 4.3), (4.55, 4.3), (6.75, 4.3), (1.6, 1.5), (6.9, 1.6)):
    S.ceiling_panel(lx, ly, 1.0, 0.6, power=60)

# ================= A：4 人討論室 =================
AX, AY = 1.6, 4.3
F.rug(S, AX, AY, 2.4, 2.4, "rug_blue", name="Rug_A")
F.round_table(S, AX, AY, r=0.5, h=0.74, name="HuddleTable")
for k, (dx, dy, yw) in enumerate(((0, -0.85, 0), (0.85, 0, 90), (0, 0.85, 180), (-0.85, 0, -90)), 1):
    F.chair(S, AX + dx, AY + dy, R(yw), color="chair_green", name="ChairA_%02d" % k)
    S.anchor("SEAT", "huddle", AX + dx, AY + dy, yw, n=k, status=1)
F.laptop(S, AX - 0.05, AY - 0.2, 0, z=0.74, name="Laptop_A")
F.screen_wall(S, AX, 5.8, 1.4, h=0.8, yaw=0, z=1.15, name="Display_A")
F.whiteboard(S, XA - 0.05, 4.5, R(-90), w=1.6, h=1.0, z=0.95, name="Whiteboard_A")
S.anchor("STAND", "whiteboard", 2.75, 4.5, -90, n=1, status=1)
F.plant(S, 2.95, 5.4, h=0.9, name="Plant_A")

# ================= B：2 人雙人室（靠牆桌＋壁掛螢幕）=================
F.desk(S, 3.8, 4.3, R(90), w=1.4, d=0.6, top="desk_white", name="DuoDesk")
F.screen_wall(S, XA + 0.05, 4.3, 1.0, h=0.6, yaw=R(90), z=1.2, name="Display_B")
for k, yy in enumerate((3.95, 4.65), 1):
    F.chair(S, 4.5, yy, R(90), color="chair_seat", name="ChairB_%02d" % k)
    S.anchor("SEAT", "duo", 4.5, yy, 90, n=k, status=2)
F.laptop(S, 3.85, 3.95, R(90), z=0.74, name="Laptop_B")

# ================= C：3 人沙發洽談室 =================
F.rug(S, 6.75, 4.4, 1.8, 2.0, "rug", name="Rug_C")
F.sofa(S, 6.75, 5.38, R(180), w=1.6, d=0.8, color="fabric_grey", name="Sofa_C", fp=(1.6, 0.4, 0, -0.2))
S.anchor("SEAT", "lounge", 6.4, 5.3, 180, n=1, status=3)
S.anchor("SEAT", "lounge", 7.1, 5.3, 180, n=2, status=3)
F.armchair(S, 7.3, 3.75, R(60), color="fabric_orange", name="Armchair_C")
S.anchor("SEAT", "lounge", 7.3, 3.75, 60, n=3, status=3)
F.round_table(S, 6.75, 4.35, r=0.26, h=0.42, top="wood_dark", name="CoffeeTable_C")

# ================= 前廊：電話亭 ×2、等候長凳、預約面板 =================
for k, bx in enumerate((4.3, 5.5), 1):
    F.phone_booth(S, bx, 0.2 + 0.55, R(180), name="PhoneBooth_%02d" % k)
    S.anchor("SEAT", "phone", bx - 0.05, 0.7, 180, n=k, status=3 + k)
F.bench(S, 6.8, 0.2 + 0.25, 0, w=1.2, name="WaitBench", fp=(1.2, 0.3, 0, -0.075))
S.anchor("SEAT", "wait", 6.5, 0.5, 0, n=1)
S.anchor("SEAT", "wait", 7.1, 0.5, 0, n=2)
F.plant(S, 0.65, 2.1, name="Plant_Lobby")

# 門旁預約面板（POI）與門楣使用中指示燈（STATUS）
for k, (px, g) in enumerate(((2.1, GA), (4.25, GB), (6.95, GC)), 1):
    F.wall_tablet(S, px, PY - 0.05, 0, name="BookingPanel_%02d" % k)
    S.anchor("POI", "booking", px, 2.1, 0, n=k)
    gx = (g[0] + g[1]) / 2
    F.door_sign_lamp(S, gx, PY - 0.05, 0, z=2.42, name="DoorLamp_%02d" % k)
    S.anchor("STATUS", "", gx, PY - 0.1, n=k, z=2.42)
# 電話亭頂部狀態燈
for k, bx in enumerate((4.3, 5.5), 4):
    F.status_lamp(S, bx, 1.2, z=2.37, name="StatusLamp_%02d" % k)
    S.anchor("STATUS", "", bx, 1.2, n=k, z=2.4)

# 小隔間多、牆面近：降低曝光避免預覽過曝
S.scene.view_settings.exposure = -1.1
S.finish(HERE)
