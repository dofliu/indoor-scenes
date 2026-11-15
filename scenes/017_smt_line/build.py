"""場景 017：電子組裝產線（SMT 線＋防靜電作業站）。執行：python3.13 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("017", "smt_line", "電子組裝產線", "Electronics Assembly Line (SMT)", "factory", (18, 10),
          tags=["factory", "electronics", "smt", "assembly-line", "pick-and-place", "reflow", "esd", "workstation"])
R = math.radians
PI = math.pi

# ---- 結構
S.add_door("W", 3)
S.add_door("E", 3)
S.add_door("S", 11)
S.add_door("N", 15)
S.add_window("N", 6, width=2.0, sill=1.2, height=1.2)
S.add_window("N", 11, width=2.0, sill=1.2, height=1.2)
S.add_window("S", 15.8, width=1.6, sill=1.6, height=0.9)
F.mat("floor_esd", (0.42, 0.50, 0.47), rough=0.35)       # 灰綠色防靜電環氧地坪
S.build_shell(floor="floor_esd", wall="wall", accent={"N": "wall_accent"})
S.light_grid(4, 2, power=70)

# ---- SMT 產線：由西向東（送板 → 印刷 → SPI → 貼片 ×2 → 迴焊 → AOI → 收板），操作面朝南
LY = 7.2
LINE = [  # (種類, 寬, 用途名, 警示燈)
    ("loader", 1.0, "loader", "green"), ("printer", 1.3, "printer", "green"), ("spi", 1.0, "spi", "green"),
    ("pnp", 1.5, "pnp", "green"), ("pnp", 1.5, "pnp", "yellow"), ("reflow", 4.2, "reflow", "green"),
    ("aoi", 1.1, "aoi", "green"), ("unloader", 1.0, "unloader", "green"),
]
GAPS = [0.4, 0.4, 0.4, 0.3, 0.4, 0.6, 0.4]
x = 1.3
nm = 0
for i, (kind, w, use, lit) in enumerate(LINE):
    cx = x + w / 2
    nm += 1
    name = "M%02d_%s" % (nm, use)
    if kind in ("loader", "unloader"):
        F.pcb_magazine_loader(S, cx, LY, 0, w=w, lit=lit, name=name)
    elif kind == "reflow":
        F.reflow_oven(S, cx, LY, 0, w=w, lit=lit, name=name)
    else:
        F.smt_machine(S, cx, LY, 0, w=w, kind=kind, lit=lit, name=name)
    front = LY - 0.7 - (0.3 if kind == "pnp" else 0.0)
    S.anchor("STAND", "machine", cx, front - 0.6, 0, n=nm)
    S.anchor("STATUS", "", cx, LY, n=nm)
    x += w
    if i < len(GAPS):
        g = GAPS[i]
        F.conveyor(S, x + g / 2, LY, g, 0, populated=i >= 3, name="Conveyor_%02d" % (i + 1))
        x += g
LINE_END = x

# ---- 地面標線：主通道（產線作業區與作業站之間）、門口斑馬區
for yy in (4.45, 5.45):
    F.floor_line(S, 0.5, yy, 17.5, yy, name="AisleLine_%d" % (yy * 100))
for xx in (10.4, 11.6):
    F.floor_line(S, xx, 0.3, xx, 4.45, name="DoorLane_%d" % (xx * 10))

# ---- 防靜電作業站 ×6（插件／目檢／返修），作業員坐南側面向產線
BY = 3.4
BXS = (2.6, 4.2, 5.8, 7.4, 13.4, 15.0)
for i, bx in enumerate(BXS):
    F.esd_workbench(S, bx, BY, 0, seed=i, name="ESDBench_%02d" % (i + 1))
    F.chair(S, bx - 0.05, BY - 0.75, 0, color="chair_seat", name="BenchChair_%02d" % (i + 1))
    S.anchor("SEAT", "station", bx - 0.05, BY - 0.75, 0, n=i + 1)
    S.anchor("STATUS", "", bx, BY, n=len(LINE) + i + 1)
    F.pendant_status_lamp(S, bx, BY + 0.05, z=2.2, name="StatusPendant_%02d" % (i + 1),
                          color=(0.95, 0.75, 0.1) if i == 3 else (0.2, 0.9, 0.3))
# 返修站（第 4、6 站）：顯微鏡＋焊接台；目檢站螢幕
F.microscope(S, 7.4 + 0.42, BY - 0.12, 0, z=0.76, name="Microscope_rework")
F.soldering_station(S, 7.4 - 0.42, BY - 0.2, 0, z=0.76, name="Solder_rework_1")
F.soldering_station(S, 15.0 - 0.42, BY - 0.2, 0, z=0.76, name="Solder_rework_2")
F.monitor(S, 13.4 + 0.5, BY + 0.1, 0, z=0.76, name="InspectMonitor")

# ---- 吊掛產線看板（Andon），面向南側主通道
F.hanging_display(S, 10.4, 5.0, 0, name="AndonBoard")
S.anchor("POI", "andon", 10.4, 3.6, 0, n=1)

# ---- 南牆：料捲架 ×3、鋼板櫃、供料器台車 ×2；門東側為包裝台與成品架
for i, rx in enumerate((1.9, 3.2, 4.5)):
    F.reel_rack(S, rx, 0.47, PI, seed=i, name="ReelRack_%02d" % (i + 1))
S.anchor("POI", "reel", 3.2, 1.25, 180, n=1)
F.cabinet(S, 5.9, 0.425, PI, w=0.9, h=1.9, name="StencilCabinet")
S.anchor("POI", "stencil", 5.9, 1.2, 180, n=1)
for i, fx in enumerate((7.4, 8.5)):
    F.feeder_cart(S, fx, 0.6, 0, name="FeederCart_%02d" % (i + 1))
S.anchor("POI", "feeder", 7.95, 1.4, 180, n=1)
F.table(S, 13.4, 0.6, 0, w=2.0, d=0.7, h=0.8, top="desk_white", name="PackingTable")
F.carton_stack(S, 12.8, 0.62, 0, n=1, z=0.8, name="Carton_table")
F.laptop(S, 13.9, 0.55, PI, z=0.8, name="PackingLaptop")
F.carton_stack(S, 14.9, 0.55, 0, n=3, name="Cartons_floor")
S.anchor("STAND", "packing", 13.4, 1.5, 180, n=1)
F.tote_shelf(S, 16.4, 0.47, PI, name="OutputShelf")
S.anchor("POI", "output", 16.4, 1.25, 180, n=1)

# ---- 西牆：入口防靜電測試站、靜電衣架；東牆：品質看板（白板）、滅火器
F.esd_tester(S, 0.32, 4.15, R(90), name="ESDTester")
S.anchor("POI", "esd", 0.95, 4.15, 90, n=1)
F.coat_rail(S, 0.2, 1.35, R(90), n=3, stand=False, name="ESDCoatRail")
S.anchor("POI", "gown", 0.95, 1.35, 90, n=1)
F.whiteboard(S, 17.8, 5.0, R(-90), w=1.6, name="QualityBoard")
S.anchor("STAND", "whiteboard", 17.05, 5.0, -90, n=1)
F.fire_extinguisher(S, 17.65, 1.6, name="Extinguisher")

# ---- 北牆（產線後方維修走道）：錫膏冰箱、電氣箱
F.fridge(S, 2.3, 9.45, 0, w=0.7, d=0.6, h=1.7, name="SolderPasteFridge")
S.anchor("POI", "paste", 2.3, 8.6, 0, n=1)
F.cabinet(S, 4.0, 9.62, 0, w=1.0, d=0.35, h=1.9, color="cabinet", name="ElectricalPanel")
S.anchor("STAND", "maintenance", 11.4, 8.5, 180, n=1)     # 迴焊爐後側保養位

S.scene.view_settings.exposure = -0.5
S.finish(HERE)
print("LINE_END", LINE_END)
