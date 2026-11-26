"""場景 020：無塵室（含更衣緩衝區：換鞋→跨越凳→更衣→風淋室→潔淨區）。執行：python3.13 build.py"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("020", "cleanroom", "無塵室（含更衣緩衝區）", "Cleanroom with Gowning Buffer", "factory", (14, 10),
          tags=["factory", "cleanroom", "gowning", "air-shower", "pass-box", "wet-bench", "laminar-bench", "ffu"])
R = math.radians
PI = math.pi
PX = 4.0          # 隔間牆中心線（西側 = 更衣緩衝區，東側 = 潔淨區）
ASY = 8.4         # 風淋室中心 y

# ---- 結構：西 1（人員入口，進更衣區）、東 5 與南 13（潔淨區逃生／物流門）
S.add_door("W", 1)
S.add_door("E", 5)
S.add_door("S", 13)
F.mat("floor_clean", (0.42, 0.50, 0.53), rough=0.35)
S.build_shell(floor="floor_clean", wall="wall")

# 隔間牆：腰牆＋大面玻璃觀景窗；風淋室穿牆處留素開口
F.interior_wall(S, PX, 0.2, PX, 9.8, glass=(0.95, 2.5), doors=[(ASY - 0.7 - 0.2, ASY + 0.7 - 0.2, 2.35)], name="Partition")

# 更衣區地坪分色：髒區（深）／更衣區（中）
fl = Piece(S, "GowningFloor", coll="STRUCTURE")
fl.boxc(0.2, 0.2, 0.0005, PX - 0.06, 3.6, 0.003, F.mat("floor_dirty", (0.33, 0.38, 0.44), rough=0.5))
fl.boxc(0.2, 3.6, 0.0005, PX - 0.06, 9.8, 0.003, F.mat("floor_gown", (0.44, 0.52, 0.56), rough=0.4))
fl.finish(obstacle=False)

# ---- 照明：更衣區燈板；潔淨區天花板 FFU 棋盤＋燈板
for (lx, ly) in ((2.0, 1.8), (2.0, 5.4), (1.4, 8.6)):
    S.ceiling_panel(lx, ly, power=45)
for i in range(7):
    for j in range(8):
        cx, cy = 5.2 + 1.2 * i, 0.9 + 1.2 * j
        if (i + j) % 2 == 0:
            F.ffu(S, cx, cy, light=False)
        elif i % 2 == 1 and j % 2 == 0:
            S.ceiling_panel(cx, cy, power=20)

# ================= 更衣緩衝區（西側） =================
F.sticky_mat(S, 0.95, 1.0, w=0.9, d=1.2, name="StickyMat_Entry")
for i, lx in enumerate((2.45, 3.35)):
    F.cabinet(S, lx, 0.425, PI, w=0.9, h=1.8, name="Locker_%02d" % (i + 1))
S.anchor("POI", "locker", 2.9, 1.25, 180)
F.shoe_rack(S, PX - 0.06 - 0.185, 2.5, R(-90), name="ShoeRack")
S.anchor("POI", "shoes", 3.05, 2.5, -90)
F.stepover_bench(S, 1.4, 3.6, 0, w=2.4, name="StepOverBench")
for sx in (0.9, 1.9):
    S.anchor("SEAT", "bench", sx, 3.7, 0)
F.floor_line(S, 2.6, 3.6, PX - 0.06, 3.6, width=0.1, name="CleanLine")

F.hand_dryer(S, 0.2, 4.35, R(90), name="HandDryer")
F.kitchen_counter(S, PX - 0.06 - 0.3, 5.0, R(-90), w=1.2, d=0.6, name="WashCounter", top="desk_white", body="cabinet")
F.sink(S, PX - 0.06 - 0.3, 5.0, R(-90), z=0.9, name="WashSink")
S.anchor("POI", "handwash", 2.75, 5.0, -90)
F.coat_rail(S, 0.2, 5.75, R(90), n=5, stand=False, name="GarmentRail")
S.anchor("POI", "garment", 0.9, 5.75, 90)
F.ppe_dispenser(S, 0.2, 7.3, R(90), name="PPEDispenser")
S.anchor("POI", "ppe", 0.9, 7.3, 90)
F.wall_mirror(S, 1.0, 9.8, 0, name="Mirror")
S.anchor("STAND", "mirror", 1.0, 9.0, 0)
F.waste_bin(S, 0.5, 8.3, name="WasteBin_Gown")

# 傳遞箱（嵌在隔間牆）
F.pass_box(S, PX, 6.3, R(90), name="PassBox")
S.anchor("POI", "passbox", 3.3, 6.3, -90, n=1)
S.anchor("POI", "passbox", 4.7, 6.3, 90, n=2)

# 風淋室（東西向穿過隔間牆）
F.air_shower(S, PX, ASY, 0, length=2.8, w=1.4, name="AirShower")
S.anchor("STAND", "airshower", PX, ASY, -90)
F.sticky_mat(S, 6.0, ASY, w=0.9, d=1.0, name="StickyMat_Clean")

# ================= 潔淨區（東側） =================
# 北牆機台：濕製程檯、封閉式機台、烘箱
tools = []
F.cleanroom_tool(S, 7.6, 9.25, 0, w=2.0, kind="wet", name="WetBench_01");            tools.append((7.6, 9.25, 2.0, 0))
S.anchor("STAND", "wetbench", 7.6, 8.35, 0, n=1)
F.cleanroom_tool(S, 10.0, 9.25, 0, w=2.0, kind="tool", lit="yellow", name="ProcessTool_01"); tools.append((10.0, 9.25, 2.0, 0))
S.anchor("STAND", "machine", 10.0, 8.35, 0, n=1)
F.cleanroom_tool(S, 12.1, 9.25, 0, w=1.6, kind="oven", name="Oven_01");              tools.append((12.1, 9.25, 1.6, 0))
S.anchor("STAND", "machine", 12.1, 8.35, 0, n=2)
# 南牆：線架 ×2、封閉式機台、濕製程檯
for i, sx in enumerate((5.1, 6.4)):
    F.wire_shelf(S, sx, 0.47, PI, seed=i, name="WireShelf_%02d" % (i + 1))
S.anchor("POI", "storage", 5.75, 1.25, 180)
F.cleanroom_tool(S, 8.6, 0.75, PI, w=2.0, kind="tool", name="ProcessTool_02");       tools.append((8.6, 0.75, 2.0, PI))
S.anchor("STAND", "machine", 8.6, 1.65, 180, n=3)
F.cleanroom_tool(S, 10.9, 0.75, PI, w=2.0, kind="wet", name="WetBench_02");          tools.append((10.9, 0.75, 2.0, PI))
S.anchor("STAND", "wetbench", 10.9, 1.65, 180, n=2)

# 中央 A 島：潔淨工作台（層流罩）背對背 ×2，高腳凳坐姿
F.laminar_bench(S, 7.6, 5.0, 0, name="CleanBench_01")
F.laminar_bench(S, 7.6, 5.8, PI, name="CleanBench_02")
F.microscope(S, 7.3, 5.0, 0, z=0.88, name="Microscope_CB1")
F.microscope(S, 7.9, 5.8, PI, z=0.88, name="Microscope_CB2")
F.stool(S, 7.6, 4.15, h=0.62, color="plastic_white", name="CleanStool_01")
S.anchor("SEAT", "cleanbench", 7.6, 4.15, 0, n=1)
F.stool(S, 7.6, 6.65, h=0.62, color="plastic_white", name="CleanStool_02")
S.anchor("SEAT", "cleanbench", 7.6, 6.65, 180, n=2)

# 中央 B 島：不鏽鋼工作桌（檢包／分片），四個站位
BX, BY = 10.7, 5.4
F.stainless_table(S, BX, BY, 0, w=2.2, d=0.9, name="WorkTable")
tb = Piece(S, "WorkTableItems", BX, BY, 0.85, coll="PROPS")
F.wafer_box(tb, -0.75, 0.15, 0)
F.wafer_box(tb, -0.4, 0.15, 0, (0.55, 0.75, 0.90))
F.wafer_box(tb, 0.75, -0.12, 0, (0.95, 0.60, 0.45))
tb.box(0.2, 0.1, 0.03, 0.5, 0.36, 0.06, "plastic_white")
tb.finish(obstacle=False)
F.laptop(S, BX + 0.1, BY - 0.25, 0, z=0.85, name="Laptop_Table")
n = 0
for (dx, dy, yw) in ((-0.6, -0.8, 0), (0.6, -0.8, 0), (-0.6, 0.8, 180), (0.6, 0.8, 180)):
    n += 1
    S.anchor("STAND", "table", BX + dx, BY + dy, yw, n=n)

# 東牆：檢驗工位 ×2（顯微鏡＋螢幕）、洗眼器、滅火器
for i, yy in enumerate((2.6, 7.3)):
    F.stainless_table(S, 13.45, yy, R(90), w=1.4, d=0.7, h=0.76, name="InspectTable_%02d" % (i + 1))
    F.monitor(S, 13.55, yy + 0.3, R(-90), z=0.76, name="InspectMonitor_%02d" % (i + 1))
    F.microscope(S, 13.4, yy - 0.25, R(-90), z=0.76, name="InspectScope_%02d" % (i + 1))
    F.keyboard(S, 13.3, yy + 0.3, R(-90), z=0.76, name="InspectKeyboard_%02d" % (i + 1))
    F.stool(S, 12.7, yy, h=0.5, color="plastic_white", name="InspectStool_%02d" % (i + 1))
    S.anchor("SEAT", "inspect", 12.7, yy, -90, n=i + 1)
F.eyewash_station(S, 13.8, 6.1, R(-90), name="Eyewash")
F.fire_extinguisher(S, 13.62, 3.75, name="Extinguisher")
S.anchor("POI", "safety", 13.1, 6.1, -90)

# 西側（隔間牆旁）：推車、微粒計數器；吊掛環境監控看板；牆面低位回風口
F.cleanroom_cart(S, 4.65, 4.6, R(90), name="CleanCart_01")
F.cleanroom_cart(S, 4.65, 3.3, R(90), name="CleanCart_02")
S.anchor("POI", "cart", 5.3, 3.95, 90)
F.particle_counter(S, 4.55, 1.9, R(-90), name="ParticleCounter")
S.anchor("POI", "particle", 5.2, 1.9, 90)
F.hanging_display(S, 9.2, 7.4, 0, w=1.6, h=0.7, z=2.1, name="EnvMonitor")
S.anchor("POI", "monitor", 9.2, 6.9, 0)
F.return_grille(S, 5.9, 9.8, 0, w=0.9, name="ReturnGrille_N1")
F.return_grille(S, 13.3, 9.8, 0, w=0.8, name="ReturnGrille_N2")
F.return_grille(S, 13.8, 8.9, R(-90), w=1.0, name="ReturnGrille_E1")
F.return_grille(S, 13.8, 1.1, R(-90), w=1.0, name="ReturnGrille_E2")
F.return_grille(S, 12.15, 0.2, PI, w=0.5, name="ReturnGrille_S1")

# ---- 狀態：風淋室入口燈、5 台機台三色燈、兩座中島與兩個檢驗工位的垂吊燈
S.anchor("STATUS", "", PX - 1.45, ASY, n=1)
k = 1
for (tx, ty, tw, yw) in tools:
    k += 1
    sgn = 1 if yw == 0 else -1
    S.anchor("STATUS", "", tx + sgn * (tw / 2 - 0.14), ty + sgn * 0.35, n=k)
for (sx, sy) in ((7.6, 5.4), (BX, BY), (13.3, 2.6), (13.3, 7.3)):
    k += 1
    S.anchor("STATUS", "", sx, sy, n=k)
    F.pendant_status_lamp(S, sx, sy, z=2.2, name="StatusPendant_%02d" % k)

S.scene.view_settings.exposure = -0.9
S.finish(HERE)
