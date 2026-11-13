"""場景 015：多功能活動空間（階梯座位、舞台、可移動隔間；通用風格，無任何品牌／商標）。
執行：python3 build.py（需 pip install bpy）
配置：西牆 4 階階梯座位（面向東）→ 中央活動地板（懶骨頭＋2 排活動椅）→ 東牆矮舞台與大螢幕。
南側以附輪隔間板圍出工作坊分組區；北側為茶點台、站立圓桌與影音控制台。
註：階梯座位與舞台上的錨點為「高架錨點」（z>0，為人物腳底高度），不在 z=0 導航網格上，
    由最近的導航點直接移動到錨點（見 SPEC.md「高架錨點」）。"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("015", "event_space", "多功能活動空間", "Multipurpose Event Space", "social", (16, 12),
          tags=["event", "town-hall", "tiered-seating", "stage", "movable-partition", "workshop", "multipurpose"])
R = math.radians

# ---- 結構：6 個門、北／南採光窗
S.add_door("S", 3)
S.add_door("S", 13)
S.add_door("N", 5)
S.add_door("N", 13)
S.add_door("E", 1)
S.add_door("E", 11)
S.add_window("N", 9, width=2.4)
S.add_window("S", 8, width=3.0)
S.build_shell(floor="floor_wood", wall="wall", accent={"E": "wall_dark"})
S.light_grid(4, 3, power=60)

# ---- 西牆：4 階階梯座位（每階 6 席，中央走道），觀眾面向東
_, seats = F.tiered_seating(S, 0.2 + 1.8, 6.0, R(-90), w=6.4, tiers=4, depth=0.9, rise=0.45, name="TieredSeating")
for n, (sx, sy, sz, k) in enumerate(seats, 1):
    S.anchor("SEAT", "tier", sx, sy, -90, n=n, z=sz)

# ---- 東牆：矮舞台、大螢幕、講桌、喇叭、燈桿
ST_H = 0.2
F.stage_platform(S, 14.3, 6.0, R(-90), w=6.0, d=3.0, h=ST_H, name="Stage")
F.screen_wall(S, 15.8, 6.0, 4.6, h=2.0, yaw=R(-90), z=0.75, name="StageScreen")
F.lectern(S, 13.5, 8.1, R(90), z=ST_H, name="Lectern")
S.anchor("STAND", "lectern", 14.0, 8.1, 90, n=1, z=ST_H)
S.anchor("STAND", "present", 13.6, 6.0, 90, n=1, z=ST_H)
S.anchor("STAND", "present", 13.9, 4.6, 90, n=2, z=ST_H)
for k, sy in enumerate((3.35, 8.65), 1):
    F.pa_speaker(S, 15.3, sy, R(-90), z=ST_H, name="Speaker_%d" % k)
F.lighting_truss(S, 11.6, 6.0, 6.0, yaw=R(-90), z=2.7, lamps=5, name="StageLightTruss")

# ---- 中央活動地板：地毯、4 個懶骨頭、2 排各 6 張活動椅（皆面向東）
F.rug(S, 7.9, 6.0, 6.6, 5.6, "rug_blue", name="FloorRug")
cols = ("fabric_orange", "fabric_teal", "fabric_grey", "fabric_orange")
for n, by in enumerate((4.2, 5.4, 6.6, 7.8), 1):
    F.beanbag(S, 5.6, by, color=cols[n - 1], name="Beanbag_%d" % n)
    bb = bpy.data.objects["Beanbag_%d" % n]
    bb.rotation_euler = (0, 0, R(-90))
    S.anchor("SEAT", "beanbag", 5.6, by, -90, n=n)
n = 0
for rx in (8.2, 9.5):
    for i in range(6):
        n += 1
        cy = 3.75 + 0.9 * i
        F.stack_chair(S, rx, cy, R(-90), color="chair_seat" if rx < 9 else "chair_green", name="AudienceChair_%02d" % n)
        S.anchor("SEAT", "audience", rx, cy, -90, n=n)

# ---- 南側：可移動隔間圍出的工作坊分組區（白板面朝南向區內）
for k, px in enumerate((6.3, 8.0, 9.7), 1):
    F.movable_partition(S, px, 2.75, 0, color=("fabric_teal", "fabric_orange", "fabric_teal")[k - 1], name="Partition_%d" % k)
F.movable_partition(S, 10.85, 1.5, R(-90), color="fabric_orange", name="Partition_4")
F.table(S, 8.0, 1.15, 0, w=1.8, d=0.8, name="WorkshopTable")
F.laptop(S, 7.7, 1.15, 0, z=0.74)
for n, (sx, sy, yw) in enumerate(((7.55, 1.95, 180), (8.45, 1.95, 180), (6.75, 1.15, -90), (9.25, 1.15, 90)), 1):
    F.stool(S, sx, sy, h=0.48, color="fabric_orange" if n % 2 else "fabric_teal", name="WorkshopStool_%d" % n)
    S.anchor("SEAT", "workshop", sx, sy, yw, n=n)
S.anchor("STAND", "whiteboard", 9.9, 2.15, 0, n=1)
# 收納：西南角停放 2 片備用隔間板
for k, px in enumerate((0.55, 1.15), 5):
    F.movable_partition(S, px, 1.25, R(90), color="fabric_grey", name="Partition_%d" % k)
S.anchor("POI", "partition", 1.9, 1.25, 90, n=1)

# ---- 北側：茶點台（咖啡機）、2 張站立圓桌、影音控制台
F.kitchen_counter(S, 9.0, 11.5, 0, w=3.0, name="CateringCounter")
F.coffee_machine(S, 8.2, 11.5, 0, name="CoffeeMachine")
pr = Piece(S, "CateringTrays", 9.6, 11.45, 0.9, coll="PROPS")
for dx in (-0.35, 0.35):
    pr.box(dx, 0, 0.015, 0.5, 0.32, 0.03, "metal")
    for i in range(3):
        pr.cyl(dx - 0.15 + 0.15 * i, 0, 0.05, 0.05, 0.04, "paper", seg=10)
pr.finish(obstacle=False)
S.anchor("POI", "coffee", 8.2, 10.75, 0, n=1)
S.anchor("POI", "catering", 9.6, 10.75, 0, n=1)
for k, (tx, ty) in enumerate(((6.4, 10.2), (11.6, 10.2)), 1):
    F.round_table(S, tx, ty, r=0.4, name="CocktailTable_%d" % k)
    S.anchor("STAND", "cocktail", tx - 0.75, ty, -90, n=2 * k - 1)
    S.anchor("STAND", "cocktail", tx + 0.75, ty, 90, n=2 * k)
F.control_console(S, 2.4, 10.6, R(-90), w=1.6, screens=2, name="AVConsole")
F.chair(S, 1.55, 10.6, R(-90), color="chair_red", name="AVChair")
S.anchor("SEAT", "av", 1.55, 10.6, -90, n=1)

# ---- 植栽
for (px, py) in ((15.3, 2.3), (15.3, 9.7), (12.2, 0.65), (3.6, 11.3)):
    F.plant(S, px, py)

# ---- 狀態標籤：舞台、看台（南／北半部）、活動椅區、工作坊區、影音控制台
S.anchor("STATUS", "", 13.6, 6.0, n=1, z=2.5)
F.pendant_status_lamp(S, 13.6, 6.0, z=2.5, name="StatusPendant_01")
S.anchor("STATUS", "", 2.6, 4.3, n=2, z=2.6)
S.anchor("STATUS", "", 2.6, 7.7, n=3, z=2.6)
S.anchor("STATUS", "", 8.0, 6.0, n=4)
F.pendant_status_lamp(S, 8.0, 6.0, z=2.2, name="StatusPendant_04", color=(0.2, 0.55, 0.95))
S.anchor("STATUS", "", 8.0, 1.15, n=5)
F.pendant_status_lamp(S, 8.0, 1.15, z=2.2, name="StatusPendant_05", color=(0.95, 0.65, 0.1))
S.anchor("STATUS", "", 2.0, 10.6, n=6)
F.pendant_status_lamp(S, 2.0, 10.6, z=2.2, name="StatusPendant_06")

S.finish(HERE)
