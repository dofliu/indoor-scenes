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


def conference_table(S, x, y, yaw=0.0, w=4.0, d=1.4, h=0.74, top="wood_light", name="ConferenceTable"):
    """會議長桌：厚桌面 + 兩組實心桌腳 + 中央線盒。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h - 0.0275, w, d, 0.055, top)
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.5), 0, (h - 0.055) / 2, 0.08, d - 0.5, h - 0.055, "desk_leg")
        p.box(sx * (w / 2 - 0.5), 0, 0.02, 0.1, d - 0.3, 0.04, "desk_leg")
    p.box(0, 0, h + 0.005, 0.35, 0.22, 0.012, "plastic_black")
    p.finish(footprint=(w, d))
    return p


def projector_screen(S, x, y, yaw=0.0, w=3.0, h=1.7, z=0.9, name="ProjectorScreen"):
    """壁掛投影布幕（正面朝 -Y，yaw=0 時貼北牆；(x,y) 為背面中心）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, -0.02, h + 0.1, w + 0.1, 0.06, 0.08, "metal_dark")
    p.box(0, -0.03, h / 2 + 0.05, w, 0.01, h, mat("screen_white", (0.93, 0.94, 0.95), rough=0.9, emit=(0.5, 0.52, 0.55)))
    p.finish(obstacle=False)
    return p


def projector(S, x, y, z, yaw=0.0, name="Projector"):
    """吊掛式投影機（z 為機身中心高度），鏡頭朝 +Y（yaw=0）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.cyl(0, 0, (S.H - z) / 2, 0.025, S.H - z, "metal_dark", seg=8)
    p.box(0, 0, 0, 0.34, 0.28, 0.11, "plastic_white")
    p.cyl(0, 0.15, 0, 0.05, 0.05, "plastic_black", seg=14, axis="Y")
    p.finish(obstacle=False)
    return p


def credenza(S, x, y, yaw=0.0, w=1.8, d=0.45, h=0.8, name="Credenza"):
    """低矮邊櫃（正面朝 -Y，yaw=0）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, "wood_dark")
    p.box(0, 0, h + 0.015, w + 0.02, d + 0.02, 0.03, "wood_light")
    for i in (-1, 1):
        p.box(i * w * 0.25, -d / 2 - 0.005, h * 0.55, 0.02, 0.01, 0.2, "metal")
    p.finish(footprint=(w, d))
    return p
