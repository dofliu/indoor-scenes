"""通用家具／設備產生器（無任何品牌、商標）。
所有函式的 (x, y) 為家具中心、yaw 為弧度（Blender Z 旋轉；0 = 正面朝 +Y）。
「正面」定義：椅子面向 +Y 時人坐的方向；桌子的「使用者側」在 -Y 側（人坐在桌子南側，面向北）。
"""
import math
import bpy
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


def _world_rect(x, y, yaw, lx0, ly0, lx1, ly1):
    """piece 區域矩形 → 世界座標軸對齊矩形（yaw 限 90° 倍數）。"""
    c, s = round(math.cos(yaw)), round(math.sin(yaw))
    pts = [(x + lx * c - ly * s, y + lx * s + ly * c) for lx in (lx0, lx1) for ly in (ly0, ly1)]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def phone_booth(S, x, y, yaw=0.0, w=1.3, d=1.4, h=2.1, color="fabric_teal", name="PhoneBooth"):
    """單人電話亭（隔音艙）：背板＋兩側吸音板＋前方玻璃（右側留 0.7 m 入口）＋頂板（內嵌燈）＋窄桌＋椅。
    yaw=0 時入口朝 -Y（南）、桌在 +Y 側；使用者坐在中心面向 +Y。
    回傳 dict：seat=(x,y)、status=(x,y,z)。導航：面板各自為障礙，入口到座位強制可走。"""
    t = 0.05
    glass = mat("glass_booth", (0.65, 0.82, 0.9), rough=0.05, alpha=0.3)
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, d / 2 - t / 2, h / 2, w, t, h, color)                       # 背板
    for sx in (-1, 1):                                                   # 側板
        p.box(sx * (w / 2 - t / 2), 0, h / 2, t, d, h, color)
    p.box(0, 0, h + 0.02, w, d, 0.04, "plastic_white")                   # 頂板
    p.box(0, 0, h - 0.005, w * 0.5, d * 0.4, 0.01, mat("light_emit", (1, 0.97, 0.9), emit=(1, 0.95, 0.85)))
    p.box(0, 0, 0.02, w - 2 * t, d - t, 0.04, "floor_wood")               # 艙內地台
    gx0, gx1 = -w / 2 + t, w / 2 - t - 0.72                               # 前方玻璃段
    p.box((gx0 + gx1) / 2, -d / 2 + 0.02, h / 2, gx1 - gx0, 0.02, h, glass)
    p.box(gx1 + 0.02, -d / 2 + 0.02, h / 2, 0.04, 0.05, h, "frame")       # 入口門框
    p.box((gx1 + w / 2 - t) / 2 + 0.01, -d / 2 + 0.02, h - 0.03, w / 2 - t - gx1, 0.05, 0.06, "frame")
    # 內側吸音格板（背板）
    for k in range(3):
        p.box(-0.35 + 0.35 * k, d / 2 - t - 0.01, 1.55, 0.3, 0.02, 0.5, "fabric_grey")
    # 窄桌（貼背板）
    p.box(0, d / 2 - t - 0.2, 0.74, w - 2 * t, 0.4, 0.03, "wood_light")
    p.box(0, d / 2 - t - 0.02, 0.37, w - 2 * t - 0.1, 0.02, 0.7, "desk_leg")
    p.finish(obstacle=False)
    # 障礙：背板+桌、兩側板、玻璃段
    c, s = math.cos(yaw), math.sin(yaw)

    def obs(lx, ly, ow, od):
        S.obstacles.append((x + lx * c - ly * s, y + lx * s + ly * c, yaw, ow, od))
    obs(0, d / 2 - 0.225, w, 0.45)
    for sx in (-1, 1):
        obs(sx * (w / 2 - t / 2), 0, t, d)
    obs((gx0 + gx1) / 2, -d / 2 + 0.02, gx1 - gx0, 0.04)
    # 入口 → 座位強制可走
    S.extra_free.append(_world_rect(x, y, yaw, -0.25, -d / 2 - 0.45, 0.5, 0.05))
    chair(S, x - (-0.05) * s, y + (-0.05) * c, yaw, color="chair_green", name=name + "_Chair")
    # 艙內小燈（區域光）
    ld = bpy.data.lights.new(name + "_Light", "AREA")
    ld.energy, ld.size = 25, 0.5
    lo = bpy.data.objects.new(name + "_Light", ld)
    lo.location = (x, y, h - 0.05)
    S.coll["LIGHTS"].objects.link(lo)
    return {"seat": (x - (-0.05) * s, y + (-0.05) * c), "status": (x, y, h + 0.2)}
