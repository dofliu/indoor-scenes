"""通用家具／設備產生器（無任何品牌、商標）。
所有函式的 (x, y) 為家具中心、yaw 為弧度（Blender Z 旋轉；0 = 正面朝 +Y）。
「正面」定義：椅子面向 +Y 時人坐的方向；桌子的「使用者側」在 -Y 側（人坐在桌子南側，面向北）。
"""
import math
from scenelib import Piece, mat, PALETTE

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


def sofa(S, x, y, yaw=0.0, w=2.0, d=0.9, color="fabric_grey", name="Sofa", fp=None):
    """沙發，坐向 +Y（yaw=0 背靠南側）。fp 可自訂導航障礙矩形 (w,d,ox,oy)，例如只擋椅背讓座位錨點貼近導航網格。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.2, w, d, 0.4, "metal_dark")
    p.box(0, 0.05, 0.43, w - 0.3, d - 0.2, 0.18, color)
    p.box(0, -d / 2 + 0.1, 0.65, w, 0.2, 0.5, color)
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.1), 0, 0.5, 0.2, d, 0.4, color)
    p.finish(footprint=fp or (w, d))
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


def armchair(S, x, y, yaw=0.0, color="fabric_orange", name="Armchair"):
    """單人扶手椅，坐向 +Y。不列為導航障礙（同辦公椅）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.cyl(sx * 0.28, sy * 0.26, 0.09, 0.02, 0.18, "wood_dark", seg=8)
    p.box(0, 0.02, 0.30, 0.70, 0.66, 0.24, color)
    p.box(0, -0.29, 0.62, 0.70, 0.12, 0.44, color)
    for sx in (-1, 1):
        p.box(sx * 0.31, 0.02, 0.50, 0.10, 0.62, 0.18, color)
    p.finish(obstacle=False)
    return p


def bench(S, x, y, yaw=0.0, w=1.2, d=0.45, color="fabric_teal", name="Bench", fp=None):
    """無靠背長凳，坐向 +Y。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.40, w, d, 0.10, color)
    p.box(0, 0, 0.33, w - 0.04, d - 0.04, 0.04, "wood_light")
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.08), 0, 0.155, 0.04, d - 0.08, 0.31, "metal_dark")
    p.finish(footprint=fp or (w, d))
    return p


def partition(S, x0, y0, x1, y1, gaps=(), glass=True, t=0.1, h=None, color="wall", door_h=2.2,
              name="Partition", leaves=()):
    """室內隔間牆（軸向）。(x0,y0)-(x1,y1) 為中心線兩端（須水平或垂直）。
    gaps=[(a,b),...]：沿軸的絕對座標區間留作門洞（高 door_h，上方仍封閉）。
    glass=True 為落地玻璃隔間（深色框＋霧面腰帶）；False 為實牆。
    leaves=[(hinge, dir, side)]：在門洞邊緣 hinge 處畫一片開啟 90° 的玻璃門扇，dir=+1/-1 表示往法線正/負向開。
    每個實體區段自動登記為導航障礙；門洞處加入強制可走矩形。"""
    h = h or S.H
    horiz = abs(y1 - y0) < 1e-6
    a0, a1 = (min(x0, x1), max(x0, x1)) if horiz else (min(y0, y1), max(y0, y1))
    c = y0 if horiz else x0
    gl = mat("glass", (0.6, 0.8, 0.9), rough=0.05, alpha=0.25)
    frost = mat("glass_frost", (0.85, 0.90, 0.92), rough=0.6, alpha=0.6)
    fr = "frame"
    p = Piece(S, name, coll="STRUCTURE")

    def B(u0, u1, z0, z1, m, tt=t):
        if horiz:
            p.boxc(u0, c - tt / 2, z0, u1, c + tt / 2, z1, m)
        else:
            p.boxc(c - tt / 2, u0, z0, c + tt / 2, u1, z1, m)

    gaps = sorted(gaps)
    segs, cur = [], a0
    for (a, b) in gaps:
        if a > cur:
            segs.append((cur, a))
        cur = b
    if cur < a1:
        segs.append((cur, a1))
    pw = 0.05
    for (u0, u1) in segs:
        if glass:
            B(u0, u0 + pw, 0, h, fr)
            B(u1 - pw, u1, 0, h, fr)
            B(u0 + pw, u1 - pw, 0, 0.08, fr)
            B(u0 + pw, u1 - pw, h - 0.06, h, fr)
            B(u0 + pw, u1 - pw, 0.08, 0.95, gl, 0.02)
            B(u0 + pw, u1 - pw, 0.95, 1.35, frost, 0.02)
            B(u0 + pw, u1 - pw, 1.35, h - 0.06, gl, 0.02)
            n = int((u1 - u0) / 1.3)
            for k in range(1, n + 1):  # 中間直框
                uu = u0 + (u1 - u0) * k / (n + 1)
                B(uu - 0.015, uu + 0.015, 0.08, h - 0.06, fr, t * 0.6)
        else:
            B(u0, u1, 0, h, color)
        um = (u0 + u1) / 2
        S.obstacles.append((um, c, 0.0, u1 - u0, t) if horiz else (c, um, 0.0, t, u1 - u0))
    for (a, b) in gaps:
        if glass:
            B(a, b, door_h, door_h + 0.05, fr)
            B(a, b, door_h + 0.05, h - 0.06, gl, 0.02)
            B(a, b, h - 0.06, h, fr)
        else:
            B(a, b, door_h, h, color)
        m, r = (a + b) / 2, 0.5
        S.extra_free.append((m - 0.25, c - r, m + 0.25, c + r) if horiz else (c - r, m - 0.25, c + r, m + 0.25))
    for (hinge, d) in leaves:
        lw = 0.85
        v0, v1 = (c, c + d * lw) if d > 0 else (c + d * lw, c)
        if horiz:
            p.boxc(hinge - 0.015, v0, 0.02, hinge + 0.015, v1, door_h, gl)
            p.boxc(hinge - 0.03, c + d * (lw - 0.12), 0.95, hinge + 0.03, c + d * (lw - 0.08), 1.15, "metal")
        else:
            p.boxc(v0, hinge - 0.015, 0.02, v1, hinge + 0.015, door_h, gl)
            p.boxc(c + d * (lw - 0.12), hinge - 0.03, 0.95, c + d * (lw - 0.08), hinge + 0.03, 1.15, "metal")
    p.finish(obstacle=False)
    return p


def phone_booth(S, x, y, yaw=0.0, w=1.1, d=1.1, h=2.25, color="fabric_teal", name="PhoneBooth"):
    """獨立式電話亭（隔音艙）。開口朝區域 -Y；內含靠背牆的小桌板與高腳凳。
    自動登記導航障礙，並加入「艙內→門口外」的強制可走通道。"""
    p = Piece(S, name, x, y, yaw=yaw)
    wt = 0.06
    shell = mat("booth_" + color, PALETTE.get(color), rough=0.85)
    inner = mat("booth_inner", (0.80, 0.80, 0.78), rough=0.9)
    gl = mat("glass", (0.6, 0.8, 0.9), rough=0.05, alpha=0.25)
    p.boxc(-w / 2, -d / 2, 0, w / 2, d / 2, 0.04, "metal_dark")                       # 底座
    p.boxc(-w / 2, -d / 2, h - 0.10, w / 2, d / 2, h, shell)                          # 頂蓋
    p.boxc(-w / 2, d / 2 - wt, 0.04, w / 2, d / 2, h - 0.10, shell)                   # 背牆
    p.boxc(-w / 2 + wt, d / 2 - wt - 0.02, 0.5, w / 2 - wt, d / 2 - wt, h - 0.2, inner)  # 內側吸音板
    for sx in (-1, 1):                                                               # 側牆：下實、上玻璃
        xa, xb = (sx * w / 2, sx * (w / 2 - wt))
        p.boxc(xa, -d / 2, 0.04, xb, d / 2 - wt, 0.95, shell)
        p.boxc(xa, -d / 2, 0.95, xb, -d / 2 + 0.06, h - 0.10, shell)
        p.boxc(xa, d / 2 - wt - 0.06, 0.95, xb, d / 2 - wt, h - 0.10, shell)
        p.boxc(xa, -d / 2, h - 0.30, xb, d / 2 - wt, h - 0.10, shell)
        xm = sx * (w / 2 - wt / 2)
        p.boxc(xm - 0.01, -d / 2 + 0.06, 0.95, xm + 0.01, d / 2 - wt - 0.06, h - 0.30, gl)
    p.boxc(-w / 2, -d / 2, h - 0.30, w / 2, -d / 2 + wt, h - 0.10, shell)             # 門楣
    p.boxc(-w / 2 + wt, -d / 2 + 0.02, 0.04, -w / 2 + 0.34, -d / 2 + 0.04, h - 0.30, gl)  # 固定玻璃片
    p.boxc(-w / 2 + wt, d / 2 - wt - 0.32, 1.00, w / 2 - wt, d / 2 - wt, 1.04, "wood_light")  # 桌板
    p.cyl(0.05, 0.05, 0.62, 0.17, 0.06, "fabric_grey", seg=16)                       # 高腳凳
    p.cyl(0.05, 0.05, 0.31, 0.025, 0.58, "metal_dark", seg=8)
    p.cyl(0.05, 0.05, 0.05, 0.16, 0.02, "metal_dark", seg=16)
    p.boxc(-0.2, -0.2, h - 0.115, 0.2, 0.2, h - 0.10, mat("light_emit", (1, 0.97, 0.9), emit=(1, 0.95, 0.85)))
    p.finish(footprint=(w, d))
    c, s = math.cos(yaw), math.sin(yaw)
    pts = [(x + lx * c - ly * s, y + lx * s + ly * c) for (lx, ly) in ((-0.25, -d / 2 - 0.5), (0.25, 0.15))]
    S.extra_free.append((min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts)))
    return p


def wall_tablet(S, x, y, yaw=0.0, z=1.25, name="BookingPanel"):
    """壁掛預約面板／小平板，正面朝 -Y（(x,y) 為背面中心）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, -0.012, 0.09, 0.26, 0.024, 0.18, "plastic_black")
    p.box(0, -0.025, 0.09, 0.23, 0.002, 0.15, mat("panel_glow", (0.05, 0.3, 0.2), emit=(0.1, 0.7, 0.4)))
    p.finish(obstacle=False)
    return p


def door_sign_lamp(S, x, y, yaw=0.0, z=2.38, color=(0.2, 0.9, 0.3), name="DoorLamp"):
    """門楣上方的使用中指示燈（搭配 STATUS 錨點），正面朝 -Y。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, -0.02, 0, 0.30, 0.04, 0.10, "metal_dark")
    p.box(0, -0.045, 0, 0.24, 0.012, 0.06, mat("status_" + "_".join("%d" % (c * 10) for c in color), color, emit=color))
    p.finish(obstacle=False)
    return p
