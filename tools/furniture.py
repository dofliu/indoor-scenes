"""通用家具／設備產生器（無任何品牌、商標）。
所有函式的 (x, y) 為家具中心、yaw 為弧度（Blender Z 旋轉；0 = 正面朝 +Y）。
「正面」定義：椅子面向 +Y 時人坐的方向；桌子的「使用者側」在 -Y 側（人坐在桌子南側，面向北）。
"""
import math
from scenelib import Piece, mat

R = math.radians


def desk(S, x, y, yaw=0.0, w=1.4, d=0.7, h=0.74, top="desk_top", name="Desk", panel=True):
    """辦公桌：桌面 + 兩側板 + 背板。使用者坐在 -Y 側。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h - 0.0125, w, d, 0.025, top)
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.02), 0, (h - 0.025) / 2, 0.03, d - 0.08, h - 0.025, "desk_leg")
    if panel:
        p.box(0, d / 2 - 0.05, h * 0.62, w - 0.08, 0.02, h * 0.5, "desk_leg")
    p.finish(footprint=(w, d))
    return p


def chair(S, x, y, yaw=0.0, color="chair_seat", name="Chair"):
    """辦公椅（五星腳）。人坐向 +Y（yaw=0）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.cyl(0, 0, 0.03, 0.30, 0.03, "metal_dark", seg=5)
    p.cyl(0, 0, 0.25, 0.03, 0.40, "metal_dark", seg=8)
    p.box(0, 0.02, 0.48, 0.46, 0.46, 0.07, color)
    p.box(0, -0.2, 0.78, 0.44, 0.07, 0.50, color)
    for sx in (-1, 1):
        p.box(sx * 0.25, 0.0, 0.62, 0.04, 0.30, 0.03, "metal_dark")
    p.finish(obstacle=False)
    return p


def monitor(S, x, y, yaw=0.0, sz=(0.56, 0.32), z=0.74, name="Monitor"):
    """桌上螢幕，螢幕面朝 -Y（面向坐在南側的人）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0, 0.01, 0.22, 0.16, 0.02, "metal_dark")
    p.box(0, 0.02, 0.10, 0.04, 0.04, 0.18, "metal_dark")
    p.box(0, 0.03, 0.17 + sz[1] / 2, sz[0], 0.025, sz[1], "plastic_black")
    p.box(0, 0.0165, 0.17 + sz[1] / 2, sz[0] - 0.03, 0.002, sz[1] - 0.03, mat("screen_glow", (0.05, 0.15, 0.3), emit=(0.08, 0.3, 0.6)))
    p.finish(obstacle=False)
    return p


def keyboard(S, x, y, yaw=0.0, z=0.74, name="Keyboard"):
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0, 0.01, 0.42, 0.14, 0.02, "plastic_white")
    p.box(0.3, 0, 0.008, 0.06, 0.10, 0.016, "plastic_black")
    p.finish(obstacle=False)
    return p


def laptop(S, x, y, yaw=0.0, z=0.74, name="Laptop"):
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0, 0.008, 0.32, 0.22, 0.016, "metal")
    p.box(0, 0.11, 0.115, 0.32, 0.012, 0.21, "metal_dark")
    p.finish(obstacle=False)
    return p


def divider(S, x, y, w, yaw=0.0, h0=0.74, h=0.45, name="Divider"):
    """桌面隔板（磨砂）。"""
    p = Piece(S, name, x, y, h0, yaw=yaw, coll="PROPS")
    p.box(0, 0, h / 2, w, 0.03, h, mat("divider_fabric", (0.55, 0.62, 0.68), rough=0.9))
    p.finish(obstacle=False)
    return p


def cabinet(S, x, y, yaw=0.0, w=0.9, d=0.45, h=1.8, color="cabinet", name="Cabinet", doors=True):
    """儲物櫃，正面朝 -Y 側（靠牆放置時 yaw 使背面貼牆）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, color)
    if doors:
        p.box(0, -d / 2 - 0.005, h / 2, 0.008, 0.01, h - 0.05, "metal_dark")
        for sx in (-1, 1):
            p.box(sx * 0.06, -d / 2 - 0.012, h * 0.5, 0.02, 0.02, 0.2, "metal")
    p.finish(footprint=(w, d))
    return p


def table(S, x, y, yaw=0.0, w=1.6, d=0.8, h=0.74, top="wood_light", leg="metal_dark", name="Table", obstacle=True):
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h - 0.02, w, d, 0.04, top)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box(sx * (w / 2 - 0.06), sy * (d / 2 - 0.06), (h - 0.04) / 2, 0.05, 0.05, h - 0.04, leg)
    p.finish(footprint=(w, d), obstacle=obstacle)
    return p


def round_table(S, x, y, r=0.5, h=1.05, top="wood_light", name="RoundTable"):
    p = Piece(S, name, x, y)
    p.cyl(0, 0, h - 0.02, r, 0.04, top, seg=28)
    p.cyl(0, 0, (h - 0.04) / 2, 0.04, h - 0.04, "metal_dark", seg=10)
    p.cyl(0, 0, 0.015, r * 0.5, 0.03, "metal_dark", seg=20)
    p.finish(footprint=(2 * r, 2 * r))
    return p


def whiteboard(S, x, y, yaw=0.0, w=2.4, h=1.2, z=0.9, name="Whiteboard"):
    """壁掛白板，正面朝 -Y（yaw=0 時貼北牆）。(x,y) 為背面中心。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, -0.015, h / 2, w, 0.03, h, "metal")
    p.box(0, -0.032, h / 2, w - 0.06, 0.005, h - 0.06, "whiteboard")
    p.box(0, -0.05, 0.02, w * 0.6, 0.05, 0.02, "metal")
    p.finish(obstacle=False)
    return p


def plant(S, x, y, h=1.1, name="Plant"):
    p = Piece(S, name, x, y, coll="PROPS")
    p.cyl(0, 0, 0.18, 0.2, 0.36, "pot", seg=16)
    p.cyl(0, 0, 0.37, 0.18, 0.02, "wood_dark", seg=16)
    p.cyl(0, 0, 0.37 + h * 0.3, 0.015, h * 0.6, "wood_dark", seg=6)
    p.sphere(0, 0, 0.37 + h * 0.7, 0.30, "leaf", 1, 1, 1.1, seg=10)
    p.sphere(0.12, 0.08, 0.37 + h * 0.5, 0.2, "leaf", seg=8)
    p.sphere(-0.12, -0.06, 0.37 + h * 0.55, 0.2, "leaf", seg=8)
    p.finish(footprint=(0.4, 0.4))
    return p


def printer(S, x, y, yaw=0.0, name="Printer"):
    """多功能影印機（落地型，操作面朝 -Y）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.45, 0.8, 0.65, 0.9, "plastic_white")
    p.box(0, 0, 0.93, 0.8, 0.65, 0.06, "metal")
    p.box(0, -0.2, 0.7, 0.3, 0.18, 0.02, "plastic_black")
    p.box(0, -0.33, 0.3, 0.6, 0.02, 0.04, "metal_dark")
    p.finish(footprint=(0.8, 0.65))
    return p


def water_dispenser(S, x, y, yaw=0.0, name="WaterDispenser"):
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.45, 0.32, 0.34, 0.9, "plastic_white")
    p.cyl(0, 0, 1.12, 0.14, 0.35, mat("water_blue", (0.5, 0.75, 0.95), rough=0.1, alpha=0.6), seg=16)
    p.box(0, -0.18, 0.8, 0.12, 0.02, 0.04, "panel_blue")
    p.finish(footprint=(0.34, 0.36))
    return p


def sofa(S, x, y, yaw=0.0, w=2.0, d=0.9, color="fabric_grey", name="Sofa"):
    """沙發，坐向 +Y（yaw=0 背靠南側）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.2, w, d, 0.4, "metal_dark")
    p.box(0, 0.05, 0.43, w - 0.3, d - 0.2, 0.18, color)
    p.box(0, -d / 2 + 0.1, 0.65, w, 0.2, 0.5, color)
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.1), 0, 0.5, 0.2, d, 0.4, color)
    p.finish(footprint=(w, d))
    return p


def rug(S, x, y, w, d, color="rug", name="Rug"):
    p = Piece(S, name, x, y, coll="PROPS")
    p.box(0, 0, 0.005, w, d, 0.01, mat(color, rough=0.95))
    p.finish(obstacle=False)
    return p


def screen_wall(S, x, y, w, h=1.6, yaw=0.0, z=0.8, name="ScreenWall"):
    """壁掛大螢幕。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, -0.03, h / 2, w, 0.06, h, "plastic_black")
    p.box(0, -0.062, h / 2, w - 0.08, 0.004, h - 0.08, mat("screen_glow", (0.05, 0.15, 0.3), emit=(0.08, 0.3, 0.6)))
    p.finish(obstacle=False)
    return p


def status_lamp(S, x, y, z=2.0, name="StatusLamp", color=(0.2, 0.9, 0.3)):
    """小型狀態燈座（吊在 STATUS 錨點下方）。"""
    p = Piece(S, name, x, y, z, coll="PROPS")
    p.cyl(0, 0, 0, 0.05, 0.04, "metal_dark", seg=12)
    p.sphere(0, 0, -0.06, 0.05, mat("status_" + "_".join("%d" % (c * 10) for c in color), color, emit=color), seg=10)
    p.finish(obstacle=False)
    return p


# ---------------------------------------------------------------- 003 起新增


def _local(x, y, yaw, lx, ly):
    """piece 區域座標 → 世界座標。"""
    c, s = math.cos(yaw), math.sin(yaw)
    return x + lx * c - ly * s, y + lx * s + ly * c


def glass_partition(S, x0, y0, x1, y1, gap=None, h=2.6, name="GlassPartition"):
    """軸向對齊的玻璃隔間（鋁框＋玻璃）。gap=(t0,t1)：沿隔間方向（自 x0/y0 起算的絕對座標）的門口開口。
    每段各自成為導航障礙。"""
    horiz = abs(y1 - y0) < 1e-6
    a, b = (min(x0, x1), max(x0, x1)) if horiz else (min(y0, y1), max(y0, y1))
    segs = [(a, b)] if not gap else [(a, gap[0]), (gap[1], b)]
    glass = mat("glass", (0.6, 0.8, 0.9), rough=0.05, alpha=0.25)
    frosted = mat("glass_frost", (0.85, 0.9, 0.92), rough=0.5, alpha=0.55)
    p = Piece(S, name, coll="FURNITURE")
    t = 0.05
    for (s0, s1) in segs:
        if s1 - s0 < 0.02:
            continue
        n = max(1, int(round((s1 - s0) / 1.0)))
        if horiz:
            yc = y0
            p.boxc(s0, yc - t / 2, 0, s1, yc + t / 2, 0.06, "frame")
            p.boxc(s0, yc - t / 2, h - 0.06, s1, yc + t / 2, h, "frame")
            p.boxc(s0, yc - 0.008, 0.06, s1, yc + 0.008, h - 0.06, glass)
            p.boxc(s0, yc - 0.01, 1.0, s1, yc + 0.01, 1.35, frosted)  # 防撞磨砂帶
            for k in range(n + 1):
                xx = s0 + (s1 - s0) * k / n
                p.box(xx, yc, h / 2, 0.04, t, h, "frame")
            S.obstacles.append(((s0 + s1) / 2, yc, 0.0, s1 - s0, t))
        else:
            xc = x0
            p.boxc(xc - t / 2, s0, 0, xc + t / 2, s1, 0.06, "frame")
            p.boxc(xc - t / 2, s0, h - 0.06, xc + t / 2, s1, h, "frame")
            p.boxc(xc - 0.008, s0, 0.06, xc + 0.008, s1, h - 0.06, glass)
            p.boxc(xc - 0.01, s0, 1.0, xc + 0.01, s1, 1.35, frosted)
            for k in range(n + 1):
                yy = s0 + (s1 - s0) * k / n
                p.box(xc, yy, h / 2, t, 0.04, h, "frame")
            S.obstacles.append((xc, (s0 + s1) / 2, 0.0, t, s1 - s0))
    if gap:  # 門口上方楣板
        if horiz:
            p.boxc(gap[0], y0 - t / 2, 2.2, gap[1], y0 + t / 2, h, "frame")
        else:
            p.boxc(x0 - t / 2, gap[0], 2.2, x0 + t / 2, gap[1], h, "frame")
    p.finish(obstacle=False)
    return p


def stool(S, x, y, h=0.46, color="fabric_teal", name="Stool"):
    p = Piece(S, name, x, y, coll="FURNITURE")
    p.cyl(0, 0, 0.015, 0.2, 0.03, "metal_dark", seg=16)
    p.cyl(0, 0, h / 2, 0.025, h, "metal_dark", seg=8)
    p.cyl(0, 0, h - 0.03, 0.19, 0.07, color, seg=18)
    p.finish(obstacle=False)
    return p


def phone_booth(S, x, y, yaw=0.0, w=1.05, d=1.2, h=2.1, felt="fabric_teal", hinge="L", open_deg=88, name="PhoneBooth"):
    """單人電話亭（獨立艙體）。門朝 -Y（yaw=0 時背靠北側），內有靠背面板桌、凳子、頂燈。
    回傳 (piece, 座位世界座標, 座位 yaw_deg)。整個艙體為導航障礙，並自動在門口內側開一條導航通道
    （S.extra_free）讓人物可走到座位附近。hinge：門扇鉸鏈側 "L"/"R"；open_deg：門扇開啟角度。"""
    p = Piece(S, name, x, y, yaw=yaw)
    wt = 0.07
    shell = "booth_shell"
    mat(shell, (0.74, 0.75, 0.74), rough=0.6)
    mat("felt_in", (0.28, 0.33, 0.36), rough=0.95)
    p.box(0, 0, 0.03, w, d, 0.06, "metal_dark")                          # 底座
    p.box(0, d / 2 - wt / 2, h / 2, w, wt, h, shell)                      # 背板
    p.box(0, d / 2 - wt - 0.01, 1.3, w - 2 * wt, 0.02, 1.6, felt)         # 內側吸音面
    for sx in (-1, 1):
        p.box(sx * (w / 2 - wt / 2), 0, h / 2, wt, d, h, shell)          # 側板
        p.box(sx * (w / 2 - wt - 0.01), 0.05, 1.3, 0.02, d - 0.3, 1.6, "felt_in")
    p.box(0, 0, h - 0.04, w, d, 0.08, shell)                              # 頂板
    p.box(0, 0, h - 0.09, w - 0.3, d - 0.4, 0.02, mat("light_emit", (1, 0.97, 0.9), emit=(1, 0.95, 0.85)))
    # 前框＋固定玻璃＋開啟的門扇
    glass = mat("glass", (0.6, 0.8, 0.9), rough=0.05, alpha=0.25)
    fy = -d / 2 + 0.02
    p.box(0, fy, h - 0.12, w, 0.04, 0.08, "frame")
    p.box(0, fy, 0.08, w, 0.04, 0.04, "frame")
    leaf = w - 2 * wt - 0.04
    hx = w / 2 - wt
    sg = 1 if hinge == "R" else -1          # 鉸鏈側：R=+X 側、L=-X 側
    a = math.radians(open_deg)              # 門扇向外（-Y）開啟角度
    dx, dy = -sg * math.cos(a), -math.sin(a)
    rz = math.atan2(dy, dx)
    cx, cy = sg * hx + dx * leaf / 2, fy + dy * leaf / 2
    p.box(cx, cy, h / 2 - 0.02, leaf, 0.02, h - 0.24, glass, rz=rz)
    p.box(cx, cy, h - 0.16, leaf, 0.03, 0.04, "frame", rz=rz)
    hx2, hy2 = sg * hx + dx * (leaf - 0.06), fy + dy * (leaf - 0.06)
    p.box(hx2, hy2, 1.05, 0.03, 0.03, 0.3, "metal", rz=rz)
    # 桌板與插座
    p.box(0, d / 2 - wt - 0.18, 0.74, w - 2 * wt, 0.36, 0.03, "wood_light")
    p.box(0.25, d / 2 - wt - 0.02, 0.85, 0.12, 0.01, 0.06, "plastic_black")
    p.finish(footprint=(w, d))
    stool(S, *_local(x, y, yaw, 0, -0.08), name=name + "_Stool")
    sx, sy = _local(x, y, yaw, 0, -0.08)
    # 門口導航通道（僅軸向 yaw 有效）：從艙門外 0.4 m 到座位前 0.15 m、寬 0.5 m
    xa, ya = _local(x, y, yaw, -0.25, -d / 2 - 0.4)
    xb, yb = _local(x, y, yaw, 0.25, -0.25)
    S.extra_free.append((min(xa, xb), min(ya, yb), max(xa, xb), max(ya, yb)))
    return p, (sx, sy), math.degrees(yaw)


def floor_lamp(S, x, y, h=1.6, name="FloorLamp"):
    p = Piece(S, name, x, y, coll="PROPS")
    p.cyl(0, 0, 0.015, 0.16, 0.03, "metal_dark", seg=16)
    p.cyl(0, 0, h / 2, 0.015, h, "metal_dark", seg=8)
    p.cyl(0, 0, h, 0.2, 0.25, mat("lamp_shade", (0.95, 0.9, 0.8), emit=(1.0, 0.85, 0.6)), seg=18, r2=0.14)
    p.finish(obstacle=False)
    return p


def acoustic_panels(S, x, y, yaw=0.0, n=3, w=0.6, hh=0.6, z=1.6, colors=("fabric_teal", "fabric_grey", "fabric_orange"),
                    name="AcousticPanels"):
    """壁掛吸音板組（背貼牆，正面朝 -Y；yaw 決定貼哪面牆）。(x,y) 為組中心背面。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    for i in range(n):
        ox = (i - (n - 1) / 2) * (w + 0.08)
        oz = 0.12 if i % 2 else -0.08
        p.box(ox, -0.025, oz, w, 0.05, hh, mat(colors[i % len(colors)], rough=0.95))
    p.finish(obstacle=False)
    return p


def wall_display(S, x, y, yaw=0.0, w=0.26, hh=0.18, z=1.35, name="BookingPanel", color=(0.2, 0.8, 0.4)):
    """門邊小型預約顯示面板（正面朝 -Y）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, -0.01, 0, w, 0.02, hh, "plastic_white")
    p.box(0, -0.021, 0.01, w - 0.04, 0.002, hh - 0.06, mat("screen_glow", (0.05, 0.15, 0.3), emit=(0.08, 0.3, 0.6)))
    p.box(0, -0.021, -hh / 2 + 0.02, w - 0.04, 0.003, 0.015, mat("status_ok", color, emit=color))
    p.finish(obstacle=False)
    return p
