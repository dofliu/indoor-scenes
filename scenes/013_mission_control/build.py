"""場景 013：AI 代理人公司：任務控制中心（東牆大螢幕牆、3 排 ×3 監控工位、指揮台）。
執行：python3.13 build.py（需 pip install bpy）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("013", "mission_control", "AI 代理人公司：任務控制中心", "AI Agent Company: Mission Control", "office", (12, 8),
          tags=["ai-company", "mission-control", "video-wall", "console", "monitoring"])
R = math.radians
EAST = R(-90)   # 面向 +X（東，螢幕牆方向）

S.add_door("W", 5)      # 後方主入口
S.add_door("N", 5)      # 側門
S.build_shell(floor="floor_carpet", wall="wall", accent={"E": "wall_dark", "N": "wall_dark"})
S.light_grid(3, 2, power=70)

# ---- 東牆：4×2 拼接螢幕牆與站位
F.video_wall(S, 11.8, 4.0, EAST, cols=4, rows=2, tw=1.6, th=0.9, z=0.85)
S.anchor("STAND", "wall", 10.6, 2.8, -90, n=1)
S.anchor("STAND", "wall", 10.6, 5.2, -90, n=2)

# ---- 3 排 ×3 監控工位（面向東），每席上方垂吊狀態燈
n = 0
for r, cx in enumerate((9.1, 7.2, 5.3)):
    F.rug(S, cx - 0.45, 4.0, 1.7, 5.2, "rug_blue", name="RowRug_%d" % (r + 1))
    for cy in (2.4, 4.0, 5.6):
        n += 1
        F.control_console(S, cx, cy, EAST, name="Console_%02d" % n)
        F.chair(S, cx - 0.85, cy, EAST, color="chair_seat", name="ConsoleChair_%02d" % n)
        S.anchor("SEAT", "console", cx - 0.85, cy, -90, n=n)
        S.anchor("STATUS", "", cx - 0.3, cy, n=n)
        F.pendant_status_lamp(S, cx - 0.3, cy, z=2.2, name="StatusPendant_%02d" % n)

# ---- 指揮台（2 席，略寬、各 2 面螢幕）
for k, cy in enumerate((3.2, 4.8), 1):
    F.control_console(S, 3.2, cy, EAST, w=1.6, d=0.9, screens=2, name="CommandDesk_%02d" % k)
    F.chair(S, 2.3, cy, EAST, color="chair_red", name="CommandChair_%02d" % k)
    S.anchor("SEAT", "supervisor", 2.3, cy, -90, n=k)
S.anchor("STATUS", "", 2.9, 4.0, n=10)
F.pendant_status_lamp(S, 2.9, 4.0, z=2.2, name="StatusPendant_10", color=(0.95, 0.65, 0.1))

# ---- 北牆：輔助顯示幕
for k, sx in enumerate((7.2, 9.1), 1):
    F.screen_wall(S, sx, 7.8, 1.5, h=0.85, yaw=0, z=1.25, name="SideDisplay_N%d" % k)

# ---- 後方（西側）：白板、事務機、飲水機、植栽
F.whiteboard(S, 0.2, 2.6, R(90), w=2.2, name="Whiteboard_W")
S.anchor("STAND", "whiteboard", 0.95, 2.6, 90, n=1)
F.printer(S, 1.6, 0.2 + 0.36, R(180), name="Printer")
S.anchor("POI", "printer", 1.6, 1.45, 180, n=1)
F.cabinet(S, 2.75, 0.2 + 0.24, R(180), w=0.9, h=0.9, name="Credenza")
F.water_dispenser(S, 0.42, 6.5, R(90), name="WaterDispenser")
S.anchor("POI", "water", 1.15, 6.5, 90, n=1)
for (px, py) in ((0.65, 7.35), (0.65, 0.65), (11.3, 0.65), (11.3, 7.35)):
    F.plant(S, px, py)

# 控制室偏暗：壓低曝光讓螢幕與狀態燈突出、避免預覽過曝
S.scene.view_settings.exposure = -1.0
S.finish(HERE)
