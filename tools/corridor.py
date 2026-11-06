"""走廊連接模組產生器：寬 2 m 的走廊（直線 2×N）與 2×2 樞紐（L/T/十字）。
所有開口都是 1.0 m 門洞，位於牆面中心（2 m 寬走廊端面 offset=1），可與其他模組的奇數公尺門洞對齊。"""
import math
from scenelib import *
import furniture as F


def extinguisher(S, x, y, yaw_deg, name):
    """壁掛滅火器（小道具，無導航障礙）。(x,y) 為貼牆處，yaw 朝室內。"""
    p = Piece(S, name, x, y, coll="PROPS", yaw=math.radians(yaw_deg))
    p.cyl(0, 0.08, 1.0, 0.07, 0.4, mat("extinguisher", (0.75, 0.1, 0.08), rough=0.4), seg=12)
    p.box(0, 0.02, 1.0, 0.18, 0.02, 0.06, "metal_dark")
    p.finish(obstacle=False)


def exit_sign(S, x, y, z, yaw_deg, name):
    p = Piece(S, name, x, y, z, coll="PROPS", yaw=math.radians(yaw_deg))
    p.box(0, 0.02, 0, 0.36, 0.03, 0.12, mat("sign_green", (0.05, 0.5, 0.2), emit=(0.1, 0.8, 0.3)))
    p.finish(obstacle=False)


def build(sid, slug, zh, en, size, doors, tags):
    """doors: [(wall, offset), ...]"""
    S = Scene(sid, slug, zh, en, "connector", size, tags=["connector", "corridor"] + tags)
    for w, o in doors:
        S.add_door(w, o)
    S.build_shell(floor="floor_carpet", wall="wall")
    W, D = size
    long_x = W >= D
    L = max(W, D)
    # 天花板燈：每 4 m 一盞（至少一盞）
    n_l = max(1, L // 4)
    for i in range(n_l):
        t = L * (i + 0.5) / n_l
        x, y = (t, D / 2) if long_x else (W / 2, t)
        S.ceiling_panel(x, y, 1.0 if long_x else 0.5, 0.5 if long_x else 1.0, power=20)
    # 路徑點：沿中心線每 2 m 一個 POI_waypoint（供人物巡航）
    k = 0
    for i in range(L // 2):
        t = 1.0 + 2 * i
        x, y = (t, D / 2) if long_x else (W / 2, t)
        k += 1
        S.anchor("POI", "waypoint", x, y, 0, n=k)
    return S
