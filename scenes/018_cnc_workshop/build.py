"""場景 018：CNC 加工車間（立式加工中心 ×4＋機器手臂上下料單元 ×2、CNC 車床 ×2）。執行：python3.13 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("018", "cnc_workshop", "CNC 加工車間", "CNC Machining Workshop", "factory", (16, 12),
          tags=["factory", "cnc", "machining", "milling", "turning", "robot-cell", "machine-tending", "workshop"])
R = math.radians
PI = math.pi

# ---- 結構
S.add_door("W", 5)
S.add_door("E", 5)
S.add_door("S", 7)
S.add_window("N", 4.2, width=2.0, sill=1.9, height=0.8)
S.add_window("N", 11.8, width=2.0, sill=1.9, height=0.8)
S.add_window("S", 4.6, width=1.6, sill=1.6, height=0.9)
F.mat("floor_epoxy_grey", (0.46, 0.48, 0.50), rough=0.35)        # 灰色環氧地坪
S.build_shell(floor="floor_epoxy_grey", wall="wall", accent={"N": "wall_accent"})
S.light_grid(4, 3, power=55)

# ---- 北側：立式加工中心 ×4（操作面朝南），每兩台之間一個機器手臂上下料單元
MY = 9.6                       # 機台中心 y（前緣 8.6、後緣 10.6，後方排屑機＋集屑車）
MILLS = [(2.0, -1, "green"), (6.4, 1, "green"), (9.6, -1, "yellow"), (14.0, 1, "green")]
for i, (mx, side, lit) in enumerate(MILLS):
    F.cnc_mill(S, mx, MY, 0, hmi_side=side, lit=lit, name="M%02d_vmc" % (i + 1))
    hx = mx + side * 1.0
    S.anchor("STAND", "machine", hx, 7.9, 0, n=i + 1)
    S.anchor("STATUS", "", hx, 7.9, n=i + 1)

# 機器手臂單元（A：服務 M01/M02；B：服務 M03/M04）
CELLS = [(4.2, 120), (11.8, -110)]
for k, (cx, j1) in enumerate(CELLS):
    x0, x1 = cx - 1.1, cx + 1.1
    F.industrial_robot(S, cx, 9.35, 0, j1=j1, name="Robot_%02d" % (k + 1))
    F.parts_table(S, cx - 0.35, 7.55, 0, done=6 + 3 * k, name="PartsTable_%02d" % (k + 1))
    F.safety_fence(S, x0, 6.9, x1, 6.9, gate=(1.4, 2.2), name="Fence_%02d_S" % (k + 1))
    F.safety_fence(S, x0, 6.9, x0, 8.55, name="Fence_%02d_W" % (k + 1))
    F.safety_fence(S, x1, 6.9, x1, 8.55, name="Fence_%02d_E" % (k + 1))
    F.safety_fence(S, x0, 10.65, x1, 10.65, name="Fence_%02d_N" % (k + 1))
    F.teach_pendant_stand(S, cx - 0.5, 6.55, PI, name="RobotController_%02d" % (k + 1))
    S.anchor("STAND", "robot", cx - 0.5, 5.85, 0, n=k + 1)          # 控制櫃／教導器操作位
    S.anchor("STAND", "loading", cx + 0.7, 7.55, 90, n=k + 1)        # 進柵門後於料盤台上下料
    S.anchor("POI", "robot", cx, 8.45, 0, n=k + 1)                   # 機器手臂前方（保養／示教；朝北面向手臂）
    S.anchor("STATUS", "", cx - 0.5, 5.85, n=len(MILLS) + k + 1)
    F.floor_line(S, x0, 6.75, x1, 6.75, name="FenceLine_%02d" % (k + 1))

# ---- 主通道（東西向，連接東、西門）地面標線
for yy in (4.0, 6.2):
    F.floor_line(S, 0.4, yy, 15.6, yy, name="AisleLine_%d" % (yy * 100))
for xx in (6.3, 7.7):
    F.floor_line(S, xx, 0.3, xx, 4.0, name="DoorLane_%d" % (xx * 10))

# ---- 南側東段：CNC 車床 ×2（背靠南牆、操作面朝北，排屑機朝西）
for i, lx in enumerate((10.0, 13.9)):
    F.cnc_lathe(S, lx, 1.0, PI, lit="green" if i == 0 else "red", name="M%02d_lathe" % (len(MILLS) + i + 1))
    hx = lx - 1.18
    S.anchor("STAND", "lathe", hx, 2.5, 180, n=i + 1)
    S.anchor("STATUS", "", hx, 2.5, n=len(MILLS) + len(CELLS) + i + 1)
F.chip_cart(S, 11.5, 3.2, 0, name="ChipCart")
S.anchor("POI", "chips", 11.5, 2.45, 0, n=1)
F.pallet(S, 14.0, 3.35, 0, name="Pallet_blanks")
F.bar_rack(S, 15.45, 3.2, R(-90), w=1.8, name="BarRack")
S.anchor("POI", "material", 14.65, 2.3, -90, n=1)

# ---- 南側西段：刀具區、對刀、鉗工台、量測平台
F.tool_chest(S, 1.0, 0.5, PI, name="ToolChest_01")
F.tool_chest(S, 2.0, 0.5, PI, color=(0.12, 0.28, 0.50), name="ToolChest_02")
S.anchor("POI", "tools", 1.5, 1.3, 180, n=1)
F.table(S, 3.6, 0.58, 0, w=1.4, d=0.7, h=0.9, top="cabinet", name="PresetterBench")
F.tool_presetter(S, 3.6, 0.6, PI, z=0.9, name="ToolPresetter")
S.anchor("STAND", "presetter", 3.6, 1.35, 180, n=1)
F.vise_bench(S, 0.6, 2.9, R(90), name="ViseBench")
S.anchor("STAND", "bench", 1.4, 2.9, 90, n=1)
F.granite_table(S, 4.6, 3.0, 0, name="GraniteTable")
S.anchor("STAND", "inspect", 4.6, 2.05, 0, n=1)
F.fire_extinguisher(S, 0.35, 6.4, name="Extinguisher_W")
F.fire_extinguisher(S, 8.15, 0.32, name="Extinguisher_S")

# ---- 東牆：生產看板（白板）；主通道上方吊掛 Andon
F.whiteboard(S, 15.8, 6.9, R(-90), w=1.4, name="ProductionBoard")
S.anchor("STAND", "whiteboard", 15.05, 6.9, -90, n=1)
F.hanging_display(S, 8.0, 5.1, 0, name="AndonBoard")
S.anchor("POI", "andon", 8.0, 4.4, 0, n=1)

S.scene.view_settings.exposure = -0.5
S.finish(HERE)
