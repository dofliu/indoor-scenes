"""場景 014：AI 代理人公司：代理人工作艙（北牆一排 8 個標準化工作艙，每艙背板頂端有狀態燈座）。
執行：python3 build.py（需 pip install bpy）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("014", "agent_pods", "AI 代理人公司：代理人工作艙", "AI Agent Company: Agent Work Pods", "office", (14, 6),
          tags=["ai-company", "agent-pod", "workstation", "status-lamp", "8-pods"])
R = math.radians

S.add_door("S", 3)
S.add_door("S", 11)
S.add_door("W", 3)
S.add_door("E", 3)
S.build_shell(floor="floor_carpet", wall="wall", accent={"N": "wall_dark"})
S.light_grid(4, 2, power=55)

# ---- 北牆：8 個標準化工作艙（寬 1.6 m、深 1.6 m，艙口朝南），兩種色帶交錯
POD_W, POD_D = 1.6, 1.6
X0 = (14 - 8 * POD_W) / 2
ACC = ((0.10, 0.50, 0.52), (0.88, 0.45, 0.15))
LAMPS = ((0.2, 0.9, 0.3), (0.2, 0.9, 0.3), (0.95, 0.65, 0.1), (0.2, 0.9, 0.3),
         (0.2, 0.55, 0.95), (0.2, 0.9, 0.3), (0.9, 0.2, 0.15), (0.2, 0.9, 0.3))
for i in range(8):
    n = i + 1
    cx, cy = X0 + POD_W * (i + 0.5), 6 - 0.2 - POD_D / 2
    _, seat, lamp = F.agent_pod(S, cx, cy, 0, w=POD_W, d=POD_D, accent=ACC[i % 2], lamp=LAMPS[i],
                                index=n, name="AgentPod_%02d" % n)
    F.chair(S, seat[0], seat[1], 0, color="chair_seat", name="PodChair_%02d" % n)
    S.anchor("SEAT", "pod", seat[0], seat[1], 0, n=n)
    S.anchor("STATUS", "", lamp[0], lamp[1], n=n)

# ---- 南牆中央：總覽狀態看板與站位
F.screen_wall(S, 7.0, 0.2, 3.0, h=1.3, yaw=R(180), z=1.05, name="OverviewBoard")
S.anchor("STAND", "overview", 7.0, 1.3, 180, n=1)

# ---- 中央走道：站立交接桌
F.rug(S, 7.0, 2.55, 3.2, 2.0, "rug_blue", name="HandoffRug")
F.round_table(S, 7.0, 2.55, r=0.5, name="HandoffTable")
F.laptop(S, 7.0, 2.55, R(90), z=1.05)
S.anchor("STAND", "handoff", 6.1, 2.55, -90, n=1)
S.anchor("STAND", "handoff", 7.9, 2.55, 90, n=2)

# ---- 南牆：補給矮櫃、事務機；西牆：飲水機；角落植栽
for k, cx in enumerate((4.75, 9.25), 1):
    F.cabinet(S, cx, 0.2 + 0.24, R(180), w=0.9, h=0.9, name="SupplyCabinet_%d" % k)
    S.anchor("POI", "supply", cx, 1.3, 180, n=k)
F.printer(S, 12.7, 0.2 + 0.36, R(180), name="Printer")
S.anchor("POI", "printer", 12.7, 1.45, 180, n=1)
F.water_dispenser(S, 0.42, 1.3, R(90), name="WaterDispenser")
S.anchor("POI", "water", 1.15, 1.3, 90, n=1)
for (px, py) in ((1.3, 0.65), (13.35, 4.05), (0.65, 4.05)):
    F.plant(S, px, py)

S.finish(HERE)
