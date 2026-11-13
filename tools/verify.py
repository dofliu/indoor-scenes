"""驗證場景輸出：python3 tools/verify.py scenes/<id_slug>
檢查：glb 可重新讀入、錨點數量與 scene.json 一致、門洞位置/奇數公尺規格、導航網格、檔案大小。"""
import sys, os, json, math
import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree


def fail(msg):
    print("FAIL:", msg)
    global bad
    bad += 1


bad = 0
d = os.path.abspath(sys.argv[1])
sj = json.load(open(os.path.join(d, "scene.json"), encoding="utf-8"))
W, D, H = sj["size_m"][0], sj["size_m"][1], sj["height_m"]
if W % 2 or D % 2:
    fail("尺寸非 2 m 倍數")
if H != 3.0:
    fail("樓高非 3.0")
for f in ("scene.blend", "scene.glb", "navmesh.glb", "scene.json", "preview.png", "plan.png", "build.py"):
    p = os.path.join(d, f)
    if not os.path.exists(p):
        fail("缺檔 " + f)
    else:
        print("  %-12s %8.1f KB" % (f, os.path.getsize(p) / 1024))
if os.path.getsize(os.path.join(d, "scene.glb")) > 8 * 1024 * 1024:
    fail("scene.glb > 8MB")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(d, "scene.glb"))
objs = list(bpy.data.objects)
names = {o.name.split(".")[0] if o.name[-4:-3] == "." else o.name: o for o in objs}
anch = [a for a in sj["anchors"]]
for a in anch:
    o = names.get(a["id"])
    if o is None:
        fail("glb 缺錨點 " + a["id"])
        continue
    p = o.matrix_world.translation
    if (p - Vector(a["position"])).length > 0.01:
        fail("錨點位置不符 %s %s vs %s" % (a["id"], tuple(p), a["position"]))
n_glb = len([o for o in objs if o.type == "EMPTY" and o.name.split(".")[0].split("_")[0] in ("SEAT", "STAND", "POI", "STATUS")])
print("  錨點 json=%d glb=%d" % (len(anch), n_glb))
if n_glb != len(anch):
    fail("錨點數量不一致")
if any(o.name.startswith("NAVMESH") for o in objs):
    fail("scene.glb 不應含 NAVMESH")
# 門
walls = [o for o in objs if o.type == "MESH" and o.name.startswith("Wall_")]
bm_v, bm_f = [], []
for o in walls:
    me = o.data
    base = len(bm_v)
    bm_v += [o.matrix_world @ v.co for v in me.vertices]
    bm_f += [tuple(base + i for i in p.vertices) for p in me.polygons]
bvh = BVHTree.FromPolygons(bm_v, bm_f)
for dr in sj["doors"]:
    if dr["offset_m"] % 2 != 1:
        fail("門偏移非奇數 " + dr["id"])
    o = names.get(dr["id"])
    if o is None:
        fail("glb 缺門 " + dr["id"])
        continue
    x, y, _ = dr["position"]
    w, off = dr["wall"], dr["offset_m"]
    nrm = {"S": (0, 1), "N": (0, -1), "W": (1, 0), "E": (-1, 0)}[w]
    for z, expect_clear in ((1.0, True), (2.1, True), (2.3, False)):
        for dt, clear in ((0, expect_clear), (0.8, False)):
            if dt and z == 2.3:
                continue
            px, py = x, y
            if w in "SN":
                px = x + dt
            else:
                py = y + dt
            org = Vector((px - nrm[0] * 1.0, py - nrm[1] * 1.0, z))
            hit = bvh.ray_cast(org, Vector((nrm[0], nrm[1], 0)), 1.5)[0] is not None
            if hit == clear:
                fail("門洞檢查 %s dt=%s z=%s hit=%s" % (dr["id"], dt, z, hit))
    print("  門 %s 位置=%s 寬=%s OK" % (dr["id"], dr["position"], dr["width_m"]))
# 導航
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(d, "navmesh.glb"))
nm = [o for o in bpy.data.objects if o.type == "MESH"]
if len(nm) != 1:
    fail("navmesh.glb 物件數 != 1")
else:
    vs = [nm[0].matrix_world @ v.co for v in nm[0].data.vertices]
    if any(abs(v.z) > 1e-4 or v.x < -1e-4 or v.y < -1e-4 or v.x > W + 1e-4 or v.y > D + 1e-4 for v in vs):
        fail("navmesh 超出範圍或不在 z=0")
    print("  navmesh 頂點=%d 面=%d" % (len(vs), len(nm[0].data.polygons)))
    elevated = 0
    for a in sj["anchors"]:
        if a["type"] in ("SEAT", "STAND", "POI"):
            ax, ay = a["position"][:2]
            dmin = min(math.hypot(v.x - ax, v.y - ay) for v in vs)
            if a["position"][2] > 0.05:
                # 高架錨點（階梯座位、舞台等，z 為腳底高度）：不在 z=0 導航網格上，由最近導航點直接移動過去
                if dmin > 3.0:
                    fail("高架錨點離導航網格過遠 %s %.2f m" % (a["id"], dmin))
                elevated += 1
            elif dmin > 0.4:
                fail("錨點離導航網格過遠 %s %.2f m" % (a["id"], dmin))
if 'elevated' in dir() and elevated:
    print("  高架錨點=%d（z>0，距導航網格 ≤ 3.0 m）" % elevated)
print("RESULT:", "PASS" if bad == 0 else "FAIL x%d" % bad)
sys.exit(1 if bad else 0)
