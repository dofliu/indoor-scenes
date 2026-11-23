"""場景 020：無塵室（含更衣緩衝區）。西側 3.8 m 為更衣緩衝區（黏塵墊→鞋櫃→洗手→跨越椅→潔淨衣櫃→防護用品→全身鏡→風淋室），
東側 8 m 為潔淨作業區（濕式清洗台、製程機台 ×2、層流潔淨工作台 ×2、檢驗桌、晶圓盒儲存櫃）。
兩區以彩鋼板＋觀察玻璃隔間分隔，人員只能經風淋室進入，物料經傳遞箱。執行：python3.13 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("020", "cleanroom", "無塵室（含更衣緩衝區）", "Cleanroom with Gowning Room", "factory", (12, 10),
          tags=["factory", "cleanroom", "semiconductor", "gowning", "air-shower", "pass-box", "wet-bench",
                "process-tool", "laminar-flow", "iso-class"])
R = math.radians
PI = math.pi
PX = 4.0                      # 隔間中心線 x

# ---- 結構：南門（更衣區入口）、東門（潔淨區緊急出口）
S.add_door("S", 1)
S.add_door("E", 1)
F.mat("floor_vinyl_cr", (0.56, 0.64, 0.70), rough=0.35)          # 抗靜電 PVC 地板
S.build_shell(floor="floor_vinyl_cr", wall="cr_panel", accent=None)
F.mat("cr_panel", F.CR_WHITE, rough=0.35)
S.light_grid(4, 3, power=45)

# 潔淨區高架開孔地板（覆蓋層＋0.6 m 格線）
fl = Piece(S, "RaisedFloor", 0, 0, coll="STRUCTURE")
x0, x1, y0, y1 = PX + 0.05, S.W - 0.2, 0.2, S.D - 0.2
fl.boxc(x0, y0, 0.0, x1, y1, 0.006, F.mat("raised_floor", (0.72, 0.75, 0.78), rough=0.3))
gx = x0 + 0.6
while gx < x1 - 0.05:
    fl.boxc(gx - 0.006, y0, 0.006, gx + 0.006, y1, 0.008, "metal")
    gx += 0.6
gy = y0 + 0.6
while gy < y1 - 0.05:
    fl.boxc(x0, gy - 0.006, 0.006, x1, gy + 0.006, 0.008, "metal")
    gy += 0.6
fl.finish(obstacle=False)

# ---- 隔間（風淋室開口 y 7.3–8.7）＋風淋室＋傳遞箱
F.cleanroom_partition(S, PX, 0.2, PX, S.D - 0.2, gaps=[(7.3, 8.7)], name="CRPartition")
F.air_shower(S, PX, 8.0, R(-90), L=1.6, inner=1.0, name="AirShower")
S.extra_free.append((PX - 1.2, 7.5, PX + 1.2, 8.5))               # 風淋室通道（內寬 1.0 m）
F.pass_box(S, PX, 5.6, R(-90), name="PassBox")
F.pressure_gauge(S, PX - 0.05, 9.25, R(90), name="PressureGauge_W")
F.pressure_gauge(S, PX + 0.05, 9.25, R(-90), name="PressureGauge_E")

# ================= 更衣緩衝區（x 0.2–3.95） =================
F.sticky_mat(S, 1.0, 0.85, name="StickyMat_S")
S.anchor("POI", "stickymat", 1.0, 0.9, 0, n=1)
F.shoe_locker(S, 0.4, 2.6, R(-90), w=1.2, d=0.4, h=1.2, name="ShoeLocker")
S.anchor("POI", "shoelocker", 1.05, 2.6, 90, n=1)
F.hand_wash_station(S, PX - 0.05 - 0.275, 1.6, R(-90), name="HandWash")
S.anchor("STAND", "handwash", 3.0, 1.6, -90, n=1)
# 跨越椅（一般區／潔淨衣區分界）
F.step_over_bench(S, 1.4, 4.2, 0, w=2.2, d=0.45, name="StepOverBench")
S.anchor("SEAT", "bench", 0.9, 3.95, 180, n=1)
S.anchor("SEAT", "bench", 1.9, 3.95, 180, n=2)
# 潔淨衣櫃 ×2（西牆）、防護用品架與全身鏡（北牆）
for i, yy in enumerate((5.6, 7.1)):
    F.gown_cabinet(S, 0.2 + 0.325, yy, R(-90), w=1.4, d=0.65, name="GownCabinet_%02d" % (i + 1))
    S.anchor("POI", "gown", 1.4, yy, 90, n=i + 1)
F.ppe_dispenser(S, 1.3, S.D - 0.2, PI, z=1.0, name="PPEDispenser")
S.anchor("POI", "ppe", 1.3, 9.1, 0, n=1)
F.wall_mirror(S, 2.7, S.D - 0.2, PI, name="Mirror")
S.anchor("STAND", "mirror", 2.7, 9.1, 0, n=1)
# 風淋室入口／內部、傳遞箱兩側
S.anchor("POI", "airshower", 2.7, 8.0, -90, n=1)
S.anchor("STAND", "airshower", PX, 8.0, -90, n=1)
S.anchor("POI", "passbox", 3.1, 5.6, -90, n=1)
S.anchor("POI", "passbox", 4.9, 5.6, 90, n=2)

# ================= 潔淨作業區（x 4.05–11.8） =================
# 北牆：濕式清洗台、洗眼器、晶圓盒儲存櫃
F.wet_bench(S, 6.6, S.D - 0.2 - 0.5, 0, w=3.0, d=1.0, name="WetBench")
S.anchor("STAND", "wetbench", 6.0, 8.15, 0, n=1)
S.anchor("STAND", "wetbench", 7.2, 8.15, 0, n=2)
F.eyewash_station(S, 8.6, S.D - 0.2, 0, name="Eyewash")
S.anchor("POI", "safety", 8.6, 9.1, 0, n=1)
F.wafer_stocker(S, 10.6, S.D - 0.2 - 0.35, 0, w=1.8, d=0.7, name="WaferStocker")
S.anchor("POI", "stocker", 10.6, 8.6, 0, n=1)
F.return_air_grille(S, 4.6, S.D - 0.2, PI, w=0.7, name="ReturnGrille_N")
F.return_air_grille(S, S.W - 0.2, 8.2, R(90), w=1.2, name="ReturnGrille_E")

# 東牆：製程機台 ×2（載入埠朝西）
TX = S.W - 0.2 - 1.3
for i, (yy, lit, acc, nf) in enumerate(((6.4, "green", (0.10, 0.35, 0.60), 1), (3.6, "yellow", (0.10, 0.50, 0.52), 2))):
    F.process_tool(S, TX, yy, R(-90), w=1.8, d=2.6, lit=lit, accent=acc, foups=nf, name="ProcessTool_%02d" % (i + 1))
    S.anchor("STAND", "tool", 8.6, yy, -90, n=i + 1)

# 中央：檢驗桌（顯微鏡 ×2、高腳凳）
F.table(S, 6.6, 4.6, 0, w=2.0, d=0.9, h=0.9, top="desk_white", leg="metal", name="InspectionTable")
for i, xx in enumerate((6.1, 7.1)):
    F.microscope(S, xx, 4.45, 0, z=0.9, name="Microscope_%02d" % (i + 1))
    F.stool(S, xx, 3.95, h=0.65, color="fabric_teal", name="InspectStool_%02d" % (i + 1))
    S.anchor("SEAT", "inspect", xx, 3.95, 0, n=i + 1)
F.laptop(S, 6.6, 4.85, PI, z=0.9, name="Laptop_Inspect")

# 南牆：層流潔淨工作台 ×2（面北）、微粒計數器推車
for i, xx in enumerate((5.6, 7.3)):
    F.laminar_flow_bench(S, xx, 0.6, PI, w=1.5, d=0.8, name="CleanBench_%02d" % (i + 1))
    F.stool(S, xx, 1.4, h=0.65, color="chair_seat", name="CleanBenchStool_%02d" % (i + 1))
    S.anchor("SEAT", "cleanbench", xx, 1.4, 180, n=i + 1)
F.particle_counter_cart(S, 8.75, 0.55, PI, name="ParticleCounter")
S.anchor("POI", "particle", 8.75, 1.3, 180, n=1)

# 東門：緊急出口燈、滅火器
ex = Piece(S, "ExitSign_E", S.W - 0.2, 1.0, coll="PROPS")
ex.box(-0.03, 0, 2.42, 0.06, 0.36, 0.14, F.mat("exit_green", (0.1, 0.75, 0.3), emit=(0.1, 0.9, 0.35)))
ex.finish(obstacle=False)
F.fire_extinguisher(S, S.W - 0.4, 2.15, name="Extinguisher")

# 走道標線（潔淨區）
F.floor_line(S, 4.6, 7.0, 11.6, 7.0, name="WalkLine_N")
F.floor_line(S, 4.6, 2.2, 8.6, 2.2, name="WalkLine_S")

# ---- 狀態燈
for (sx, sy) in ((2.3, 6.6), (6.6, 8.15), (8.6, 6.4), (8.6, 3.6), (6.6, 3.95), (5.6, 1.4), (7.3, 1.4)):
    n = S.anchor("STATUS", "", sx, sy)
    F.pendant_status_lamp(S, sx, sy, z=2.2, name="StatusPendant_" + n.split("_")[1])

# ---- 額外欄位：分區與更衣路線
S.extra_json["zones"] = [
    {"id": "gowning", "name_zh": "更衣緩衝區", "rect_m": [0, 0, PX, S.D], "clean_class": "ISO 8",
     "pressure_pa": 10, "entry_doors": ["DOOR_S_01"]},
    {"id": "cleanroom", "name_zh": "潔淨作業區", "rect_m": [PX, 0, S.W, S.D], "clean_class": "ISO 6",
     "pressure_pa": 25, "entry_doors": ["DOOR_E_01"], "note": "DOOR_E_01 為緊急出口，正常進出須經風淋室"},
]
S.extra_json["routes"] = {
    "gowning": {"desc": "進入無塵室的標準更衣流程（依序經過）",
                "waypoints": ["POI_stickymat_01", "POI_shoelocker_01", "STAND_handwash_01", "SEAT_bench_01",
                              "POI_gown_01", "POI_ppe_01", "STAND_mirror_01", "POI_airshower_01",
                              "STAND_airshower_01"],
                "dwell_s": {"STAND_airshower_01": 15, "POI_gown_01": 60}},
    "material": {"desc": "物料傳遞（更衣區側放入、潔淨區側取出）",
                 "waypoints": ["POI_passbox_01", "POI_passbox_02"]},
}

S.scene.view_settings.exposure = -1.1
S.finish(HERE)
