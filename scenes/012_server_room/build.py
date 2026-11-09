"""場景 012：伺服器機房（冷熱通道、2×6 機櫃、精密空調、UPS、值班監控桌）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("012", "server_room", "伺服器機房", "Server Room", "factory", (8, 6),
          tags=["server", "datacenter", "racks", "cold-aisle", "12-racks", "ai-company"])
R = math.radians

S.add_door("S", 1)
S.add_door("E", 3)
S.build_shell(floor="floor_concrete", wall="wall", accent={"N": "wall_dark"})
S.light_grid(3, 2, margin=1.8, power=35)

# 冷通道（藍）標示於兩排機櫃之間
F.rug(S, 3.6, 3.0, 3.8, 1.0, "rug_blue", name="ColdAisle")

# ---- 兩排機櫃（各 6 座），正面朝冷通道 y=3
xs = [2.1 + 0.6 * i for i in range(6)]
n = 0
for i, x in enumerate(xs):
    n += 1
    F.server_rack(S, x, 2.0, R(180), seed=i, name="Rack_S%02d" % (i + 1))   # 南排，面向北
    S.anchor("STAND", "rack", x, 2.9, 180, n=n)
for i, x in enumerate(xs):
    n += 1
    F.server_rack(S, x, 4.0, 0, seed=i + 6, name="Rack_N%02d" % (i + 1))    # 北排，面向南
    S.anchor("STAND", "rack", x, 3.1, 0, n=n)

# ---- 天花板線槽（沿機櫃上方）
F.cable_tray(S, 1.7, 2.0, 5.5, 2.0, name="Tray_S")
F.cable_tray(S, 1.7, 4.0, 5.5, 4.0, name="Tray_N")

# ---- 北牆：兩台精密空調
for i, cx in enumerate((5.9, 7.1), 1):
    F.crac_unit(S, cx, 5.35, 0, name="CRAC_%d" % i)
S.anchor("POI", "crac", 6.5, 4.6, 180, n=1)

# ---- 北牆西側：UPS／配電櫃（2 組）
for i, cx in enumerate((1.3, 2.2)):
    F.cabinet(S, cx, 5.575, 0, w=0.9, d=0.45, h=1.9, color="metal_dark", name="UPS_%d" % (i + 1))
S.anchor("POI", "ups", 1.3, 4.95, 0, n=1)

# ---- 東南角：值班監控桌（使用者坐北側，面向南牆螢幕）
F.desk(S, 6.8, 0.55, 0, w=1.8, d=0.7, name="OpsDesk")
F.monitor(S, 6.4, 0.62, R(180), name="Monitor_01")
F.monitor(S, 7.2, 0.62, R(180), name="Monitor_02")
F.keyboard(S, 6.8, 0.82, R(180), name="Keyboard_01")
F.chair(S, 6.8, 1.3, R(180), name="OpsChair")
S.anchor("SEAT", "desk", 6.8, 1.3, 180, n=1)
F.screen_wall(S, 6.8, 0.2, 2.4, h=0.9, yaw=R(180), z=1.3, name="StatusWall")

# ---- 西側：入口旁滅火器箱（POI）與備品櫃
F.cabinet(S, 0.425, 4.2, R(90), w=0.9, h=1.8, name="SpareParts")
S.anchor("POI", "spares", 1.2, 4.2, 90, n=1)

# ---- 狀態標籤：兩排機櫃上方與值班桌
S.anchor("STATUS", "", 2.7, 3.0, n=1)
S.anchor("STATUS", "", 4.5, 3.0, n=2)
S.anchor("STATUS", "", 6.8, 0.9, n=3)
for i, (sx, sy) in enumerate(((2.7, 3.0), (4.5, 3.0), (6.8, 0.9)), 1):
    F.status_lamp(S, sx, sy, z=2.2, name="StatusLamp_%02d" % i)

S.finish(HERE, cam_elev=56)
