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


def sofa(S, x, y, yaw=0.0, w=2.0, d=0.9, color="fabric_grey", name="Sofa", seat_clear=False):
    """沙發，坐向 +Y（yaw=0 背靠南側）。seat_clear=True 時導航障礙只含靠背半部，讓坐下點貼近導航網格。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.2, w, d, 0.4, "metal_dark")
    p.box(0, 0.05, 0.43, w - 0.3, d - 0.2, 0.18, color)
    p.box(0, -d / 2 + 0.1, 0.65, w, 0.2, 0.5, color)
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.1), 0, 0.5, 0.2, d, 0.4, color)
    p.finish(footprint=(w, d / 2, 0, -d / 4) if seat_clear else (w, d))
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


def projector(S, x, y, z, yaw=0.0, name="Projector"):
    """吊掛式投影機（吊桿＋機身＋鏡頭，鏡頭朝 +Y 本地方向）。z 為天花板高度。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.cyl(0, 0, -0.1, 0.02, 0.2, "metal_dark", seg=8)
    p.box(0, 0, -0.24, 0.34, 0.26, 0.1, "plastic_white")
    p.cyl(0, 0.15, -0.24, 0.05, 0.06, "plastic_black", seg=12, axis="Y")
    p.finish(obstacle=False)
    return p


def projector_screen(S, x, y, w=2.8, h=1.75, z=0.95, name="ProjectorScreen"):
    """北牆吊掛式投影布幕，(x,y) 為牆內側面中心，正面朝 -Y。"""
    p = Piece(S, name, x, y, z, coll="PROPS")
    p.box(0, -0.04, h + 0.12, w + 0.1, 0.08, 0.08, "metal_dark")
    p.box(0, -0.045, h / 2 + 0.05, w, 0.01, h, "whiteboard")
    p.finish(obstacle=False)
    return p


def conference_table(S, x, y, yaw=0.0, w=4.0, d=1.4, h=0.74, name="ConferenceTable"):
    """會議長桌：厚桌面＋兩個寬腳座＋桌面中央線路盒與麥克風。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h - 0.03, w, d, 0.06, "wood_dark")
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.5), 0, (h - 0.06) / 2, 0.08, d - 0.4, h - 0.06, "metal_dark")
        p.box(sx * (w / 2 - 0.5), 0, 0.02, 0.1, d - 0.2, 0.04, "metal_dark")
    for sx in (-1.0, 0.0, 1.0):
        p.box(sx * w * 0.28, 0, h + 0.008, 0.16, 0.12, 0.016, "metal")
        p.cyl(sx * w * 0.28, 0.2, h + 0.03, 0.04, 0.06, "plastic_black", seg=12)
    p.finish(footprint=(w, d))
    return p


def glass_panel(S, x, y, w, yaw=0.0, h=2.1, name="GlassPanel"):
    """玻璃隔間板（含上下金屬框）。w 沿本地 X，厚 0.04；列為導航障礙。"""
    p = Piece(S, name, x, y, yaw=yaw, coll="PROPS")
    p.box(0, 0, h / 2, w, 0.01, h - 0.08, mat("glass_panel", (0.6, 0.8, 0.9), rough=0.05, alpha=0.25))
    p.box(0, 0, 0.02, w, 0.04, 0.04, "metal_dark")
    p.box(0, 0, h - 0.02, w, 0.04, 0.04, "metal_dark")
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.02), 0, h / 2, 0.04, 0.04, h, "metal_dark")
    p.finish(footprint=(w, 0.05))
    return p


def stool(S, x, y, h=0.65, color="fabric_orange", name="Stool"):
    p = Piece(S, name, x, y)
    p.cyl(0, 0, h - 0.04, 0.17, 0.08, color, seg=16)
    p.cyl(0, 0, h / 2 - 0.04, 0.025, h - 0.08, "metal_dark", seg=8)
    p.cyl(0, 0, 0.015, 0.16, 0.03, "metal_dark", seg=16)
    p.finish(obstacle=False)
    return p


def conference_chair(S, x, y, yaw=0.0, color="chair_seat", name="MeetChair"):
    """會議椅（四腳固定、無扶手）。人坐向 +Y（yaw=0）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box(sx * 0.2, sy * 0.19, 0.22, 0.035, 0.035, 0.44, "metal_dark")
    p.box(0, 0.0, 0.46, 0.46, 0.46, 0.07, color)
    p.box(0, -0.21, 0.74, 0.44, 0.06, 0.45, color)
    p.finish(obstacle=False)
    return p


def speakerphone(S, x, y, z=0.74, name="Speakerphone"):
    """桌面會議喇叭。"""
    p = Piece(S, name, x, y, z, coll="PROPS")
    p.cyl(0, 0, 0.02, 0.12, 0.04, "plastic_black", seg=20)
    p.cyl(0, 0, 0.042, 0.08, 0.004, "metal", seg=20)
    p.finish(obstacle=False)
    return p


# ---------------------------------------------------------------- 茶水間／廚房設備（場景 004 起）
def kitchen_counter(S, x, y, yaw=0.0, w=1.2, d=0.6, h=0.9, name="Counter", top="desk_white", body="wood_dark"):
    """廚房流理台（正面朝 -Y，yaw=0；背靠牆）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0.01, 0.05 + (h - 0.08) / 2, w, d - 0.02, h - 0.08, body)
    p.box(0, 0, h - 0.015, w + 0.01, d, 0.03, top)
    p.box(0, -d / 2 - 0.005, 0.05 + (h - 0.08) * 0.5, w - 0.04, 0.01, h - 0.1, "metal_dark")
    p.box(0, -d / 2 - 0.012, h * 0.7, w * 0.4, 0.012, 0.015, "metal")
    p.finish(footprint=(w, d))
    return p


def sink(S, x, y, yaw=0.0, z=0.9, name="Sink"):
    """檯面水槽＋水龍頭（置於流理台上方，z=檯面高度）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0, 0.002, 0.5, 0.38, 0.006, "metal")
    p.box(0, 0, 0.0005, 0.44, 0.32, 0.002, "metal_dark")
    p.cyl(0, 0.2, 0.15, 0.015, 0.3, "metal", seg=8)
    p.box(0, 0.12, 0.3, 0.02, 0.18, 0.02, "metal")
    p.finish(obstacle=False)
    return p


def coffee_machine(S, x, y, yaw=0.0, z=0.9, name="CoffeeMachine"):
    """咖啡機（正面朝 -Y）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0.05, 0.19, 0.34, 0.36, 0.38, "metal_dark")
    p.box(0, -0.1, 0.34, 0.2, 0.06, 0.05, "plastic_black")
    p.box(0, -0.12, 0.08, 0.16, 0.12, 0.02, "metal")
    p.cyl(0, -0.12, 0.12, 0.035, 0.08, mat("mug", (0.9, 0.9, 0.88)), seg=10)
    p.box(0.1, -0.13, 0.28, 0.06, 0.02, 0.04, mat("status_green", (0.2, 0.9, 0.3), emit=(0.2, 0.9, 0.3)))
    p.finish(obstacle=False)
    return p


def microwave(S, x, y, yaw=0.0, z=0.9, name="Microwave"):
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0, 0.14, 0.46, 0.34, 0.28, "plastic_white")
    p.box(-0.05, -0.171, 0.14, 0.3, 0.004, 0.2, "plastic_black")
    p.box(0.19, -0.171, 0.14, 0.06, 0.004, 0.2, "metal_dark")
    p.finish(obstacle=False)
    return p


def fridge(S, x, y, yaw=0.0, w=0.75, d=0.7, h=1.85, name="Fridge"):
    """直立冰箱（正面朝 -Y）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, "metal")
    p.box(0, -d / 2 - 0.004, h * 0.62, w - 0.02, 0.006, 0.01, "metal_dark")
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.08), -d / 2 - 0.02, h * 0.62 - 0.4, 0.025, 0.03, 0.5, "plastic_black")
    p.finish(footprint=(w, d))
    return p


def vending_machine(S, x, y, yaw=0.0, w=0.95, d=0.8, h=1.85, name="VendingMachine"):
    """通用販賣機（無品牌；正面朝 -Y）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, "panel_blue")
    p.box(-0.08, -d / 2 - 0.004, h * 0.6, w - 0.3, 0.008, h * 0.6, mat("vend_glass", (0.15, 0.2, 0.25), rough=0.1))
    for i in range(4):
        for j in range(3):
            p.box(-0.08 - 0.22 + j * 0.22, -d / 2 - 0.012, h * 0.42 + i * 0.22, 0.14, 0.008, 0.12,
                  ("fabric_orange", "chair_red", "chair_green", "plastic_white")[(i + j) % 4])
    p.box(0.33, -d / 2 - 0.006, h * 0.7, 0.14, 0.008, 0.3, "metal_dark")
    p.box(0, -d / 2 - 0.006, 0.18, 0.5, 0.008, 0.2, "plastic_black")
    p.finish(footprint=(w, d))
    return p


def armchair(S, x, y, yaw=0.0, color="fabric_teal", name="Armchair"):
    """單人沙發椅，坐向 +Y（yaw=0 背靠南側）。"""
    return sofa(S, x, y, yaw, w=0.9, d=0.85, color=color, name=name, seat_clear=True)


def coffee_table(S, x, y, yaw=0.0, w=1.2, d=0.6, h=0.4, top="wood_light", name="CoffeeTable"):
    return table(S, x, y, yaw, w=w, d=d, h=h, top=top, name=name)


def beanbag(S, x, y, color="fabric_orange", r=0.42, name="Beanbag"):
    """懶骨頭（扁球體）。"""
    p = Piece(S, name, x, y)
    p.sphere(0, 0, 0.26, r, color, sz=0.62, seg=16)
    p.sphere(0, -r * 0.45, 0.45, r * 0.62, color, sz=0.9, seg=14)
    p.finish(footprint=(0.1, 0.1))
    return p


def tv_console(S, x, y, yaw=0.0, w=2.0, name="TVConsole"):
    """電視櫃（低櫃）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.25, w, 0.4, 0.5, "wood_dark")
    p.finish(footprint=(w, 0.4))
    return p


def foosball(S, x, y, yaw=0.0, w=1.4, d=0.75, name="Foosball"):
    """桌上足球機（長邊沿 piece X 軸）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.8, w, d, 0.1, "panel_blue")
    p.boxc(-w / 2, -d / 2, 0.8, w / 2, -d / 2 + 0.04, 0.95, "wood_dark")
    p.boxc(-w / 2, d / 2 - 0.04, 0.8, w / 2, d / 2, 0.95, "wood_dark")
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box(sx * (w / 2 - 0.05), sy * (d / 2 - 0.05), 0.38, 0.07, 0.07, 0.76, "wood_dark")
    for k in range(-3, 4):
        p.cyl(k * 0.17, 0, 1.0, 0.012, d + 0.25, "metal", seg=6, axis="Y")
        p.box(k * 0.17, 0, 0.98, 0.04, 0.06, 0.1, "chair_red" if k < 0 else "plastic_white")
    p.finish(footprint=(w + 0.05, d + 0.3))
    return p


def pool_table(S, x, y, yaw=0.0, w=2.3, d=1.3, name="PoolTable"):
    """撞球桌。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.8, w, d, 0.1, "wood_dark")
    p.box(0, 0, 0.86, w - 0.2, d - 0.2, 0.03, mat("felt", (0.04, 0.32, 0.18), rough=0.9))
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box(sx * (w / 2 - 0.12), sy * (d / 2 - 0.12), 0.38, 0.14, 0.14, 0.76, "wood_dark")
    for i, (bx, by) in enumerate(((0.3, 0.0), (0.38, 0.04), (0.38, -0.04), (-0.5, 0.0))):
        p.sphere(bx, by, 0.9, 0.028, ("chair_red", "fabric_orange", "chair_seat", "plastic_white")[i], seg=8)
    p.finish(footprint=(w, d))
    return p


# ---------------------------------------------------------------- 大廳／接待設備（場景 006 起）
def reception_desk(S, x, y, yaw=0.0, w=4.0, name="ReceptionDesk"):
    """接待櫃台：訪客側（-Y）為高檯面 1.1 m，工作側（+Y）為 0.74 m 桌面。(x,y) 為整體中心。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, -0.38, 0.55, w, 0.3, 1.1, "wood_dark")
    p.box(0, -0.38, 1.11, w + 0.06, 0.38, 0.04, "desk_white")
    p.box(0, 0.12, 0.735, w - 0.1, 0.72, 0.03, "desk_white")
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.08), 0.12, 0.36, 0.04, 0.6, 0.72, "desk_leg")
    p.box(0, -0.545, 0.55, w - 0.5, 0.02, 0.6, "metal")  # 前飾板（無文字）
    p.finish(footprint=(w, 1.0, 0, -0.05))
    return p


def turnstile(S, x, y, yaw=0.0, name="Turnstile"):
    """閘機柱（通道沿本地 Y 方向；yaw=0 時柱體長軸沿 Y，一對柱形成沿 X 的通道需旋轉）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.5, 0.22, 0.9, 1.0, "metal")
    p.box(0, 0, 1.01, 0.24, 0.92, 0.03, "plastic_black")
    p.box(0, 0.0, 1.03, 0.1, 0.5, 0.004, mat("status_green", (0.2, 0.9, 0.3), emit=(0.2, 0.9, 0.3)))
    p.box(0, 0.35, 0.45, 0.3, 0.02, 0.5, mat("glass_panel", (0.6, 0.8, 0.9), rough=0.05, alpha=0.25))
    p.finish(footprint=(0.3, 0.92))
    return p


def info_kiosk(S, x, y, yaw=0.0, name="InfoKiosk"):
    """立式訪客登記機（螢幕面朝 -Y）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.55, 0.45, 0.3, 1.1, "plastic_white")
    p.box(0, -0.15, 1.25, 0.5, 0.04, 0.4, "plastic_black")
    p.box(0, -0.172, 1.25, 0.46, 0.004, 0.36, mat("screen_glow", (0.05, 0.15, 0.3), emit=(0.08, 0.3, 0.6)))
    p.finish(footprint=(0.5, 0.4))
    return p


def feature_wall(S, x, y, yaw=0.0, w=4.0, h=2.3, name="FeatureWall"):
    """背景裝飾牆板（木紋條 + 無文字金屬圓盤；正面朝 -Y，(x,y) 為背面中心）。"""
    p = Piece(S, name, x, y, yaw=yaw, coll="PROPS")
    p.box(0, -0.02, h / 2 + 0.05, w, 0.04, h, "wood_light")
    for i in range(1, int(w / 0.4)):
        p.box(-w / 2 + 0.4 * i, -0.045, h / 2 + 0.05, 0.02, 0.01, h, "wood_dark")
    p.cyl(0, -0.06, 1.6, 0.3, 0.02, "metal", seg=32, axis="Y")
    p.finish(obstacle=False)
    return p


def bench(S, x, y, yaw=0.0, w=1.6, d=0.45, h=0.45, color="fabric_teal", name="Bench"):
    """長凳，坐向 +Y。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h - 0.06, w, d, 0.12, color)
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.1), 0, (h - 0.12) / 2, 0.04, d - 0.1, h - 0.12, "metal_dark")
    p.finish(footprint=(w, d))
    return p


def server_rack(S, x, y, yaw=0.0, w=0.6, d=1.0, h=2.0, name="Rack", leds=True):
    """19 吋伺服器機櫃（正面朝本地 -Y；yaw=0 時機櫃正面朝南）。含伺服器面板與狀態 LED。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, "metal_dark")
    p.box(0, -d / 2 - 0.01, h / 2, w - 0.06, 0.02, h - 0.1, mat("rack_front", (0.07, 0.08, 0.09), rough=0.4, metal=0.5))
    green = mat("led_green", (0.1, 0.9, 0.3), emit=(0.1, 0.9, 0.3))
    blue = mat("led_blue", (0.2, 0.5, 1.0), emit=(0.2, 0.5, 1.0))
    for i in range(10):
        zc = 0.25 + i * 0.17
        p.box(0, -d / 2 - 0.025, zc, w - 0.1, 0.02, 0.14, "metal")
        if leds:
            p.box(-w / 2 + 0.09, -d / 2 - 0.04, zc, 0.03, 0.01, 0.02, green if i % 3 else blue)
    p.finish(footprint=(w, d))
    return p


def crac_unit(S, x, y, yaw=0.0, w=0.9, d=0.9, h=1.9, name="CoolingUnit"):
    """精密空調（機房冷卻單元），正面朝本地 -Y。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, "cabinet")
    p.box(0, -d / 2 - 0.01, h * 0.7, w - 0.2, 0.02, 0.6, "metal")
    for i in range(6):
        p.box(0, -d / 2 - 0.015, 0.2 + i * 0.1, w - 0.2, 0.02, 0.02, "metal_dark")
    p.box(0.25, -d / 2 - 0.02, h * 0.45, 0.2, 0.02, 0.1, mat("crac_display", (0.1, 0.3, 0.5), emit=(0.1, 0.4, 0.7)))
    p.finish(footprint=(w, d))
    return p


def ups_cabinet(S, x, y, yaw=0.0, w=0.8, d=0.8, h=1.7, name="UPS"):
    """不斷電系統櫃，正面朝本地 -Y。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, "fabric_grey")
    p.box(0, -d / 2 - 0.01, h * 0.8, 0.4, 0.02, 0.25, mat("ups_display", (0.1, 0.5, 0.2), emit=(0.1, 0.8, 0.3)))
    p.box(0, -d / 2 - 0.01, h * 0.35, w - 0.1, 0.02, h * 0.5, "metal_dark")
    p.finish(footprint=(w, d))
    return p


def cable_tray(S, x, y, length, yaw=0.0, z=2.5, w=0.4, name="CableTray"):
    """天花吊掛線槽（沿本地 X 方向）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0, 0, length, w, 0.03, "metal")
    for sy in (-1, 1):
        p.box(0, sy * (w / 2 - 0.01), 0.04, length, 0.02, 0.08, "metal")
    for i in range(int(length // 1.5) + 1):
        p.box(-length / 2 + 0.2 + i * 1.5, 0, 0.2, 0.03, w, 0.03, "metal_dark")
    p.finish(obstacle=False)
    return p


def crash_cart(S, x, y, yaw=0.0, name="CrashCart"):
    """機房推車（螢幕＋鍵盤），使用者面向本地 +Y 側。"""
    p = Piece(S, name, x, y, yaw=yaw, coll="PROPS")
    p.box(0, 0, 0.45, 0.6, 0.5, 0.04, "metal")
    p.box(0, 0, 0.1, 0.6, 0.5, 0.03, "metal")
    for sx in (-1, 1):
        for sy in (-1, 1):
            p.box(sx * 0.28, sy * 0.22, 0.25, 0.03, 0.03, 0.5, "metal_dark")
    p.box(0, 0.1, 0.8, 0.4, 0.03, 0.28, "screen")
    p.box(0, -0.05, 0.49, 0.36, 0.14, 0.015, "plastic_black")
    p.finish(footprint=(0.6, 0.5))
    return p


# ---------------------------------------------------------------- 控制中心（013 起）
def control_console(S, x, y, yaw=0.0, w=1.6, d=0.85, h=0.74, screens=3, name="Console"):
    """監控工位：桌面＋側板＋後方矮背牆＋弧形排列的 2–3 面螢幕＋鍵盤。使用者坐在 -Y 側、面向 +Y。"""
    p = Piece(S, name, x, y, yaw=yaw)
    glow = mat("screen_glow", (0.05, 0.15, 0.3), emit=(0.08, 0.3, 0.6))
    p.box(0, 0, h - 0.02, w, d, 0.04, "desk_white")
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.02), 0, (h - 0.04) / 2, 0.04, d - 0.06, h - 0.04, "desk_leg")
    p.box(0, d / 2 - 0.03, 0.55, w, 0.06, 1.10, "desk_leg")                 # 背牆（遮線、隔開前排）
    p.box(0, d / 2 - 0.03, 1.115, w, 0.10, 0.03, "metal")                   # 背牆頂蓋
    sw, sh = 0.50, 0.30
    offs = (-1, 0, 1) if screens >= 3 else (-0.5, 0.5)
    for k in offs:
        ang = -k * math.radians(22)
        cx, cy = k * (sw + 0.015) * math.cos(math.radians(11) * abs(k)), d / 2 - 0.20 - abs(k) * 0.085
        p.box(cx, cy + 0.04, h + 0.11, 0.04, 0.04, 0.22, "metal_dark", rz=ang)
        p.box(cx, cy, h + 0.12 + sh / 2, sw, 0.025, sh, "plastic_black", rz=ang)
        p.box(cx + 0.014 * math.sin(ang), cy - 0.014 * math.cos(ang), h + 0.12 + sh / 2, sw - 0.03, 0.002, sh - 0.03, glow, rz=ang)
    p.box(0, -0.12, h + 0.01, 0.42, 0.14, 0.02, "plastic_white")             # 鍵盤
    p.box(0.33, -0.12, h + 0.008, 0.06, 0.10, 0.016, "plastic_black")        # 滑鼠
    p.box(-0.55, -0.05, h + 0.03, 0.16, 0.20, 0.06, "metal_dark")            # 通話面板
    p.finish(footprint=(w, d))
    return p


def video_wall(S, x, y, yaw=0.0, cols=4, rows=2, tw=1.6, th=0.9, z=0.85, name="VideoWall"):
    """拼接大螢幕牆，正面朝 -Y（(x,y) 為背面中心）。每格以發光方塊畫出通用的圖表／狀態矩陣／趨勢線（無文字、無商標）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    W, H = cols * tw, rows * th
    base = mat("vw_base", (0.02, 0.05, 0.10), emit=(0.01, 0.035, 0.08))
    cs = {"g": mat("vw_green", (0.1, 0.8, 0.4), emit=(0.08, 0.75, 0.35)),
          "a": mat("vw_amber", (0.9, 0.6, 0.1), emit=(0.9, 0.55, 0.08)),
          "r": mat("vw_red", (0.9, 0.2, 0.15), emit=(0.9, 0.15, 0.1)),
          "b": mat("vw_blue", (0.2, 0.6, 0.95), emit=(0.15, 0.55, 0.95)),
          "w": mat("vw_white", (0.8, 0.9, 1.0), emit=(0.6, 0.75, 0.9))}
    p.box(0, -0.04, H / 2, W + 0.12, 0.08, H + 0.12, "plastic_black")
    yf = -0.083

    def E(u, v, su, sv, c):   # u,v 為牆面座標（左下為 -W/2, 0）
        p.box(u, yf - 0.004, v, su, 0.004, sv, cs[c])
    for i in range(cols):
        for j in range(rows):
            u0, v0 = -W / 2 + i * tw, j * th
            p.box(u0 + tw / 2, yf, v0 + th / 2, tw - 0.03, 0.006, th - 0.03, base)
            kind = (i + 2 * j) % 4
            E(u0 + 0.33, v0 + th - 0.11, 0.42, 0.045, "w")                  # 標題列
            if kind == 0:      # 長條圖
                for k, hh in enumerate((0.25, 0.42, 0.33, 0.55, 0.47, 0.30, 0.52, 0.38)):
                    E(u0 + 0.22 + k * 0.165, v0 + 0.10 + hh / 2, 0.10, hh, "b" if k % 3 else "g")
            elif kind == 1:    # 代理人狀態矩陣
                pat = "ggagggrggaggggggagggggga"
                for k in range(24):
                    E(u0 + 0.20 + (k % 8) * 0.17, v0 + 0.16 + (k // 8) * 0.17, 0.12, 0.12, pat[(k + 5 * i + 3 * j) % 24])
            elif kind == 2:    # 趨勢折線（以短段近似）
                ys = (0.20, 0.27, 0.24, 0.35, 0.31, 0.44, 0.40, 0.52, 0.49, 0.58)
                for k, yy in enumerate(ys):
                    E(u0 + 0.18 + k * 0.135, v0 + yy, 0.12, 0.03, "g")
                    E(u0 + 0.18 + k * 0.135, v0 + yy * 0.55 + 0.04, 0.12, 0.03, "a")
            else:              # 佇列／進度條
                for k, ww in enumerate((1.1, 0.8, 1.25, 0.55, 0.95)):
                    E(u0 + 0.15 + ww / 2, v0 + 0.14 + k * 0.115, ww, 0.06, ("b", "g", "b", "a", "g")[k])
    p.finish(obstacle=False)
    return p


def pendant_status_lamp(S, x, y, z=2.2, name="StatusPendant", color=(0.2, 0.9, 0.3)):
    """自天花板垂吊的狀態燈（細桿＋燈座＋發光球），發光球中心約在 STATUS 錨點高度 z。"""
    p = Piece(S, name, x, y, 0, coll="PROPS")
    top = S.H
    p.cyl(0, 0, (top + z + 0.08) / 2, 0.008, top - z - 0.08, "metal_dark", seg=6)
    p.cyl(0, 0, z + 0.07, 0.05, 0.04, "metal_dark", seg=12)
    p.sphere(0, 0, z, 0.06, mat("status_" + "_".join("%d" % (c * 10) for c in color), color, emit=color), seg=10)
    p.finish(obstacle=False)
    return p


# ---------------------------------------------------------------- 代理人工作艙（014 起）
def agent_pod(S, x, y, yaw=0.0, w=1.6, d=1.6, h=1.5, accent=(0.10, 0.50, 0.52), lamp=(0.2, 0.9, 0.3),
              lamp_z=2.2, index=1, name="AgentPod"):
    """標準化代理人工作艙：背板（+Y 側，靠牆）＋兩側隔板＋桌面＋雙螢幕＋運算單元＋地墊＋背板頂端狀態燈座。
    (x,y) 為艙位中心，使用者坐在 -Y 側、面向 +Y；艙口開在 -Y 側。狀態燈球心在背板中央上方 lamp_z。
    index 以背板上的小方點數量表示艙號（不使用文字）。回傳 (piece, 椅子位置, 狀態燈位置)（世界座標）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    glow = mat("screen_glow", (0.05, 0.15, 0.3), emit=(0.08, 0.3, 0.6))
    acc = mat("pod_acc_" + "_".join("%d" % (c * 100) for c in accent), accent, rough=0.8)
    shell = mat("pod_shell", (0.80, 0.82, 0.84), rough=0.7)
    t = 0.06
    yb = d / 2 - t / 2                      # 背板中心
    side_len = d - 0.3                      # 側板不到艙口，留 0.3 m 讓出入口較寬
    ys = d / 2 - side_len / 2
    p.box(0, yb, h / 2, w, t, h, shell)                                   # 背板
    p.box(0, yb - t / 2 - 0.006, h - 0.16, w - 2 * t, 0.012, 0.22, acc)       # 背板色帶
    for sx in (-1, 1):
        p.box(sx * (w / 2 - t / 2), ys, (h - 0.1) / 2, t, side_len, h - 0.1, shell)
        p.box(sx * (w / 2 - t / 2), ys, h - 0.1 + 0.015, t + 0.02, side_len, 0.03, "metal_dark")
        p.box(sx * (w / 2 - t / 2), d / 2 - side_len - 0.012, (h - 0.1) / 2, t + 0.01, 0.024, h - 0.1, acc)   # 側板端蓋
    p.box(0, yb, h + 0.015, w + 0.02, t + 0.02, 0.03, "metal_dark")       # 背板頂蓋
    # 桌面
    dd, dh = 0.65, 0.74
    yd = d / 2 - t - dd / 2
    p.box(0, yd, dh - 0.015, w - 2 * t, dd, 0.03, "desk_white")
    p.box(0, yd + dd / 2 - 0.25, dh / 2, 0.05, 0.05, dh - 0.03, "desk_leg")
    p.box(0, yd - dd / 2 + 0.02, dh - 0.045, w - 2 * t, 0.03, 0.03, "desk_leg")
    # 雙螢幕（掛在背板上）
    sw, sh = 0.56, 0.33
    for k in (-1, 1):
        cx = k * (sw / 2 + 0.01)
        p.box(cx, d / 2 - t - 0.035, dh + 0.14 + sh / 2, sw, 0.03, sh, "plastic_black")
        p.box(cx, d / 2 - t - 0.052, dh + 0.14 + sh / 2, sw - 0.03, 0.002, sh - 0.03, glow)
    p.box(0, d / 2 - t - 0.02, dh + 0.14 + sh / 2, 0.10, 0.04, 0.10, "metal_dark")
    p.box(-0.05, yd - 0.12, dh + 0.01, 0.42, 0.14, 0.02, "plastic_white")       # 鍵盤
    p.box(0.28, yd - 0.12, dh + 0.008, 0.06, 0.10, 0.016, "plastic_black")      # 滑鼠
    # 桌下運算單元（通用機箱＋指示燈）
    ux = w / 2 - t - 0.16
    p.box(ux, yd + 0.05, 0.25, 0.20, 0.45, 0.46, "metal_dark")
    led = mat("status_" + "_".join("%d" % (c * 10) for c in lamp), lamp, emit=lamp)
    for k in range(3):
        p.box(ux, yd + 0.05 - 0.2265, 0.38 - k * 0.07, 0.10, 0.004, 0.02, led)
    # 艙號方點（背板色帶上）
    for k in range(index):
        p.box(-w / 2 + t + 0.12 + k * 0.07, yb - t / 2 - 0.014, h - 0.16, 0.04, 0.006, 0.04, "plastic_white")
    # 地墊
    p.box(0, -0.05, 0.004, w - 2 * t - 0.04, d - 0.2, 0.008, acc)
    # 狀態燈座：背板頂端立桿＋燈座＋發光球
    p.cyl(0, yb, (h + lamp_z - 0.08) / 2, 0.012, lamp_z - 0.08 - h, "metal_dark", seg=8)
    p.cyl(0, yb, h + 0.05, 0.05, 0.04, "metal_dark", seg=12)
    p.cyl(0, yb, lamp_z - 0.075, 0.045, 0.03, "metal_dark", seg=12)
    p.sphere(0, yb, lamp_z, 0.07, led, seg=12)
    p.finish()
    # 導航障礙：背板＋桌、兩側隔板
    c, s = math.cos(yaw), math.sin(yaw)

    def wpt(lx, ly):
        return (x + lx * c - ly * s, y + lx * s + ly * c)
    ox, oy = wpt(0, d / 2 - (t + dd) / 2)
    S.obstacles.append((ox, oy, yaw, w, t + dd))
    for sx in (-1, 1):
        ox, oy = wpt(sx * (w / 2 - t / 2), ys)
        S.obstacles.append((ox, oy, yaw, t, side_len))
    return p, wpt(0, yd - dd / 2 - 0.42), wpt(0, yb)


# ---------------------------------------------------------------- 多功能活動空間（015 起）
def tiered_seating(S, x, y, yaw=0.0, w=6.4, tiers=4, depth=0.9, rise=0.45, aisle=1.0, per_side=3,
                   name="TieredSeating"):
    """階梯座位（看台）：tiers 階木質平台，中央走道含半階踏步，每階兩側各 per_side 個坐墊。
    (x,y) 為整體中心；yaw=0 時觀眾面向 +Y（最低階在 +Y 側、最高階靠 -Y 側牆）。
    第 k 階（0 起算）的人坐在該階前緣、腳踩前一階（或地面），故坐下點高度 z = k*rise。
    導航障礙只含前緣後 0.3 m 起的範圍，使最低階坐下點貼近導航網格。
    回傳 (piece, seats)；seats = [(世界x, 世界y, z, 階序k), ...]，由低階到高階、每階由 -X 到 +X。"""
    p = Piece(S, name, x, y, yaw=yaw)
    D = tiers * depth
    wood, dark = "wood_light", "wood_dark"
    cols = ("fabric_teal", "fabric_orange", "fabric_grey")
    side_w = (w - aisle) / 2
    seats = []
    c, s = math.cos(yaw), math.sin(yaw)
    for k in range(tiers):
        y0, y1 = -D / 2, D / 2 - k * depth          # 第 k 階平台（由後牆延伸到前緣）
        z0, z1 = k * rise, (k + 1) * rise
        p.boxc(-w / 2, y0, z0, w / 2, y1, z1, wood)
        p.box(0, y1 + 0.006, (z0 + z1) / 2, w, 0.012, rise - 0.04, dark)            # 立板深色面
        p.box(0, y1 - 0.02, z1 + 0.003, w, 0.04, 0.006, "metal")                    # 踏面前緣止滑條
        # 中央走道半階踏步
        p.boxc(-aisle / 2 + 0.05, y1, z0, aisle / 2 - 0.05, y1 + 0.3, z0 + rise / 2, dark)
        for sx in (-1, 1):
            for i in range(per_side):
                lx = sx * (aisle / 2 + side_w * (i + 0.5) / per_side)
                ly = y1 - 0.28
                p.box(lx, ly, z1 + 0.03, min(0.6, side_w / per_side - 0.12), 0.46, 0.06, cols[(i + k) % 3])
                seats.append((lx, ly, z0, k))
    for sx in (-1, 1):                               # 兩側階梯形封板
        for k in range(tiers):
            p.boxc(sx * w / 2, -D / 2, k * rise, sx * (w / 2 + 0.02), D / 2 - k * depth, (k + 1) * rise, dark)
    p.finish(footprint=(w, D - 0.3, 0, -0.15))
    S.obstacles.append((x - (D / 2 + 0.15) * s, y + (D / 2 + 0.15) * c, yaw, aisle - 0.1, 0.3))   # 最低半階
    seats.sort(key=lambda t: (t[3], t[0]))
    return p, [(x + lx * c - ly * s, y + lx * s + ly * c, z, k) for (lx, ly, z, k) in seats]


def movable_partition(S, x, y, yaw=0.0, w=1.6, h=1.9, color="fabric_teal", name="Partition"):
    """附輪可移動隔間板：-Y 面為白板、+Y 面為吸音布面，兩支橫腳附腳輪。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, 0.12 + (h - 0.12) / 2, w, 0.05, h - 0.12, "metal")
    p.box(0, -0.028, 0.12 + (h - 0.12) / 2, w - 0.08, 0.008, h - 0.2, "whiteboard")
    p.box(0, 0.028, 0.12 + (h - 0.12) / 2, w - 0.08, 0.008, h - 0.2, mat(color, rough=0.95))
    for sx in (-1, 1):
        p.box(sx * (w / 2 - 0.15), 0, 0.10, 0.05, 0.5, 0.04, "metal_dark")
        for sy in (-1, 1):
            p.cyl(sx * (w / 2 - 0.15), sy * 0.22, 0.04, 0.04, 0.03, "plastic_black", seg=10, axis="X")
    p.finish(footprint=(w, 0.5))
    return p


def stage_platform(S, x, y, yaw=0.0, w=6.0, d=3.0, h=0.2, name="Stage"):
    """矮舞台平台（木質面＋深色側裙＋前緣警示條）。(x,y) 為中心，前緣在 -Y 側。"""
    p = Piece(S, name, x, y, yaw=yaw)
    p.box(0, 0, h / 2, w, d, h, "wood_dark")
    p.box(0, 0, h + 0.004, w - 0.04, d - 0.04, 0.008, mat("stage_top", (0.42, 0.30, 0.19), rough=0.6))
    p.box(0, -d / 2 + 0.05, h + 0.009, w - 0.04, 0.05, 0.003, mat("stage_edge", (0.92, 0.75, 0.15), rough=0.7))
    p.finish(footprint=(w, d))
    return p


def lectern(S, x, y, yaw=0.0, z=0.0, name="Lectern"):
    """講桌（講者站在 -Y 側、面向 +Y）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.box(0, 0.05, 0.5, 0.5, 0.3, 1.0, "wood_light")
    p.box(0, 0.212, 0.5, 0.42, 0.006, 0.7, "wood_dark")
    p.box(0, 0, 1.03, 0.6, 0.45, 0.03, "wood_dark")
    p.cyl(0.15, 0.1, 1.16, 0.008, 0.24, "metal_dark", seg=6)
    p.sphere(0.15, 0.1, 1.29, 0.025, "plastic_black", seg=8)
    p.finish(obstacle=False)
    return p


def stack_chair(S, x, y, yaw=0.0, color="chair_seat", name="StackChair"):
    """可堆疊活動椅（四腳，人坐向 +Y）。"""
    p = Piece(S, name, x, y, yaw=yaw)
    for sx in (-1, 1):
        p.box(sx * 0.2, 0.18, 0.22, 0.025, 0.025, 0.44, "metal")
        p.box(sx * 0.2, -0.2, 0.42, 0.025, 0.025, 0.84, "metal")
    p.box(0, 0, 0.455, 0.44, 0.42, 0.04, color)
    p.box(0, -0.205, 0.72, 0.44, 0.03, 0.26, color)
    p.finish(obstacle=False)
    return p


def pa_speaker(S, x, y, yaw=0.0, z=0.0, name="Speaker"):
    """立架式擴聲喇叭（正面朝 -Y）。"""
    p = Piece(S, name, x, y, z, yaw=yaw, coll="PROPS")
    p.cyl(0, 0, 0.6, 0.02, 1.2, "metal_dark", seg=8)
    for a in range(3):
        an = a * 2.094
        p.box(0.16 * math.cos(an), 0.16 * math.sin(an), 0.02, 0.34, 0.03, 0.03, "metal_dark", rz=an)
    p.box(0, 0, 1.47, 0.32, 0.28, 0.54, "plastic_black")
    p.cyl(0, -0.142, 1.38, 0.11, 0.01, "metal_dark", seg=16, axis="Y")
    p.cyl(0, -0.142, 1.62, 0.05, 0.01, "metal_dark", seg=12, axis="Y")
    p.finish(obstacle=False)
    return p


def lighting_truss(S, x, y, length, yaw=0.0, z=2.7, lamps=5, name="LightTruss"):
    """舞台燈桿：沿本地 X 的桿件＋吊桿＋數盞筒燈（朝本地 +Y 斜下方打光，燈口自發光）。"""
    p = Piece(S, name, x, y, 0, yaw=yaw, coll="PROPS")
    p.cyl(0, 0, z, 0.03, length, "metal_dark", seg=8, axis="X")
    for sx in (-1, 1):
        p.cyl(sx * (length / 2 - 0.2), 0, (z + S.H) / 2, 0.012, S.H - z, "metal_dark", seg=6)
    warm = mat("spot_warm", (1.0, 0.85, 0.6), emit=(1.0, 0.8, 0.5))
    for i in range(lamps):
        lx = -length / 2 + length * (i + 0.5) / lamps
        p.box(lx, 0, z - 0.06, 0.03, 0.03, 0.08, "metal_dark")
        p.cyl(lx, 0.05, z - 0.17, 0.07, 0.2, "plastic_black", seg=12, axis="Y")
        p.cyl(lx, 0.152, z - 0.17, 0.06, 0.006, warm, seg=12, axis="Y")
    p.finish(obstacle=False)
    return p
