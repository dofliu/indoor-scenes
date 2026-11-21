"""場景 019：倉儲物流區（選擇式棧板貨架 6 排、3 條堆高機走道、收發貨碼頭、纏繞機、出貨辦公桌）。執行：python3.13 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("019", "warehouse", "倉儲物流區", "Warehouse & Logistics Area", "factory", (16, 12),
          tags=["factory", "warehouse", "logistics", "pallet-rack", "forklift", "loading-dock", "picking", "shipping"])
R = math.radians
PI = math.pi

# ---- 結構（人員門 1.0 m 依規格；南牆碼頭捲門為貼牆裝飾件，非門洞）
S.add_door("W", 3)
S.add_door("E", 3)
S.add_door("S", 5)
S.add_door("N", 7)
S.add_window("E", 7.0, width=2.0, sill=2.0, height=0.7)    # 高窗（貨架上方採光）
F.mat("floor_sealed", (0.58, 0.58, 0.56), rough=0.4)          # 封閉劑處理混凝土地坪
S.build_shell(floor="floor_sealed", wall="wall", accent={"N": "wall_dark"})
S.light_grid(4, 3, power=55)

# ---- 選擇式棧板貨架 6 排（南北向，y 4.85–11.45），3 條 3 m 堆高機走道
RY = 8.15
RACKS = [  # (x 中心, yaw：+90 取貨面朝東、-90 朝西)
    (0.75, 90), (4.75, -90), (5.85, 90), (9.85, -90), (10.95, 90), (15.25, -90)]
PATTERNS = [
    None,
    ["wrapped", "cartons", "cartons", "empty", "bins", "wrapped", "cartons", "drum", "empty", "wrapped", "cartons", "bins"],
    ["bins", "bins", "cartons", "wrapped", "empty", "cartons", "drum", "drum", "wrapped", "cartons", "cartons"],
    ["cartons", "empty", "wrapped", "wrapped", "cartons", "bins", "cartons", "wrapped", "drum", "empty"],
    ["drum", "cartons", "wrapped", "bins", "cartons", "cartons", "empty", "wrapped", "bins", "cartons", "wrapped", "cartons", "empty"],
    ["cartons", "wrapped", "empty", "cartons", "cartons", "bins", "wrapped", "drum", "cartons"],
]
for i, ((rx, yaw), pat) in enumerate(zip(RACKS, PATTERNS)):
    F.pallet_rack(S, rx, RY, R(yaw), bays=3, bay_w=2.1, d=1.0, pattern=pat, name="Rack_%02d" % (i + 1))

AISLES = [(2.75, (0.12, 0.42, 0.80)), (7.85, (0.16, 0.62, 0.30)), (13.1, (0.85, 0.30, 0.12))]
for k, (ax, col) in enumerate(AISLES):
    F.aisle_sign(S, ax, 4.8, 0, color=col, name="AisleSign_%02d" % (k + 1))
F.safety_mirror(S, 5.3, 4.72, PI, name="SafetyMirror_01")
F.safety_mirror(S, 10.4, 4.72, PI, name="SafetyMirror_02")

# 揀貨站位（每條走道兩側各一）＋狀態點
PICKS = [(1.85, 6.0, 90), (3.65, 9.5, -90), (6.95, 6.0, 90), (8.75, 9.5, -90), (12.05, 6.0, 90), (14.15, 9.5, -90)]
for (px, py, yw) in PICKS:
    S.anchor("STAND", "pick", px, py, yw)
    S.anchor("STATUS", "", px, py)

# ---- 地面標線：東西向堆高機主通道、走道邊線、碼頭／停車區框線
F.floor_line(S, 0.4, 3.1, 15.6, 3.1, name="ForkLane_S")
F.floor_line(S, 1.4, 4.7, 15.6, 4.7, name="ForkLane_N")
for xx in (1.4, 4.1, 6.5, 9.2, 11.6, 14.6):
    F.floor_line(S, xx, 4.7, xx, 11.5, name="AisleEdge_%d" % (xx * 10))
F.floor_line(S, 9.9, 2.35, 12.1, 2.35, name="DockZone_N")
F.floor_line(S, 12.3, 0.3, 12.3, 2.35, name="ParkZone_W")
F.floor_line(S, 12.3, 1.75, 15.6, 1.75, name="ParkZone_N")

# ---- 南牆：裝卸碼頭（捲門＋升降平台）、碼頭控制盒
F.dock_door(S, 11.0, 0.2, 0, w=3.0, name="DockDoor")
F.dock_control(S, 9.15, 0.2, 0, name="DockControl")
S.anchor("STAND", "dock", 9.15, 0.8, 180)
S.anchor("STATUS", "", 9.15, 0.8)

# ---- 東南：堆高機停車＋充電；待出貨棧板
F.forklift(S, 14.2, 1.0, R(90), name="Forklift_01")
F.battery_charger(S, 15.6, 1.0, R(90), name="Charger_01")
S.anchor("STAND", "forklift", 14.3, 2.25, 180)
S.anchor("STATUS", "", 14.3, 2.25)
S.anchor("POI", "charger", 15.2, 2.25, 180)
F.pallet(S, 12.95, 2.45, 0, load="none", name="Pallet_staged")
F.carton_stack(S, 12.75, 2.45, 0, n=3, z=0.135, name="Cartons_staged_01")
F.carton_stack(S, 13.2, 2.45, R(90), n=2, z=0.135, name="Cartons_staged_02")
F.pallet_jack(S, 8.95, 2.55, R(-90), name="PalletJack")

# ---- 南側西段：出貨辦公桌、包裝台、纏繞機
F.desk(S, 1.6, 0.6, PI, w=1.4, d=0.7, name="ShippingDesk")
F.chair(S, 1.6, 1.3, PI, name="ShippingChair")
F.monitor(S, 1.45, 0.45, PI, name="ShippingMonitor")
F.keyboard(S, 1.45, 0.75, PI, name="ShippingKeyboard")
S.anchor("SEAT", "desk", 1.6, 1.3, 180)
S.anchor("STATUS", "", 1.6, 1.3)
lp = Piece(S, "LabelPrinter", 2.05, 0.5, 0.74, coll="PROPS")
lp.box(0, 0, 0.09, 0.22, 0.28, 0.18, "plastic_white").box(0, -0.141, 0.12, 0.12, 0.004, 0.02, "plastic_black")
lp.box(0, -0.16, 0.06, 0.1, 0.04, 0.002, "paper")
lp.finish(obstacle=False)
S.anchor("POI", "labelprinter", 2.05, 1.25, 180)
F.table(S, 3.6, 0.6, 0, w=1.4, d=0.7, h=0.9, top="wood_light", name="PackingTable")
F.carton_stack(S, 3.3, 0.6, 0, n=1, z=0.9, name="Cartons_packing")
tp = Piece(S, "TapeDispenser", 3.95, 0.65, 0.9, coll="PROPS")
tp.box(0, 0, 0.05, 0.12, 0.25, 0.1, "chair_red").cyl(0, 0.05, 0.1, 0.05, 0.06, "carton_tape", seg=12, axis="X")
tp.finish(obstacle=False)
F.carton_stack(S, 2.55, 0.4, 0, n=4, name="Cartons_flat")
S.anchor("STAND", "packing", 3.6, 1.3, 180)
S.anchor("STATUS", "", 3.6, 1.3)
F.stretch_wrapper(S, 7.6, 1.5, PI, name="StretchWrapper")
S.anchor("STAND", "wrapper", 6.35, 2.5, -90)
S.anchor("STATUS", "", 6.35, 2.5)

# ---- 西牆：庫存看板；滅火器
F.whiteboard(S, 0.2, 4.15, R(90), w=1.0, h=0.9, z=1.0, name="InventoryBoard")
S.anchor("STAND", "whiteboard", 0.95, 4.15, 90)
F.fire_extinguisher(S, 0.35, 1.9, name="Extinguisher_W")
F.fire_extinguisher(S, 15.65, 3.9, name="Extinguisher_E")

# ---- 堆高機路線點（POI_route_*）與巡迴路線
ROUTE = [(2.75, 3.9), (2.75, 10.9), (7.85, 10.9), (7.85, 3.9), (13.1, 3.9), (13.1, 10.9), (11.0, 1.6)]
for (rx, ry) in ROUTE:
    S.anchor("POI", "route", rx, ry, 0)
S.extra_json["routes"] = {
    "forklift": {"desc": "堆高機巡迴：碼頭 → A 走道 → B 走道 → C 走道 → 碼頭（沿 POI_route_* 依序）",
                 "waypoints": ["POI_route_07", "POI_route_04", "POI_route_01", "POI_route_02", "POI_route_03",
                               "POI_route_04", "POI_route_05", "POI_route_06", "POI_route_05", "POI_route_07"],
                 "vehicle_clearance_m": 1.3}
}

S.scene.view_settings.exposure = -0.5
S.finish(HERE)
