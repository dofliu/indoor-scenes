"""場景 012：伺服器機房（雙排機櫃、冷熱通道、冷卻單元、UPS、維運工作台）。執行：python3.13 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("012", "server_room", "伺服器機房", "Server Room", "office", (8, 6),
          tags=["datacenter", "server", "rack", "cooling", "ups"])
R = math.radians

S.add_door("S", 1)
S.add_door("W", 3)
S.build_shell(floor="floor_epoxy", wall="wall", accent={"N": "wall_dark"})
S.light_grid(2, 2, power=120)

# 北排機櫃（正面朝南 yaw=0）／南排機櫃（正面朝北 yaw=180）
for i in range(6):
    cx = 2.3 + 0.6 * i
    F.server_rack(S, cx, 4.5, 0, name="Rack_N_%02d" % (i + 1))
    F.server_rack(S, cx, 1.9, R(180), name="Rack_S_%02d" % (i + 1))
    S.anchor("STAND", "rack", cx, 3.3, 0, n=i + 1)         # 站在通道面向北排
    S.anchor("STAND", "rack", cx, 3.1, 180, n=i + 7)       # 面向南排
for k in range(3):
    S.anchor("STATUS", "", 2.6 + 1.2 * k, 3.2, n=k + 1)
    F.status_lamp(S, 2.6 + 1.2 * k, 3.2, z=2.2, name="StatusLamp_%d" % (k + 1))

# 線槽
F.cable_tray(S, 3.8, 4.5, 3.6, name="CableTray_N")
F.cable_tray(S, 3.8, 1.9, 3.6, name="CableTray_S")

# 東牆：冷卻單元 ×2、UPS（正面朝西 -X：yaw=-90 使本地 -Y 朝 +X? 採 yaw=R(-90) → 本地 -Y 轉向 -X）
for i, yy in enumerate((1.4, 3.0)):
    F.crac_unit(S, 7.55, yy, R(-90), name="CoolingUnit_%d" % (i + 1))
    S.anchor("POI", "cooling", 6.65, yy, -90, n=i + 1)
F.ups_cabinet(S, 7.55, 4.6, R(-90), name="UPS_1")
S.anchor("POI", "ups", 6.65, 4.6, -90, n=1)

# 西北角：維運工作台（使用者坐南側面北）＋推車
F.desk(S, 1.0, 5.4, 0, w=1.4, d=0.7, name="OpsDesk")
F.monitor(S, 0.8, 5.5, 0, name="Monitor_01")
F.monitor(S, 1.3, 5.5, 0, name="Monitor_02")
F.keyboard(S, 1.0, 5.25, 0, name="Keyboard_01")
F.chair(S, 1.0, 4.6, 0, name="OpsChair")
S.anchor("SEAT", "desk", 1.0, 4.6, 0, n=1)
S.anchor("STATUS", "", 1.0, 5.4, n=4)
F.crash_cart(S, 0.6, 1.2, R(90), name="CrashCart")
S.anchor("POI", "crashcart", 1.2, 1.2, 90, n=1)
F.cabinet(S, 0.45, 2.4, R(90), w=0.9, h=1.8, name="SpareParts")
S.anchor("POI", "spareparts", 1.2, 2.4, 90, n=2)

S.finish(HERE)
