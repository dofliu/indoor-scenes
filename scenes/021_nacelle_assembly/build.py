"""場景 021：風機機艙組裝廠房（懸掛式天車＋三站式機艙組裝線）。執行：python3.13 build.py
樓高依規格固定 3.0 m，故機艙採中小型機組比例、天車為低淨高懸掛式單樑天車。"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("021", "nacelle_assembly", "風機機艙組裝廠房", "Wind Turbine Nacelle Assembly Hall", "factory", (18, 12),
          tags=["factory", "wind-turbine", "nacelle", "assembly", "bridge-crane", "heavy-assembly", "drivetrain"])
R = math.radians
PI = math.pi
CY = 6.0                       # 組裝線中心線
ST = (3.8, 9.0, 14.2)          # 三個組裝站中心 x（西→東：主機架 → 傳動鏈 → 罩殼／出廠檢驗）

# ---- 結構：西 3（人員）、南 9、北 15；東牆為出貨捲門（裝飾件，非門洞）
S.add_door("W", 3)
S.add_door("S", 9)
S.add_door("N", 15)
S.add_window("N", 5, width=2.4, sill=1.2, height=1.2)
S.add_window("N", 9, width=2.4, sill=1.2, height=1.2)
S.add_window("W", 6, width=2.0, sill=1.2, height=1.2)
F.mat("floor_hall", (0.47, 0.49, 0.50), rough=0.4)
S.build_shell(floor="floor_hall", wall="wall")
S.light_grid(4, 3, power=55)

# 地坪：三個站區塗色＋黃色邊線
fl = Piece(S, "StationZones", coll="STRUCTURE")
zone = F.mat("floor_zone", (0.30, 0.40, 0.44), rough=0.45)
yel = F.mat("safety_yellow", F.SAFETY_YELLOW)
for cx in ST:
    x0, x1, y0, y1 = cx - 2.4, cx + 2.4, CY - 1.95, CY + 1.95
    fl.boxc(x0, y0, 0.0005, x1, y1, 0.003, zone)
    for (a, b, c, d) in ((x0, y0, x1, y0 + 0.08), (x0, y1 - 0.08, x1, y1), (x0, y0, x0 + 0.08, y1), (x1 - 0.08, y0, x1, y1)):
        fl.boxc(a, b, 0.003, c, d, 0.005, yel)
fl.finish(obstacle=False)

# ================= 組裝線 =================
F.nacelle_assembly(S, ST[0], CY, 0, stage=1, name="Nacelle_Stage1")
F.nacelle_assembly(S, ST[1], CY, 0, stage=2, generator=False, name="Nacelle_Stage2")
F.nacelle_assembly(S, ST[2], CY, 0, stage=3, name="Nacelle_Stage3")

# 天車：大車停在第 2 站後段上方，正把發電機落到機座上
CRANE_X, CRANE_Y = ST[1] - 1.5, CY
F.bridge_crane(S, CRANE_X, CRANE_Y, 0.5, 11.5, hook_z=2.0, load="generator", name="Crane")
S.anchor("STAND", "crane", CRANE_X - 0.2, CY + 1.75, 180)

# 附輪工作平台（第 2 站北側、第 3 站南側）＋高架站位（z = 平台高度）
F.rolling_platform(S, ST[1] + 0.6, CY + 1.45, PI, name="WorkPlatform_01")
S.anchor("STAND", "platform", ST[1] + 0.35, CY + 1.45, 180, z=0.8)
F.rolling_platform(S, ST[2] - 0.4, CY - 1.45, 0, name="WorkPlatform_02")
S.anchor("STAND", "platform", ST[2] - 0.15, CY - 1.45, 0, z=0.8)

# 各站地面站位
for (dx, dy, yw) in ((-1.0, -1.4, 0), (1.0, -1.4, 0), (-1.0, 1.4, 180), (1.0, 1.4, 180)):      # 第 1 站
    S.anchor("STAND", "assembly", ST[0] + dx, CY + dy, yw)
for (dx, dy, yw) in ((-1.0, -1.4, 0), (1.0, -1.4, 0), (2.6, 0.0, 90)):                         # 第 2 站
    S.anchor("STAND", "assembly", ST[1] + dx, CY + dy, yw)
for (dx, dy, yw) in ((-1.0, 1.4, 180), (1.0, 1.4, 180), (1.3, -1.4, 0)):                       # 第 3 站
    S.anchor("STAND", "assembly", ST[2] + dx, CY + dy, yw)
S.anchor("STAND", "inspection", ST[2] + 2.55, CY, 90)

# 東牆：出貨捲門與控制盒
F.dock_door(S, 17.8, CY, R(90), w=3.0, h=2.6, name="ShippingDoor")
F.dock_control(S, 17.8, 8.1, R(90), name="ShippingDoorControl")
S.anchor("POI", "shippingdoor", 17.2, 8.1, -90)
F.fire_extinguisher(S, 17.62, 3.6, name="Extinguisher_E")

# ================= 南牆：工具與次組裝 =================
for i, tx in enumerate((1.2, 2.2)):
    F.tool_chest(S, tx, 0.5, PI, color=((0.70, 0.14, 0.12), (0.12, 0.30, 0.62))[i], name="ToolChest_%02d" % (i + 1))
S.anchor("POI", "tools", 1.7, 1.35, 180)
for i, bx in enumerate((4.2, 6.3)):
    F.vise_bench(S, bx, 0.6, PI, name="SubAssemblyBench_%02d" % (i + 1))
    S.anchor("STAND", "bench", bx, 1.5, 180)
for i, cx in enumerate((10.6, 11.5)):
    F.ups_cabinet(S, cx, 0.62, PI, name="ControlCabinet_%02d" % (i + 1))
S.anchor("STAND", "wiring", 11.05, 1.6, 180)
for i, rx in enumerate((12.9, 14.0)):
    F.cable_reel(S, rx, 0.85, 0, name="CableReel_%02d" % (i + 1))
S.anchor("POI", "cable", 13.45, 1.8, 180)
F.tote_shelf(S, 15.5, 0.47, PI, name="BoltShelf")
S.anchor("POI", "bolts", 15.5, 1.3, 180)
F.torque_cart(S, 16.9, 0.9, PI, name="TorqueCart_01")
S.anchor("POI", "torque", 16.9, 1.7, 180)
F.torque_cart(S, 5.9, CY - 1.55, R(20), name="TorqueCart_02")

# ================= 北牆：大件備料區、看板、領班桌 =================
F.desk(S, 1.5, 11.35, 0, name="ForemanDesk")
F.monitor(S, 1.5, 11.5, 0, name="ForemanMonitor")
F.keyboard(S, 1.5, 11.2, 0, name="ForemanKeyboard")
F.chair(S, 1.5, 10.65, 0, name="ForemanChair")
S.anchor("SEAT", "desk", 1.5, 10.65, 0)
F.whiteboard(S, 0.2, 8.6, R(90), w=2.0, name="Whiteboard_W")
S.anchor("STAND", "whiteboard", 1.0, 8.6, 90)

F.hub_on_stand(S, 4.0, 10.75, name="RotorHub")
S.anchor("POI", "hub", 4.0, 9.55, 0)
F.component_pallet(S, 6.2, 10.95, 0, kind="gearbox", name="Kit_Gearbox")
F.component_pallet(S, 8.0, 10.95, 0, kind="generator", name="Kit_Generator")
S.anchor("POI", "kitting", 7.1, 9.95, 0)
F.component_pallet(S, 10.4, 11.0, 0, kind="shaft", name="Kit_MainShaft")
S.anchor("POI", "kitting", 10.4, 10.05, 0)
F.pallet(S, 12.6, 11.05, 0, name="Kit_SmallParts")
F.screen_wall(S, 12.6, 11.8, 1.8, h=1.0, yaw=0, z=1.35, name="ProductionBoard")
S.anchor("STAND", "board", 12.6, 10.05, 0)
F.component_pallet(S, 16.75, 10.5, R(90), kind="cover", name="Kit_CoverPanels")
S.anchor("POI", "cover", 15.8, 10.3, -90)
F.waste_bin(S, 0.55, 5.0, name="WasteBin")

# ---- 狀態：三站落地燈柱（紅黃綠）、領班桌／次組裝／配線／備料燈柱、天車主樑下方狀態燈
lits = ("green", "yellow", "green")
for k, cx in enumerate(ST):
    S.anchor("STATUS", "", cx + 1.75, CY + 1.25, n=k + 1)
    F.beacon_post(S, cx + 1.75, CY + 1.25, lit=lits[k], name="StationBeacon_%02d" % (k + 1))
k = 3
for (sx, sy, lit) in ((0.55, 11.3, "green"), (5.25, 0.45, "green"), (12.2, 0.5, "yellow"), (7.1, 11.3, "green")):
    k += 1
    S.anchor("STATUS", "", sx, sy, n=k)
    F.beacon_post(S, sx, sy, lit=lit, name="AreaBeacon_%02d" % k)
S.anchor("STATUS", "", CRANE_X, CY + 2.6, n=8, z=2.3)
F.status_lamp(S, CRANE_X, CY + 2.6, z=2.47, name="CraneStatusLamp", color=(0.95, 0.75, 0.1))

# ---- scene.json 額外欄位：天車可動範圍（供程式做動畫）與組裝站
S.extra_json["crane"] = {
    "desc": "懸掛式單樑天車：CraneBridge 沿 X 移動、CraneTrolley 沿 Y 移動（需與 Bridge 同步 X），吊鉤垂直升降",
    "objects": {"runway": "CraneRunway", "bridge": "CraneBridge", "trolley": "CraneTrolley"},
    "bridge_x_m": CRANE_X, "trolley_y_m": CRANE_Y,
    "bridge_x_range_m": [1.0, 17.0], "trolley_y_range_m": [1.2, 10.8],
    "hook_z_m": 2.0, "hook_z_range_m": [0.6, 2.0], "load": "generator",
    "operator_anchor": "STAND_crane_01", "status_anchor": "STATUS_08",
}
S.extra_json["stations"] = [
    {"id": "ST1", "name_zh": "主機架／偏航系統", "center": [ST[0], CY], "object": "Nacelle_Stage1", "status_anchor": "STATUS_01",
     "anchors": ["STAND_assembly_%02d" % i for i in (1, 2, 3, 4)]},
    {"id": "ST2", "name_zh": "傳動鏈（主軸、齒輪箱、發電機）", "center": [ST[1], CY], "object": "Nacelle_Stage2", "status_anchor": "STATUS_02",
     "anchors": ["STAND_assembly_%02d" % i for i in (5, 6, 7)] + ["STAND_platform_01", "STAND_crane_01"]},
    {"id": "ST3", "name_zh": "機艙罩／出廠檢驗", "center": [ST[2], CY], "object": "Nacelle_Stage3", "status_anchor": "STATUS_03",
     "anchors": ["STAND_assembly_%02d" % i for i in (8, 9, 10)] + ["STAND_platform_02", "STAND_inspection_01"]},
]

S.scene.view_settings.exposure = -0.5
S.finish(HERE)
