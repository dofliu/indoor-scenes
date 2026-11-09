"""DofLab 室內場景模組庫 — 共用參數化建模函式庫（bpy）。

用法（於各場景 build.py）：
    import sys, os
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
    from scenelib import *
    S = Scene("001", "open_office", "開放式工位辦公區", "Open-plan Office", "office", (16, 12))
    ...
    S.finish(out_dir)

座標慣例：公尺、Z 向上、+Y 為北、房間西南角為原點、地板頂面 z=0。
yaw_deg：Blender 繞 Z 軸旋轉（逆時針為正）。yaw=0 面向 +Y（北），90 面向 -X（西），-90 面向 +X（東），180 面向 -Y（南）。
"""
import bpy
import bmesh
import math
import json
import os
import datetime
from mathutils import Matrix, Vector

WALL_T = 0.2
HEIGHT = 3.0
DOOR_W = 1.0
DOOR_H = 2.2
NAV_CELL = 0.25
NAV_MARGIN = 0.3
SIDES = ("S", "E", "N", "W")
COLLS = ("STRUCTURE", "FURNITURE", "PROPS", "LIGHTS", "ANCHORS", "NAV")

# ---------------------------------------------------------------- 材質調色盤
PALETTE = {
    "floor_carpet": (0.20, 0.24, 0.30), "floor_wood": (0.55, 0.38, 0.22),
    "floor_concrete": (0.45, 0.45, 0.46), "floor_tile": (0.78, 0.78, 0.76),
    "floor_epoxy": (0.30, 0.42, 0.36),
    "wall": (0.93, 0.92, 0.89), "wall_accent": (0.16, 0.38, 0.48), "wall_dark": (0.22, 0.24, 0.27),
    "ceiling": (0.96, 0.96, 0.95), "frame": (0.25, 0.26, 0.28),
    "desk_top": (0.86, 0.80, 0.70), "desk_white": (0.92, 0.92, 0.90), "desk_leg": (0.20, 0.21, 0.23),
    "chair_seat": (0.12, 0.20, 0.32), "chair_red": (0.70, 0.18, 0.15), "chair_green": (0.22, 0.52, 0.32),
    "plastic_black": (0.04, 0.04, 0.045), "plastic_white": (0.88, 0.88, 0.88),
    "metal": (0.62, 0.64, 0.66), "metal_dark": (0.18, 0.19, 0.20),
    "screen": (0.02, 0.03, 0.05), "panel_blue": (0.10, 0.35, 0.60),
    "whiteboard": (0.97, 0.97, 0.97), "wood_dark": (0.30, 0.20, 0.12), "wood_light": (0.72, 0.55, 0.36),
    "leaf": (0.12, 0.42, 0.16), "pot": (0.72, 0.70, 0.66), "cabinet": (0.78, 0.80, 0.82),
    "fabric_grey": (0.45, 0.47, 0.50), "fabric_orange": (0.88, 0.45, 0.15), "fabric_teal": (0.10, 0.50, 0.52),
    "rug": (0.58, 0.30, 0.26), "rug_blue": (0.10, 0.27, 0.34), "nav": (0.1, 0.9, 0.4), "paper": (0.95, 0.94, 0.90),
}
_mat_cache = {}


def mat(name, rgb=None, rough=0.55, metal=0.0, emit=None, alpha=1.0):
    """程序化 Principled BSDF 材質（同名只建一次）。"""
    if name in _mat_cache and _mat_cache[name].name in bpy.data.materials:
        return _mat_cache[name]
    rgb = rgb or PALETTE.get(name, (0.6, 0.6, 0.6))
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if alpha < 1.0:
        b.inputs["Alpha"].default_value = alpha
        try:
            m.surface_render_method = "BLENDED"
        except Exception:
            pass
    if emit:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = 3.0
    m.diffuse_color = (*rgb, alpha)
    _mat_cache[name] = m
    return m


def M(name, **kw):
    return mat(name, **kw)


# ---------------------------------------------------------------- Piece：把多個幾何合併成單一物件
class Piece:
    """累積 box/cyl 幾何（piece 區域座標），finish 後成為單一 mesh 物件（多材質槽）。"""

    def __init__(self, S, name, x=0, y=0, z=0, yaw=0.0, coll="FURNITURE"):
        self.S, self.name, self.x, self.y, self.z, self.yaw, self.coll = S, name, x, y, z, yaw, coll
        self.bm = bmesh.new()
        self.mats = []

    def _mi(self, m):
        if isinstance(m, str):
            m = mat(m)
        if m not in self.mats:
            self.mats.append(m)
        return self.mats.index(m)

    def _tag(self, geom_verts, m):
        mi = self._mi(m)
        faces = {f for v in geom_verts for f in v.link_faces}
        for f in faces:
            f.material_index = mi

    def box(self, cx, cy, cz, sx, sy, sz, m, rz=0.0):
        r = bmesh.ops.create_cube(self.bm, size=1.0)
        T = Matrix.Translation((cx, cy, cz)) @ Matrix.Rotation(rz, 4, "Z") @ Matrix.Diagonal((sx, sy, sz, 1))
        bmesh.ops.transform(self.bm, matrix=T, verts=r["verts"])
        self._tag(r["verts"], m)
        return self

    def boxc(self, x0, y0, z0, x1, y1, z1, m):
        """以對角角點指定（piece 座標）。"""
        return self.box((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), m)

    def cyl(self, cx, cy, cz, r, h, m, seg=20, axis="Z", r2=None):
        res = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=seg,
                                    radius1=r, radius2=r if r2 is None else r2, depth=h)
        rot = Matrix.Identity(4)
        if axis == "X":
            rot = Matrix.Rotation(math.radians(90), 4, "Y")
        elif axis == "Y":
            rot = Matrix.Rotation(math.radians(90), 4, "X")
        bmesh.ops.transform(self.bm, matrix=Matrix.Translation((cx, cy, cz)) @ rot, verts=res["verts"])
        self._tag(res["verts"], m)
        return self

    def sphere(self, cx, cy, cz, r, m, sx=1.0, sy=1.0, sz=1.0, seg=12):
        res = bmesh.ops.create_uvsphere(self.bm, u_segments=seg, v_segments=max(6, seg // 2), radius=r)
        T = Matrix.Translation((cx, cy, cz)) @ Matrix.Diagonal((sx, sy, sz, 1))
        bmesh.ops.transform(self.bm, matrix=T, verts=res["verts"])
        self._tag(res["verts"], m)
        return self

    def finish(self, footprint=None, obstacle=True):
        """footprint=(w,d,ox,oy)：piece 區域座標的導航障礙矩形（中心偏移 ox,oy）。"""
        mesh = bpy.data.meshes.new(self.name)
        self.bm.normal_update()
        self.bm.to_mesh(mesh)
        self.bm.free()
        for m in self.mats:
            mesh.materials.append(m)
        obj = bpy.data.objects.new(self.name, mesh)
        obj.location = (self.x, self.y, self.z)
        obj.rotation_euler = (0, 0, self.yaw)
        self.S.coll[self.coll].objects.link(obj)
        if footprint and obstacle:
            w, d = footprint[0], footprint[1]
            ox, oy = (footprint[2], footprint[3]) if len(footprint) > 2 else (0, 0)
            c, s = math.cos(self.yaw), math.sin(self.yaw)
            self.S.obstacles.append((self.x + ox * c - oy * s, self.y + ox * s + oy * c, self.yaw, w, d))
        return obj


def snap_yaw(deg):
    d = (deg + 180) % 360 - 180
    return 180.0 if d == -180 else d


# ---------------------------------------------------------------- Scene
class Scene:
    def __init__(self, sid, slug, name_zh, name_en, category, size, tags=None, height=HEIGHT):
        assert size[0] % 2 == 0 and size[1] % 2 == 0, "房間外框必須是 2 m 整數倍"
        self.id, self.slug, self.name_zh, self.name_en = sid, slug, name_zh, name_en
        self.category, self.W, self.D, self.H = category, size[0], size[1], height
        self.tags = tags or []
        self.doors, self.anchors, self.obstacles, self.windows = [], [], [], []
        self.door_objs = []
        self.extra_free = []  # 額外強制可走矩形 (x0,y0,x1,y1)
        self.wall_pieces = {}
        self._counters = {}
        _mat_cache.clear()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = bpy.context.scene
        self.scene.unit_settings.system = "METRIC"
        self.coll = {}
        for n in COLLS:
            c = bpy.data.collections.new(n)
            self.scene.collection.children.link(c)
            self.coll[n] = c

    # ---------- 錨點
    def _empty(self, name, x, y, z, yaw_deg, display="ARROWS", size=0.3, props=None, coll="ANCHORS"):
        e = bpy.data.objects.new(name, None)
        e.empty_display_type = display
        e.empty_display_size = size
        e.location = (x, y, z)
        e.rotation_euler = (0, 0, math.radians(yaw_deg))
        for k, v in (props or {}).items():
            e[k] = v
        self.coll[coll].objects.link(e)
        return e

    def _next(self, key):
        self._counters[key] = self._counters.get(key, 0) + 1
        return self._counters[key]

    def anchor(self, typ, use, x, y, yaw_deg=0.0, n=None, z=None):
        """typ: SEAT/STAND/POI/STATUS；SEAT/STAND/POI 的 use 為用途；STATUS 無 use。"""
        yaw_deg = snap_yaw(yaw_deg)
        if typ == "STATUS":
            n = n or self._next("STATUS")
            name, use, z = "STATUS_%02d" % n, "", (2.2 if z is None else z)
        else:
            n = n or self._next(typ + use)
            name, z = "%s_%s_%02d" % (typ, use, n), (0.0 if z is None else z)
        self._empty(name, x, y, z, yaw_deg, props={"anchor_type": typ, "use": use})
        self.anchors.append({"id": name, "type": typ, "use": use,
                             "position": [round(x, 3), round(y, 3), round(z, 3)], "yaw_deg": round(yaw_deg, 2)})
        return name

    # ---------- 結構
    def _wall_openings(self, side):
        ops = []
        for d in self.doors:
            if d["wall"] == side:
                ops.append((d["offset_m"] - d["width_m"] / 2, d["offset_m"] + d["width_m"] / 2, 0.0, DOOR_H, "door"))
        for w in self.windows:
            if w["wall"] == side:
                ops.append((w["offset_m"] - w["width_m"] / 2, w["offset_m"] + w["width_m"] / 2,
                            w["sill"], w["sill"] + w["height"], "window"))
        return sorted(ops)

    def add_door(self, wall, offset, width=DOOR_W):
        """門洞中心於該牆起點（S/N 牆自西起、E/W 牆自南起）之奇數公尺處。"""
        assert wall in SIDES and offset % 2 == 1, "門洞中心必須在奇數公尺：%s %s" % (wall, offset)
        L = self.W if wall in "SN" else self.D
        assert 1 <= offset <= L - 1, "門超出牆範圍"
        n = self._next("DOOR" + wall)
        self.doors.append({"id": "DOOR_%s_%02d" % (wall, n), "wall": wall, "offset_m": float(offset), "width_m": width})
        return self

    def add_window(self, wall, offset, width=2.0, sill=0.9, height=1.5):
        self.windows.append({"wall": wall, "offset_m": float(offset), "width_m": width, "sill": sill, "height": height})
        return self

    def _pos_on_wall(self, side, t):
        """沿牆座標 t → 牆中心線 (x,y) 與牆內法線朝向。"""
        h = WALL_T / 2
        if side == "S":
            return t, h
        if side == "N":
            return t, self.D - h
        if side == "W":
            return h, t
        return self.W - h, t

    def build_shell(self, floor="floor_carpet", wall="wall", ceiling=True, accent=None):
        """地板、牆（含門洞/窗洞/門框/玻璃）、天花板。accent={'N':'wall_accent'} 指定某面牆內側顏色。"""
        W, D, H = self.W, self.D, self.H
        p = Piece(self, "Floor", coll="STRUCTURE")
        p.boxc(0, 0, -0.1, W, D, 0, floor)
        p.finish()
        if ceiling:
            c = Piece(self, "Ceiling", coll="STRUCTURE")
            c.boxc(0, 0, H, W, D, H + 0.1, "ceiling")
            c.finish()
        glass = mat("glass", (0.6, 0.8, 0.9), rough=0.05, alpha=0.25)
        frame = mat("frame")
        for side in SIDES:
            lenw = W if side in "SN" else D
            lo, hi = (0, lenw) if side in "SN" else (WALL_T, lenw - WALL_T)
            ops = self._wall_openings(side)
            segs = []  # (t0,t1,z0,z1)
            cur = lo
            for (a, b, z0, z1, kind) in ops:
                if a > cur:
                    segs.append((cur, a, 0, H))
                if z0 > 0:
                    segs.append((a, b, 0, z0))
                if z1 < H:
                    segs.append((a, b, z1, H))
                cur = max(cur, b)
            if cur < hi:
                segs.append((cur, hi, 0, H))
            wp = Piece(self, "Wall_" + side, coll="STRUCTURE")
            inner_m = (accent or {}).get(side, wall)
            for (t0, t1, z0, z1) in segs:
                if side in "SN":
                    y0, y1 = (0, WALL_T) if side == "S" else (D - WALL_T, D)
                    wp.boxc(t0, y0, z0, t1, y1, z1, inner_m)
                else:
                    x0, x1 = (0, WALL_T) if side == "W" else (W - WALL_T, W)
                    wp.boxc(x0, t0, z0, x1, t1, z1, inner_m)
            wp.finish()
            self.wall_pieces[side] = wp.name
            # 門框 / 窗框 / 玻璃
            fp = Piece(self, "Frames_" + side, coll="STRUCTURE")
            for (a, b, z0, z1, kind) in ops:
                ft = 0.05
                if side in "SN":
                    y0, y1 = (0, WALL_T) if side == "S" else (D - WALL_T, D)
                    yc = (y0 + y1) / 2
                    fp.boxc(a - ft, y0 - 0.01, z0, a, y1 + 0.01, z1, frame)
                    fp.boxc(b, y0 - 0.01, z0, b + ft, y1 + 0.01, z1, frame)
                    fp.boxc(a - ft, y0 - 0.01, z1, b + ft, y1 + 0.01, z1 + ft, frame)
                    if kind == "window":
                        fp.boxc(a - ft, y0 - 0.01, z0 - ft, b + ft, y1 + 0.01, z0, frame)
                        fp.boxc(a, yc - 0.01, z0, b, yc + 0.01, z1, glass)
                else:
                    x0, x1 = (0, WALL_T) if side == "W" else (W - WALL_T, W)
                    xc = (x0 + x1) / 2
                    fp.boxc(x0 - 0.01, a - ft, z0, x1 + 0.01, a, z1, frame)
                    fp.boxc(x0 - 0.01, b, z0, x1 + 0.01, b + ft, z1, frame)
                    fp.boxc(x0 - 0.01, a - ft, z1, x1 + 0.01, b + ft, z1 + ft, frame)
                    if kind == "window":
                        fp.boxc(x0 - 0.01, a - ft, z0 - ft, x1 + 0.01, b + ft, z0, frame)
                        fp.boxc(xc - 0.01, a, z0, xc + 0.01, b, z1, glass)
            if fp.bm.verts:
                fp.finish()
            else:
                fp.bm.free()
        # 門 empties
        for d in self.doors:
            cx, cy = self._pos_on_wall(d["wall"], d["offset_m"])
            yaw = {"S": 0, "N": 180, "W": -90, "E": 90}[d["wall"]]  # 朝室內
            d["position"] = [round(cx, 3), round(cy, 3), 0.0]
            e = self._empty(d["id"], cx, cy, 0.0, yaw, display="CUBE", size=0.25,
                            props={"width_m": d["width_m"], "height_m": DOOR_H, "wall": d["wall"], "offset_m": d["offset_m"]})
            self.door_objs.append(e)
            # 導航：門口通道（從房間外緣到牆內側 + 邊距）
            w2 = 0.5
            if d["wall"] in "SN":
                y0, y1 = (0, WALL_T + NAV_MARGIN + 0.05) if d["wall"] == "S" else (D - WALL_T - NAV_MARGIN - 0.05, D)
                self.extra_free.append((d["offset_m"] - w2, y0, d["offset_m"] + w2, y1))
            else:
                x0, x1 = (0, WALL_T + NAV_MARGIN + 0.05) if d["wall"] == "W" else (W - WALL_T - NAV_MARGIN - 0.05, W)
                self.extra_free.append((x0, d["offset_m"] - w2, x1, d["offset_m"] + w2))
        return self

    # ---------- 燈具
    def ceiling_panel(self, x, y, w=1.2, d=0.6, power=250, name=None):
        p = Piece(self, name or "LightPanel_%02d" % self._next("lp"), x, y, self.H - 0.03, coll="LIGHTS")
        p.box(0, 0, 0, w, d, 0.04, "frame")
        p.box(0, 0, -0.021, w - 0.08, d - 0.08, 0.01, mat("light_emit", (1, 0.97, 0.9), emit=(1, 0.95, 0.85)))
        p.finish()
        ld = bpy.data.lights.new("Area_%02d" % self._counters["lp"], "AREA")
        ld.energy, ld.shape, ld.size, ld.size_y = power, "RECTANGLE", w, d
        lo = bpy.data.objects.new("AreaLight_%02d" % self._counters["lp"], ld)
        lo.location = (x, y, self.H - 0.1)
        self.coll["LIGHTS"].objects.link(lo)

    def light_grid(self, nx, ny, margin=1.5, w=1.2, d=0.6, power=250):
        xs = [margin + (self.W - 2 * margin) * (i + 0.5) / nx for i in range(nx)]
        ys = [margin * 0.7 + (self.D - 1.4 * margin * 0.7) * (j + 0.5) / ny for j in range(ny)]
        for x in xs:
            for y in ys:
                self.ceiling_panel(x, y, w, d, power)

    # ---------- 導航網格
    def _inflated_free(self, x, y):
        for (cx, cy, yaw, w, d) in self.obstacles:
            c, s = math.cos(-yaw), math.sin(-yaw)
            dx, dy = x - cx, y - cy
            u, v = dx * c - dy * s, dx * s + dy * c
            if abs(u) <= w / 2 + NAV_MARGIN and abs(v) <= d / 2 + NAV_MARGIN:
                return False
        return True

    def build_navmesh(self):
        lo = WALL_T + NAV_MARGIN
        n = NAV_CELL
        nx, ny = int(round((self.W - 2 * lo) / n)), int(round((self.D - 2 * lo) / n))
        free = {}
        for i in range(nx):
            for j in range(ny):
                x, y = lo + (i + 0.5) * n, lo + (j + 0.5) * n
                free[(i, j)] = self._inflated_free(x, y)
        # 門口通道（可延伸到房間外緣）
        extra = {}
        for (x0, y0, x1, y1) in self.extra_free:
            i0, i1 = int(round((x0 - lo) / n)), int(round((x1 - lo) / n))
            j0, j1 = int(round((y0 - lo) / n)), int(round((y1 - lo) / n))
            for i in range(i0, i1):
                for j in range(j0, j1):
                    extra[(i, j)] = True
        for (i, j) in extra:
            free[(i, j)] = True
        verts, idx, faces = [], {}, []

        def vid(i, j):
            if (i, j) not in idx:
                idx[(i, j)] = len(verts)
                verts.append((lo + i * n, lo + j * n, 0.0))
            return idx[(i, j)]
        count = 0
        for (i, j), ok in free.items():
            if ok:
                faces.append((vid(i, j), vid(i + 1, j), vid(i + 1, j + 1), vid(i, j + 1)))
                count += 1
        mesh = bpy.data.meshes.new("NAVMESH")
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        mesh.materials.append(mat("nav", alpha=0.5))
        obj = bpy.data.objects.new("NAVMESH", mesh)
        self.coll["NAV"].objects.link(obj)
        self.nav_cells = count
        return obj

    # ---------- 輸出
    def _scene_json(self):
        return {
            "id": self.id, "name_zh": self.name_zh, "name_en": self.name_en, "category": self.category,
            "size_m": [self.W, self.D], "height_m": self.H,
            "doors": [{"id": d["id"], "wall": d["wall"], "offset_m": d["offset_m"], "width_m": d["width_m"],
                       "position": d["position"]} for d in self.doors],
            "anchors": self.anchors, "tags": self.tags,
            "nav": {"file": "navmesh.glb", "cell_m": NAV_CELL, "margin_m": NAV_MARGIN, "cells": self.nav_cells},
            "files": {"blend": "scene.blend", "glb": "scene.glb", "navmesh": "navmesh.glb",
                      "preview": "preview.png", "plan": "plan.png", "build": "build.py"},
            "coord": "Blender Z-up, +Y north, SW corner origin; glb is glTF Y-up (gx=x, gy=z, gz=-y)",
            "created": datetime.date.today().isoformat(),
        }

    def add_camera_and_sun(self):
        cam = bpy.data.cameras.new("Camera")
        cam.type = "ORTHO"
        co = bpy.data.objects.new("Camera_Iso", cam)
        self.scene.collection.objects.link(co)
        self.scene.camera = co
        sun = bpy.data.lights.new("Sun", "SUN")
        sun.energy = 1.6
        sun.angle = math.radians(8)
        so = bpy.data.objects.new("Sun", sun)
        so.rotation_euler = (math.radians(50), math.radians(10), math.radians(-35))
        so.location = (self.W / 2, self.D / 2, 10)
        self.coll["LIGHTS"].objects.link(so)
        self.cam = co

    def _cam_iso(self, aspect=16 / 9, elev=42, azim=45, margin=1.08):
        W, D, H = self.W, self.D, self.H
        tgt = Vector((W / 2, D / 2, 0.9))
        az, el = math.radians(azim), math.radians(elev)
        # 相機位於西南方：方向向量（目標指向相機）
        dirv = Vector((-math.sin(az), -math.cos(az), 0)) * math.cos(el) + Vector((0, 0, math.sin(el)))
        self.cam.location = tgt + dirv * 60
        self.cam.rotation_euler = (-dirv).to_track_quat("-Z", "Y").to_euler()
        # 投影範圍
        right = Vector((math.cos(az), -math.sin(az), 0))
        up = right.cross(-dirv).normalized()
        up = (-dirv).cross(right)
        pts = [Vector((x, y, z)) for x in (0, W) for y in (0, D) for z in (0, H)]
        us = [(p - tgt).dot(right) for p in pts]
        vs = [(p - tgt).dot(up) for p in pts]
        wu, hv = max(us) - min(us), max(vs) - min(vs)
        self.cam.data.ortho_scale = max(wu, hv * aspect) * margin
        # 平移鏡頭以置中投影範圍
        cu, cv = (max(us) + min(us)) / 2, (max(vs) + min(vs)) / 2
        self.cam.location += right * cu + up * cv
        self.cam.data.clip_start, self.cam.data.clip_end = 0.1, 200

    def _render(self, path, w, h, samples, engine="CYCLES"):
        sc = self.scene
        sc.render.engine = engine
        sc.render.resolution_x, sc.render.resolution_y = w, h
        sc.render.resolution_percentage = 100
        sc.render.filepath = path
        sc.render.image_settings.file_format = "PNG"
        if engine == "CYCLES":
            sc.cycles.device = "CPU"
            sc.cycles.samples = samples
            sc.cycles.use_denoising = True
            sc.cycles.max_bounces = 4
        sc.view_settings.view_transform = "Standard"
        bpy.ops.render.render(write_still=True)

    def _world(self, strength=0.45, color=(0.82, 0.88, 1.0)):
        w = bpy.data.worlds.new("World")
        w.use_nodes = True
        bg = w.node_tree.nodes["Background"]
        bg.inputs["Color"].default_value = (*color, 1)
        bg.inputs["Strength"].default_value = strength
        self.scene.world = w

    def _export(self, path, selection=None, visible_only=False):
        bpy.ops.object.select_all(action="DESELECT")
        kw = dict(filepath=path, export_format="GLB", export_apply=True, export_extras=True,
                  export_cameras=False, export_lights=False, export_yup=True)
        if visible_only:
            kw["use_visible"] = True
        if selection is not None:
            for o in selection:
                o.select_set(True)
            kw["use_selection"] = True
        bpy.ops.export_scene.gltf(**kw)

    def finish(self, out_dir, preview_samples=48, render=True, hide_near=("S", "W"), plan_px_per_m=60, cam_elev=42, cam_azim=45):
        os.makedirs(out_dir, exist_ok=True)
        navobj = self.build_navmesh()
        self.add_camera_and_sun()
        self._world()
        with open(os.path.join(out_dir, "scene.json"), "w", encoding="utf-8") as f:
            json.dump(self._scene_json(), f, ensure_ascii=False, indent=2)
        bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out_dir, "scene.blend"))
        # scene.glb：排除 NAV
        vl = bpy.context.view_layer
        lc = {c.name: c for c in vl.layer_collection.children}
        navobj.hide_set(True)
        self._export(os.path.join(out_dir, "scene.glb"), visible_only=True)
        navobj.hide_set(False)
        self._export(os.path.join(out_dir, "navmesh.glb"), selection=[navobj])
        if not render:
            return
        # 預覽：隱藏天花板與近側牆（剖視），Cycles 等角
        hide = ["Ceiling"] + ["Wall_" + s for s in hide_near] + ["Frames_" + s for s in hide_near]
        for n in hide:
            if n in bpy.data.objects:
                bpy.data.objects[n].hide_render = True
        for o in bpy.data.objects:
            if o.name.startswith("LightPanel_"):
                o.hide_render = True
        navobj.hide_render = True
        self._cam_iso(elev=cam_elev, azim=cam_azim)
        self._render(os.path.join(out_dir, "preview.png"), 1280, 720, preview_samples)
        # 平面圖：正交頂視 + PIL 標註
        self._plan(out_dir, plan_px_per_m)

    def _plan(self, out_dir, ppm):
        pad = 1.0
        W, D = self.W, self.D
        px_w, px_h = int((W + 2 * pad) * ppm), int((D + 2 * pad) * ppm)
        for o in bpy.data.objects:
            if o.name.startswith(("Wall_", "Frames_")):
                o.hide_render = False
        cam = self.cam
        cam.data.ortho_scale = max(W + 2 * pad, (D + 2 * pad) * px_w / px_h)
        cam.location = (W / 2, D / 2, 30)
        cam.rotation_euler = (0, 0, 0)
        # 若寬高比 ≠ 1，ortho_scale 以較長邊為準
        sc = self.scene
        sc.render.engine = "CYCLES"
        sc.cycles.device, sc.cycles.samples, sc.cycles.use_denoising = "CPU", 12, True
        sc.render.resolution_x, sc.render.resolution_y = px_w, px_h
        sc.render.filepath = os.path.join(out_dir, "_plan_raw.png")
        sc.view_settings.view_transform = "Standard"
        sc.render.film_transparent = False
        sc.world.color = (0.97, 0.97, 0.97)
        bpy.ops.render.render(write_still=True)
        from PIL import Image, ImageDraw, ImageFont
        img = Image.open(os.path.join(out_dir, "_plan_raw.png")).convert("RGB")
        os.remove(os.path.join(out_dir, "_plan_raw.png"))
        s = float(ppm)
        cx0, cy0 = px_w / 2, px_h / 2

        def P(x, y):
            return (cx0 + (x - W / 2) * s, cy0 - (y - D / 2) * s)
        dr = ImageDraw.Draw(img, "RGBA")
        try:
            f = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 13)
            fb = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", 20)
        except Exception:
            f = fb = ImageFont.load_default()
        # 2 m 網格
        for gx in range(0, W + 1, 2):
            dr.line([P(gx, 0), P(gx, D)], fill=(0, 0, 0, 40), width=1)
        for gy in range(0, D + 1, 2):
            dr.line([P(0, gy), P(W, gy)], fill=(0, 0, 0, 40), width=1)
        colors = {"SEAT": (220, 40, 40), "STAND": (30, 90, 220), "POI": (230, 150, 0), "STATUS": (140, 60, 200)}
        for d in self.doors:
            x, y = d["position"][0], d["position"][1]
            hw = d["width_m"] / 2
            if d["wall"] in "SN":
                a, b = P(x - hw, y), P(x + hw, y)
            else:
                a, b = P(x, y - hw), P(x, y + hw)
            dr.line([a, b], fill=(0, 170, 80, 255), width=8)
            dr.text((P(x, y)[0] + 6, P(x, y)[1] - 18 if d["wall"] != "N" else P(x, y)[1] + 4), d["id"].replace("DOOR_", "D_"), fill=(0, 120, 50), font=f)
        for a in self.anchors:
            if a["type"] == "STATUS":
                continue
            x, y = a["position"][0], a["position"][1]
            px, py = P(x, y)
            col = colors[a["type"]]
            r = 7
            dr.ellipse([px - r, py - r, px + r, py + r], fill=col + (200,), outline=(255, 255, 255, 255))
            yaw = math.radians(a["yaw_deg"])
            fx, fy = -math.sin(yaw), math.cos(yaw)
            dr.line([(px, py), (px + fx * 20, py - fy * 20)], fill=col + (255,), width=3)
            lab = a["id"].replace("SEAT_", "S").replace("STAND_", "T").replace("POI_", "P")
            if a["type"] == "SEAT":
                lab = a["id"].split("_")[-1]
            dr.text((px + 8, py + 5), lab, fill=(20, 20, 20), font=f)
        dr.rectangle([0, 0, px_w, 34], fill=(255, 255, 255, 230))
        dr.text((10, 5), "%s %s  %s  %d×%d m  H=%.1f m" % (self.id, self.name_zh, self.name_en, W, D, self.H), fill=(0, 0, 0), font=fb)
        lg = [("SEAT", "坐下點"), ("STAND", "站立點"), ("POI", "互動點")]
        x0 = px_w - 330
        for k, (t, z) in enumerate(lg):
            xx = x0 + k * 105
            dr.ellipse([xx, 10, xx + 12, 22], fill=colors[t] + (255,))
            dr.text((xx + 16, 6), z, fill=(0, 0, 0), font=f)
        dr.line([(x0 - 70, 16), (x0 - 52, 16)], fill=(0, 170, 80), width=6)
        dr.text((x0 - 48, 6), "門", fill=(0, 0, 0), font=f)
        img.save(os.path.join(out_dir, "plan.png"))
