"""場景 022：控制室／中控室（風場 SCADA 中控）。
北牆 5×2 拼接螢幕牆（風場總覽圖、單線圖、出力趨勢、警報清單、海象）、弧形排列 5 席值班操作台、
後排值班主任台＋2 席工程師台、東牆控制盤櫃列（PLC／保護電驛／通訊）、無線電通訊席、警報窗、交接班站桌。
執行：python3.13 build.py（需 pip install bpy）"""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from scenelib import *
import furniture as F

S = Scene("022", "scada_control_room", "控制室／中控室（風場 SCADA 中控）", "SCADA Control Room (Wind Farm)", "office", (14, 10),
          tags=["control-room", "scada", "wind-farm", "video-wall", "console", "monitoring", "24x7"])
R = math.radians

S.add_door("S", 11)     # 主入口
S.add_door("W", 3)      # 通往辦公區／走廊
S.add_door("E", 5)      # 通往設備機房
S.build_shell(floor="floor_carpet", wall="wall", accent={"N": "wall_dark", "E": "wall_dark"})
S.light_grid(3, 2, power=80)

# ---- 北牆：SCADA 拼接螢幕牆（8.0×1.8 m）＋時區時鐘列＋站位
F.scada_wall(S, 7.0, 9.8, 0, cols=5, rows=2, tw=1.6, th=0.9, z=0.85)
F.digital_clock(S, 7.0, 9.8, 0, z=2.77, n=3)
S.anchor("STAND", "wall", 4.6, 8.9, 0, n=1)
S.anchor("STAND", "wall", 9.4, 8.9, 0, n=2)
# 螢幕牆兩側：警報窗（西）與 CCTV 顯示幕（東）
F.annunciator_panel(S, 1.7, 9.8, 0, name="Annunciator")
S.anchor("STAND", "annunciator", 1.7, 8.95, 0, n=1)
F.screen_wall(S, 12.1, 9.8, 1.4, h=0.8, yaw=0, z=1.4, name="CCTVDisplay")

# ---- 弧形值班操作台 5 席（圓心在螢幕牆後方，全部面向牆面中央）
ARC_C, ARC_R = (7.0, 12.6), 6.0
ROLES = [("turbine_west", "風機監控（西區）"), ("turbine_east", "風機監控（東區）"), ("grid", "電網調度／併網點"),
         ("substation", "海上變電站／海纜"), ("marine", "海事協調／船舶人員")]
consoles = []
n = 0
for a, (role, role_zh) in zip((-32, -16, 0, 16, 32), ROLES):
    n += 1
    ar = R(a)
    cx, cy = ARC_C[0] + ARC_R * math.sin(ar), ARC_C[1] - ARC_R * math.cos(ar)
    fx, fy = -math.sin(ar), math.cos(ar)                       # 面向
    F.control_console(S, cx, cy, ar, w=1.6, d=0.85, screens=3, name="OperatorConsole_%02d" % n)
    sx, sy = cx - 0.85 * fx, cy - 0.85 * fy
    F.chair(S, sx, sy, ar, color="chair_seat", name="OperatorChair_%02d" % n)
    seat = S.anchor("SEAT", "operator", sx, sy, a, n=n)
    st = S.anchor("STATUS", "", cx - 0.3 * fx, cy - 0.3 * fy, n=n)
    F.pendant_status_lamp(S, cx - 0.3 * fx, cy - 0.3 * fy, z=2.2, name="StatusPendant_%02d" % n,
                          color=(0.95, 0.65, 0.1) if n == 4 else (0.2, 0.9, 0.3))
    consoles.append({"id": "OP%d" % n, "role": role, "role_zh": role_zh, "object": "OperatorConsole_%02d" % n,
                     "seat": seat, "status_anchor": st})

# ---- 後排：值班主任台（中央，較寬）＋兩側工程師台
F.control_console(S, 7.0, 4.0, 0, w=2.2, d=0.9, screens=3, name="SupervisorDesk")
F.chair(S, 7.0, 3.1, 0, color="chair_red", name="SupervisorChair")
F.hotline_phone(S, 7.85, 3.8, 0, name="HotlinePhone")
seat = S.anchor("SEAT", "supervisor", 7.0, 3.1, 0, n=1)
st = S.anchor("STATUS", "", 7.0, 3.7, n=6)
F.pendant_status_lamp(S, 7.0, 3.7, z=2.2, name="StatusPendant_06", color=(0.2, 0.6, 1.0))
consoles.append({"id": "SUP", "role": "shift_supervisor", "role_zh": "值班主任", "object": "SupervisorDesk",
                 "seat": seat, "status_anchor": st})
for k, (ex, a, role, role_zh) in enumerate(((3.7, -12, "forecast", "發電預測／氣象"), (10.3, 12, "maintenance", "運維排程／工單")), 1):
    ar = R(a)
    fx, fy = -math.sin(ar), math.cos(ar)
    F.control_console(S, ex, 4.2, ar, w=1.6, d=0.85, screens=2, name="EngineerDesk_%02d" % k)
    sx, sy = ex - 0.85 * fx, 4.2 - 0.85 * fy
    F.chair(S, sx, sy, ar, color="chair_green", name="EngineerChair_%02d" % k)
    seat = S.anchor("SEAT", "engineer", sx, sy, a, n=k)
    st = S.anchor("STATUS", "", ex - 0.3 * fx, 4.2 - 0.3 * fy, n=6 + k)
    F.pendant_status_lamp(S, ex - 0.3 * fx, 4.2 - 0.3 * fy, z=2.2, name="StatusPendant_%02d" % (6 + k))
    consoles.append({"id": "ENG%d" % k, "role": role, "role_zh": role_zh, "object": "EngineerDesk_%02d" % k,
                     "seat": seat, "status_anchor": st})

# ---- 東牆北段：控制盤櫃列（正面朝西）
EX = 13.8 - 0.30
for k, (cy, kind) in enumerate(((6.4, "plc"), (7.2, "relay"), (8.0, "relay"), (8.8, "comm")), 1):
    F.control_cabinet(S, EX, cy, R(-90), kind=kind, name="ControlCabinet_%02d" % k)
S.anchor("STAND", "cabinet", 12.55, 6.8, -90, n=1)
S.anchor("STAND", "cabinet", 12.55, 8.4, -90, n=2)

# ---- 東牆南段：無線電通訊席（面向東）＋牆上氣象／海象顯示幕＋角落 UPS
F.desk(S, 13.43, 2.4, R(-90), w=1.6, d=0.7, top="desk_white", name="RadioDesk")
F.chair(S, 12.6, 2.4, R(-90), color="chair_seat", name="RadioChair")
F.radio_base(S, 13.5, 2.85, R(-90), name="RadioBase")
F.monitor(S, 13.58, 2.15, R(-90), name="RadioMonitor")
F.keyboard(S, 13.25, 2.15, R(-90), name="RadioKeyboard")
F.screen_wall(S, 13.8, 2.4, 1.3, h=0.75, yaw=R(-90), z=1.55, name="WeatherDisplay")
seat = S.anchor("SEAT", "radio", 12.6, 2.4, -90, n=1)
st = S.anchor("STATUS", "", 13.1, 2.4, n=9)
F.pendant_status_lamp(S, 13.1, 2.4, z=2.2, name="StatusPendant_09")
consoles.append({"id": "RADIO", "role": "radio_operator", "role_zh": "無線電通訊", "object": "RadioDesk",
                 "seat": seat, "status_anchor": st})
F.ups_cabinet(S, 13.38, 0.62, R(-90), name="UPS")
S.anchor("POI", "ups", 12.45, 0.75, -90, n=1)

# ---- 西牆：交接班白板、飲水機
F.whiteboard(S, 0.2, 6.2, R(90), w=2.0, name="HandoverBoard")
S.anchor("STAND", "whiteboard", 0.95, 6.2, 90, n=1)
F.water_dispenser(S, 0.42, 1.2, R(90), name="WaterDispenser")
S.anchor("POI", "water", 1.15, 1.2, 90, n=1)

# ---- 南側：交接班站桌、值班日誌矮櫃、事務機
F.round_table(S, 3.0, 1.9, r=0.55, h=1.05, name="HandoverTable")
S.anchor("STAND", "handover", 2.05, 1.9, -90, n=1)
S.anchor("STAND", "handover", 3.95, 1.9, 90, n=2)
S.anchor("STAND", "handover", 3.0, 2.85, 180, n=3)
for i in range(2):
    F.cabinet(S, 5.6 + 0.9 * i, 0.2 + 0.225, R(180), h=0.9, name="Credenza_%d" % (i + 1))
F.logbook(S, 5.75, 0.45, R(180), z=0.9, name="Logbook")
S.anchor("POI", "logbook", 5.9, 1.3, 180, n=1)
F.printer(S, 8.3, 0.2 + 0.36, R(180), name="Printer")
S.anchor("POI", "printer", 8.3, 1.45, 180, n=1)
for (px, py) in ((0.65, 9.35), (1.7, 0.65), (9.6, 0.65)):
    F.plant(S, px, py)

S.extra_json["consoles"] = consoles
S.extra_json["displays"] = [
    {"object": "ScadaWall", "kind": "video_wall", "size_m": [8.0, 1.8], "wall": "N",
     "content": ["wind_rose", "farm_overview(24 turbines, 3 strings, offshore substation)", "alarm_list",
                 "power_trend", "single_line_diagram", "total_output", "turbine_matrix", "sea_state"]},
    {"object": "Annunciator", "kind": "annunciator", "wall": "N", "windows": [6, 5]},
    {"object": "CCTVDisplay", "kind": "screen", "wall": "N"},
    {"object": "WeatherDisplay", "kind": "screen", "wall": "E"},
]

# 控制室偏暗：壓低曝光讓螢幕與狀態燈突出
S.scene.view_settings.exposure = -1.0
S.finish(HERE)
