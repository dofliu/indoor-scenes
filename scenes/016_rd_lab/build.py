"""場景 016：研發實驗室（中島工作台 ×2、儀器架、排氣櫃、3D 列印區、分析工位）。執行：python3.13 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("016", "rd_lab", "研發實驗室", "R&D Laboratory", "lab", (12, 8),
          tags=["lab", "r&d", "workbench", "instrument-rack", "fume-hood", "3d-printer", "prototyping"])
R = math.radians
PI = math.pi

# ---- 結構
S.add_door("W", 1)
S.add_door("S", 9)
S.add_door("N", 9)
S.add_window("N", 3, width=2.0)
S.add_window("E", 5.15, width=2.0)
S.add_window("S", 4, width=2.0)
F.mat("floor_lab", (0.36, 0.42, 0.47), rough=0.35)     # 灰藍色環氧樹脂地坪
S.build_shell(floor="floor_lab", wall="wall", accent={"E": "wall_accent"})
S.light_grid(3, 2, power=60)

# ---- 中島工作台 ×2（雙面使用；每側 3 個站位）
IY = 4.2
ISL = ((3.4, "A"), (7.6, "B"))
nb = 0
for ix, tag in ISL:
    F.lab_bench(S, ix, IY, 0, w=3.0, d=1.5, name="LabBench_" + tag)
for ix, tag in ISL:                       # 南側站位（面北）
    for dx in (-1.0, 0.0, 1.0):
        nb += 1
        S.anchor("STAND", "bench", ix + dx, IY - 1.2, 0, n=nb)
for dx in (-1.0, 0.0, 1.0):               # A 島北側站位（面南）
    nb += 1
    S.anchor("STAND", "bench", 3.4 + dx, IY + 1.2, 180, n=nb)
for i, dx in enumerate((-1.0, 0.0, 1.0)): # B 島北側：高腳凳坐姿工位（顯微鏡／精密組裝）
    F.stool(S, 7.6 + dx, IY + 1.05, h=0.65, color="fabric_teal", name="LabStool_%02d" % (i + 1))
    S.anchor("SEAT", "bench", 7.6 + dx, IY + 1.05, 180, n=i + 1)

# A 島：電子量測（示波器、電源、焊接台）
AX = 3.4
F.oscilloscope(S, AX - 1.0, IY - 0.32, 0, name="Scope_01")
F.bench_psu(S, AX - 0.55, IY - 0.32, 0, name="PSU_01")
F.soldering_station(S, AX + 0.0, IY - 0.3, 0, name="Solder_01")
F.laptop(S, AX + 1.0, IY - 0.42, 0, z=0.9, name="Laptop_A1")
F.oscilloscope(S, AX + 1.0, IY + 0.32, PI, name="Scope_02")
F.bench_psu(S, AX + 0.5, IY + 0.32, PI, name="PSU_02")
F.soldering_station(S, AX - 0.1, IY + 0.3, PI, name="Solder_02")
F.laptop(S, AX - 1.0, IY + 0.42, PI, z=0.9, name="Laptop_A2")
F.parts_bins(S, AX - 0.7, IY, 0, z=1.28, n=5, name="Bins_A1")
F.parts_bins(S, AX + 0.7, IY, PI, z=1.28, n=5, name="Bins_A2")
F.bottles(S, AX, IY, 0, z=1.6, n=6, gap=0.14, name="Bottles_A")

# B 島：原型組裝（桌上手臂、顯微鏡、量測）
BX = 7.6
F.desktop_robot_arm(S, BX - 1.0, IY - 0.3, PI, name="DesktopArm_01")
F.laptop(S, BX + 0.0, IY - 0.42, 0, z=0.9, name="Laptop_B1")
F.bench_psu(S, BX + 0.5, IY - 0.32, 0, name="PSU_03")
F.oscilloscope(S, BX + 1.0, IY - 0.32, 0, name="Scope_03")
for i, dx in enumerate((-1.0, 0.0, 1.0)):
    F.microscope(S, BX + dx, IY + 0.42, PI, name="Microscope_%02d" % (i + 1))
F.bottles(S, BX - 0.7, IY, 0, z=1.28, n=6, name="Bottles_B1")
F.parts_bins(S, BX + 0.7, IY, 0, z=1.28, n=5, name="Bins_B1")
F.bottles(S, BX + 0.3, IY, 0, z=1.6, n=5, gap=0.16, name="Bottles_B2")

# ---- 西牆：儀器架 ×3（西門在西南角，儀器架排在門北側）
for i, yy in enumerate((3.4, 4.7, 6.0)):
    F.instrument_rack(S, 0.47, yy, R(90), seed=i, name="InstrumentRack_%02d" % (i + 1))
    S.anchor("POI", "instrument", 1.25, yy, 90, n=i + 1)

# ---- 北牆：實驗檯＋水槽（窗下）、排氣櫃、藥品／耗材櫃
for i in range(4):
    F.kitchen_counter(S, 1.6 + 1.0 * i, 7.5, 0, w=1.0, d=0.6, name="WallBench_%d" % (i + 1), top="desk_white", body="cabinet")
F.sink(S, 4.6, 7.5, 0, z=0.9, name="LabSink")
S.anchor("STAND", "sink", 4.6, 6.7, 0, n=1)
F.bottles(S, 2.1, 7.6, 0, z=0.9, n=5, name="Bottles_N1")
F.microscope(S, 3.3, 7.5, 0, name="Microscope_N")
F.fume_hood(S, 6.5, 7.4, 0, name="FumeHood")
S.anchor("STAND", "hood", 6.5, 6.55, 0, n=1)
F.mat("safety_yellow", (0.92, 0.72, 0.08), rough=0.5)
F.cabinet(S, 10.45, 7.575, 0, w=0.9, h=1.9, color="safety_yellow", name="ChemCabinet")
F.cabinet(S, 11.35, 7.575, 0, w=0.9, h=1.9, name="SupplyCabinet")
S.anchor("POI", "storage", 10.45, 6.8, 0, n=1)

# ---- 東牆：白板（南段）、氣瓶、分析工位 ×2（窗前）
F.whiteboard(S, 11.8, 1.5, R(-90), w=1.6, name="Whiteboard_E")
S.anchor("STAND", "whiteboard", 11.1, 1.5, 90, n=1)
F.gas_cylinders(S, 11.6, 3.0, R(-90), n=2, name="GasCylinders")
for i, yy in enumerate((4.4, 5.9)):
    F.desk(S, 11.45, yy, R(-90), w=1.4, d=0.7, top="desk_white", name="AnalysisDesk_%02d" % (i + 1), panel=False)
    F.monitor(S, 11.55, yy + 0.25, R(-90), name="Monitor_%02d_a" % (i + 1))
    F.monitor(S, 11.55, yy - 0.3, R(-90), name="Monitor_%02d_b" % (i + 1))
    F.keyboard(S, 11.3, yy, R(-90), name="Keyboard_%02d" % (i + 1))
    F.chair(S, 10.65, yy, R(-90), name="AnalysisChair_%02d" % (i + 1))
    S.anchor("SEAT", "desk", 10.65, yy, -90, n=i + 1)

# ---- 南牆：衣架（實驗衣）、矮櫃、3D 列印台、洗眼器＋滅火器
F.coat_rail(S, 2.2, 0.2, PI, n=3, name="CoatRail")
S.anchor("POI", "labcoat", 2.2, 0.85, 180, n=1)
for i in range(2):
    F.cabinet(S, 3.55 + 0.9 * i, 0.425, PI, w=0.9, h=0.9, name="LowCabinet_%d" % (i + 1))
F.parts_bins(S, 4.0, 0.42, PI, z=0.9, n=6, name="Bins_S")
F.table(S, 6.2, 0.6, 0, w=2.0, d=0.7, top="desk_white", name="PrinterTable")
for i, px in enumerate((5.6, 6.2, 6.8)):
    F.printer3d(S, px, 0.58, PI, name="Printer3D_%02d" % (i + 1))
S.anchor("POI", "printer3d", 6.2, 1.4, 180, n=1)
F.eyewash_station(S, 7.75, 0.2, PI, name="Eyewash")
F.fire_extinguisher(S, 8.15, 0.32, name="Extinguisher")
S.anchor("POI", "safety", 7.75, 0.9, 180, n=1)

# ---- 狀態燈：兩座中島、兩個分析工位、排氣櫃
for i, (sx, sy) in enumerate(((3.4, IY), (7.6, IY), (11.3, 4.4), (11.3, 5.9), (6.5, 6.8))):
    S.anchor("STATUS", "", sx, sy, n=i + 1)
    F.pendant_status_lamp(S, sx, sy, z=2.2, name="StatusPendant_%02d" % (i + 1))

S.scene.view_settings.exposure = -0.5
S.finish(HERE)
