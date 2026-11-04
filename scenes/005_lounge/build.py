"""場景 005：休憩交誼區（沙發區＋電視、懶骨頭、桌上足球、撞球）。執行：python3 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("005", "lounge", "休憩交誼區", "Lounge & Game Area", "social", (10, 8),
          tags=["social", "lounge", "sofa", "beanbag", "game", "break"])

S.add_door("S", 5)
S.add_door("W", 3)
S.add_door("E", 1)
S.add_window("E", 5, width=1.6)
S.add_window("N", 8.5, width=1.6)
S.add_window("N", 1.5, width=1.6)
S.build_shell(floor="floor_wood", accent={"N": "wall_accent"})
S.light_grid(4, 3, margin=1.6, power=60)

NY = S.D - WALL_T  # 7.8

# ---- 沙發區：電視牆＋電視櫃＋沙發×2＋扶手椅×2＋茶几
F.rug(S, 3.8, 5.2, 4.4, 3.6, "rug_blue")
F.screen_wall(S, 3.8, NY, 2.4, h=1.35, z=1.0)
F.tv_console(S, 3.8, NY - 0.25, 0, w=2.6)
S.anchor("POI", "tv", 3.8, 6.9, 0, n=1)
F.sofa(S, 3.1, 3.7, 0, w=2.0, color="fabric_grey", name="Sofa_1", seat_clear=True)
F.sofa(S, 4.7, 3.7, 0, w=1.3, color="fabric_orange", name="Sofa_2", seat_clear=True)
F.coffee_table(S, 3.8, 5.2, 0, w=1.4, d=0.7)
F.armchair(S, 2.2, 5.2, -90, color="fabric_teal", name="Armchair_1")
F.armchair(S, 5.4, 5.2, 90, color="fabric_teal", name="Armchair_2")
for n, (x, y, yaw) in enumerate(((2.6, 3.8, 0), (3.6, 3.8, 0), (4.7, 3.8, 0), (2.3, 5.2, -90), (5.3, 5.2, 90)), 1):
    S.anchor("SEAT", "sofa", x, y, yaw, n=n)
S.anchor("STATUS", "", 3.8, 4.5, n=1)

# ---- 懶骨頭區（西南角）＋低圓桌
cols = ["fabric_orange", "chair_green", "chair_red", "fabric_teal"]
F.round_table(S, 2.4, 1.6, r=0.35, h=0.4, top="wood_light", name="LowTable")
for n, (x, y, yaw) in enumerate(((1.4, 1.3, -60), (2.4, 0.7, 0), (3.3, 1.4, 70), (1.9, 2.4, -150)), 1):
    F.beanbag(S, x, y, color=cols[n % 4], name="Beanbag_%d" % n)
    S.anchor("SEAT", "beanbag", x, y, yaw, n=n)
S.anchor("STATUS", "", 2.4, 1.6, n=2)

# ---- 遊戲區（東側）：撞球＋桌上足球
F.rug(S, 8.0, 4.4, 3.2, 5.4, "rug")
F.pool_table(S, 7.7, 5.7, 0, w=2.3, d=1.3)
for n, (x, y, yaw) in enumerate(((6.2, 5.7, 90), (9.2, 5.7, -90), (7.2, 4.7, 0), (8.2, 6.7, 180)), 1):
    S.anchor("STAND", "pool", x, y, yaw, n=n)
F.foosball(S, 8.0, 2.8, 90, w=1.4, d=0.75)
for n, (x, y, yaw) in enumerate(((7.2, 2.1, 0), (8.8, 2.1, 0), (7.2, 3.5, 180), (8.8, 3.5, 180)), 1):
    S.anchor("STAND", "foosball", x, y, yaw, n=n)
S.anchor("STATUS", "", 8.0, 4.2, n=3)

# ---- 植栽
F.plant(S, 0.7, 7.3)
F.plant(S, 9.3, 7.3)
F.plant(S, 5.7, 7.3)
F.plant(S, 0.7, 4.5)

S.finish(HERE)
