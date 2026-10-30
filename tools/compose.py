"""把多個場景依 layout.json 組合成一層樓的 .blend / .glb / .json。
用法：python3 tools/compose.py compose/layout.json
layout.json：{"name":..., "tiles":[{"scene":"001_open_office","offset":[x,y],"rot":0|90|180|270}]}
offset 為該場景「旋轉後外框」西南角的位置（須為 2 m 倍數）；旋轉繞原場景 SW 角，之後自動平移使外框落在 offset。
輸出：compose/<name>.blend、<name>.glb、<name>.json（合併後的門／錨點／警告，含門對齊檢查）、<name>_navmesh.glb。"""
import sys, os, json, math
import bpy
from mathutils import Matrix, Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def rot_pt(p, rot, W, D):
    """場景座標 → 旋轉並平移到外框 SW 角 (0,0) 的座標。"""
    x, y = p[0], p[1]
    r = rot % 360
    if r == 0:
        return x, y
    if r == 90:
        return D - y, x
    if r == 180:
        return W - x, D - y
    if r == 270:
        return y, W - x
    raise ValueError("rot 必須為 0/90/180/270")


def footprint(W, D, rot):
    return (D, W) if rot % 180 else (W, D)


def main(layout_path):
    lay = json.load(open(layout_path, encoding="utf-8"))
    name = lay["name"]
    out = os.path.dirname(os.path.abspath(layout_path))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    root_c = bpy.data.collections.new("FLOOR")
    sc.collection.children.link(root_c)
    nav_c = bpy.data.collections.new("NAV")
    sc.collection.children.link(nav_c)
    doors, anchors, warns, rects, tiles_out = [], [], [], [], []
    navs = []
    for ti, t in enumerate(lay["tiles"]):
        sd = os.path.join(ROOT, "scenes", t["scene"])
        sj = json.load(open(os.path.join(sd, "scene.json"), encoding="utf-8"))
        W, D = sj["size_m"]
        rot = int(t.get("rot", 0))
        ox, oy = t["offset"]
        if ox % 2 or oy % 2:
            warns.append("tile %d offset 不在 2 m 網格" % ti)
        fw, fd = footprint(W, D, rot)
        for (a, b, c, d) in rects:
            if ox < a + c and a < ox + fw and oy < b + d and b < oy + fd:
                warns.append("tile %d (%s) 與先前場景重疊" % (ti, t["scene"]))
        rects.append((ox, oy, fw, fd))
        # 轉換矩陣：先繞原點旋轉，再平移 (旋轉後 SW 角 → offset)
        sh = {0: (0, 0), 90: (D, 0), 180: (W, D), 270: (0, W)}[rot % 360]
        T = Matrix.Translation((ox + sh[0], oy + sh[1], 0)) @ Matrix.Rotation(math.radians(rot), 4, "Z")
        for glb, coll, tag in (("scene.glb", root_c, ""), ("navmesh.glb", nav_c, "nav")):
            before = set(bpy.data.objects)
            bpy.ops.import_scene.gltf(filepath=os.path.join(sd, glb))
            new = [o for o in bpy.data.objects if o not in before]
            roots = [o for o in new if o.parent is None]
            for o in new:
                for c in list(o.users_collection):
                    c.objects.unlink(o)
                coll.objects.link(o)
                o.name = "T%02d_%s" % (ti, o.name)
            for r in roots:
                r.matrix_world = T @ r.matrix_world
            if tag == "nav":
                navs += [o for o in new if o.type == "MESH"]
        for dr in sj["doors"]:
            x, y = rot_pt(dr["position"], rot, W, D)
            wall = {"S": "S", "E": "E", "N": "N", "W": "W"}[dr["wall"]]
            wall = "SENW"[("SENW".index(wall) + rot // 90) % 4]  # S→E→N→W 依逆時針旋轉
            doors.append({"id": "T%02d_%s" % (ti, dr["id"]), "tile": ti, "scene": t["scene"], "wall": wall,
                          "width_m": dr["width_m"], "position": [round(ox + x, 3), round(oy + y, 3), 0.0]})
        for a in sj["anchors"]:
            x, y = rot_pt(a["position"], rot, W, D)
            anchors.append({**a, "id": "T%02d_%s" % (ti, a["id"]), "tile": ti,
                            "position": [round(ox + x, 3), round(oy + y, 3), a["position"][2]],
                            "yaw_deg": ((a["yaw_deg"] + rot + 180) % 360) - 180})
        tiles_out.append({"scene": t["scene"], "offset": [ox, oy], "rot": rot, "size_m": [fw, fd]})
    # 門對齊檢查：兩個不同 tile 且位置相距 < 0.6 m 視為已連通；單獨在樓層外緣的門不算錯
    connected = 0
    for i, a in enumerate(doors):
        for b in doors[i + 1:]:
            if a["tile"] != b["tile"]:
                dd = math.hypot(a["position"][0] - b["position"][0], a["position"][1] - b["position"][1])
                if dd < 0.5 + 0.2 * 2:  # 牆厚各 0.2，中心線相距 0.2~0.4 m
                    connected += 1
    info = {"name": name, "tiles": tiles_out, "doors": doors, "anchors": anchors, "connected_door_pairs": connected,
            "warnings": warns}
    json.dump(info, open(os.path.join(out, name + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out, name + ".blend"))
    # glb（排除 NAV）與合併導航 glb
    for o in navs:
        o.hide_set(True)
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, name + ".glb"), export_format="GLB", export_apply=True,
                              export_extras=True, export_cameras=False, export_lights=False, use_visible=True)
    for o in navs:
        o.hide_set(False)
        o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, name + "_navmesh.glb"), export_format="GLB",
                              export_extras=True, use_selection=True)
    print("組合完成：%s tiles=%d doors=%d anchors=%d 連通門=%d 警告=%s" % (name, len(tiles_out), len(doors), len(anchors), connected, warns))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "compose", "layout.json"))
