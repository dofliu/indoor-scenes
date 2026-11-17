"""場景 003：小型討論室／電話亭（4 人討論室＋2 座單人電話亭＋雙人沙發角）。執行：python3 build.py
配置（6×6 m）：南側 1.6 m 為東西向通道（S/E/W 三門可串接走廊），北側左為玻璃隔間討論室，右為電話亭與休憩角。"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
from scenelib import Piece
import furniture as F

S = Scene("003", "focus_rooms", "小型討論室／電話亭", "Focus Rooms & Phone Booths", "meeting", (6, 6),
          tags=["meeting", "phone-booth", "small-room", "focus", "4-seats", "pass-through"])

# ---- 結構：門（S 中央、E/W 通道兩端）、窗
S.add_door("S", 3)
S.add_door("E", 1)
S.add_door("W", 1)
S.add_window("W", 4, width=1.6)
S.build_shell(floor="floor_carpet", accent={"N": "wall_accent"})

PY = 2.0   # 隔間南緣
PX = 3.6   # 討論室東緣
# ---- 玻璃隔間：討論室南面（含門口）與東面
F.glass_partition(S, 0.2, PY, PX, PY, gap=(2.45, 3.35), name="Partition_S")
F.glass_partition(S, PX, PY, PX, 5.8, name="Partition_E")
F.wall_display(S, 2.25, PY - 0.03, math.pi, name="BookingPanel")  # 掛在隔間外側（面向通道）
S.anchor("POI", "booking", 2.1, 1.35, 0, n=1)

# ---- 討論室：4 人桌（長軸南北）、壁掛螢幕、吸音板
TX, TY = 1.6, 3.95
F.rug(S, TX, TY, 2.4, 2.6, "rug_blue")
F.table(S, TX, TY, math.pi / 2, w=1.4, d=0.8, top="wood_light", name="FocusTable")
n = 0
for dy in (-0.35, 0.35):
    n += 1
    F.chair(S, TX - 0.85, TY + dy, -math.pi / 2, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", TX - 0.85, TY + dy, -90, n=n)
for dy in (-0.35, 0.35):
    n += 1
    F.chair(S, TX + 0.85, TY + dy, math.pi / 2, color="chair_seat", name="Chair_%02d" % n)
    S.anchor("SEAT", "meeting", TX + 0.85, TY + dy, 90, n=n)
F.laptop(S, TX - 0.2, TY - 0.3, -math.pi / 2, z=0.74)
F.laptop(S, TX + 0.2, TY + 0.3, math.pi / 2, z=0.74)
F.screen_wall(S, TX, 5.8, 1.5, h=0.85, yaw=0, z=1.0, name="FocusScreen")
S.anchor("STAND", "screen", 2.75, 5.2, 180, n=1)
F.acoustic_panels(S, 0.2, 2.9, math.radians(90), n=2, name="AcousticPanels_W")
F.plant(S, 0.55, 2.4)
S.anchor("STATUS", "", TX, TY, n=1)
F.status_lamp(S, TX, TY, z=2.2, name="StatusLamp_01")

# ---- 電話亭 ×2（並排靠北牆，門朝南）
BW, BD = 1.05, 1.2
for k, bx in enumerate((PX + 0.07 + BW / 2, 5.8 - 0.02 - BW / 2)):
    by = 5.8 - 0.02 - BD / 2
    _, (sx, sy), yaw = F.phone_booth(S, bx, by, 0.0, w=BW, d=BD, felt=("fabric_teal", "fabric_orange")[k],
                                     name="PhoneBooth_%02d" % (k + 1))
    S.anchor("SEAT", "booth", sx, sy, yaw, n=k + 1)
    S.anchor("STATUS", "", bx, by, n=k + 2)
    F.status_lamp(S, bx, by, z=2.2 + 0.06, name="StatusLamp_%02d" % (k + 2))

# ---- 休憩角：雙人沙發（靠東牆，面西）、立燈；座位前開導航通道
SX, SY = 5.8 - 0.45, 3.0
F.sofa(S, SX, SY, math.pi / 2, w=1.4, d=0.85, color="chair_green", name="Sofa")
for k, dy in enumerate((-0.33, 0.33)):
    S.anchor("SEAT", "lounge", SX - 0.15, SY + dy, 90, n=k + 1)
S.extra_free.append((4.55, SY - 0.55, 5.0, SY + 0.55))
F.floor_lamp(S, 5.5, 2.05)

# ---- 通道：東牆吸音板（門洞北側）
F.acoustic_panels(S, 5.8, 3.25, math.radians(-90), n=2, w=0.5, hh=0.5, z=1.75, name="AcousticPanels_E")

# ---- 燈具
S.ceiling_panel(TX, TY, power=110)
S.ceiling_panel(4.7, 3.2, w=0.6, d=0.6, power=55)
S.ceiling_panel(1.5, 1.1, w=0.6, d=0.6, power=55)
S.ceiling_panel(4.5, 1.1, w=0.6, d=0.6, power=55)

S.finish(HERE)
