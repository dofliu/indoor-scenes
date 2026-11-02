# DofLab 室內場景模組庫（indoor-scenes）

以 Blender（bpy）程序化建模的**室內場景模組庫**：每個模組遵守統一規格（2 m 網格、3 m 樓高、奇數公尺門洞、命名錨點、導航網格），
可任意拼接成一層樓，也可匯入 Three.js / Unity / Godot 讓人物在其中移動。詳見 [SPEC.md](SPEC.md)。

**目前場景數：4**　｜　待做清單：[backlog.md](backlog.md)　｜　清單資料：[catalog.json](catalog.json)

## 場景一覽

| # | 場景 | 尺寸 | 門 | 錨點 | 預覽 |
|---|---|---|---|---|---|
| 001 | [開放式工位辦公區](scenes/001_open_office/) | 16×12 m | 5 | 45（16 工位＋4 協作座） | <img src="scenes/001_open_office/preview.png" width="360"> |
| 002 | [中型會議室](scenes/002_meeting_room/) | 8×6 m | 2 | 18（12 座位＋白板／簡報／飲水點） | <img src="scenes/002_meeting_room/preview.png" width="360"> |
| 003 | [小型討論室／電話亭](scenes/003_huddle_room/) | 4×4 m | 2 | 9（4 討論座＋電話亭 1 座＋白板／螢幕） | <img src="scenes/003_huddle_room/preview.png" width="360"> |
| 004 | [茶水間／咖啡吧](scenes/004_pantry/) | 8×6 m | 3 | 18（6 吧凳＋4 小圓桌座＋流理台／咖啡機／冰箱／販賣機互動點） | <img src="scenes/004_pantry/preview.png" width="360"> |

## 目錄
```
scenes/<NNN>_<slug>/   scene.blend / scene.glb / navmesh.glb / scene.json / preview.png / plan.png / build.py
tools/scenelib.py      共用：牆、地板、門窗洞、燈、錨點、導航網格、輸出與渲染
tools/furniture.py     共用：桌椅、螢幕、櫃、白板、沙發、影印機等參數化家具
tools/verify.py        驗證某場景輸出（glb 重讀、錨點數、門洞、導航）
tools/compose.py       依 compose/layout.json 組合多場景成一層樓
compose/               layout.json 範例與組合輸出
viewer/index.html      Three.js 瀏覽器（可用 GitHub Pages）
```

## 使用
```bash
pip install bpy            # Blender Python 模組（Python 3.11/3.13 皆可）
python3 scenes/001_open_office/build.py          # 重建單一場景
python3 tools/verify.py scenes/001_open_office   # 驗證
python3 tools/compose.py compose/layout.json     # 組合一層樓
```
Viewer：在 repo 根目錄 `python3 -m http.server`，開 `http://localhost:8000/viewer/`；或啟用 GitHub Pages 後開 `/viewer/`。
支援切換錨點／導航網格／天花板，以及「Demo 人物」（人物依導航網格在錨點間走動，STATUS 位置顯示工作中／開會中／閒置）。

## 組合（compose）
`compose/layout.json`：`tiles[]` 列出 `scene`（資料夾名）、`offset`（旋轉後外框西南角，2 m 倍數）、`rot`（0/90/180/270，繞場景西南角）。
輸出 `<name>.blend/.glb/.json/_navmesh.glb`，json 內含合併後的門與錨點（id 加 `T<序號>_` 前綴）與重疊警告。

## 程式整合提示
- `scene.json` 的座標為 Blender Z-up；glb 為 glTF Y-up（`gx=x, gy=z, gz=−y`）。
- 人物面向：anchor `yaw_deg=0` 面向 +Y（北）。Three.js 中朝向 = `(−sinθ, 0, −cosθ)`。
