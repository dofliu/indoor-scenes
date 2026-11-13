# 室內場景模組規格（SPEC）

每個場景都必須遵守，這是模組能任意拼接、並讓人物在其中移動的關鍵。

## 座標與尺寸
- 單位公尺，Z 軸向上，+Y 為北。房間地板西南角為原點 (0,0,0)，地板頂面 z=0。
- 外框尺寸為 **2 m 網格整數倍**（如 8×6、12×10）。樓高（地板到天花板下緣）固定 **3.0 m**。
- 牆厚 0.2 m，牆體在外框線內側。
- yaw_deg 為 Blender 繞 Z 軸旋轉（逆時針為正）：0 面向 +Y（北）、90 面向 −X（西）、−90 面向 +X（東）、180 面向 −Y（南）。

## 門洞
- 寬 1.0 m、高 2.2 m；門洞中心只能在某面牆距**牆起點奇數公尺**（1, 3, 5…）處，使任兩模組並排時可對齊。
- 牆起點：S、N 牆自西端（x=0）起量；E、W 牆自南端（y=0）起量。
- 每個門洞一個 empty：`DOOR_<N/E/S/W>_<序號>`，位於門洞中心地面（牆中心線），自訂屬性 `width_m`、`height_m`、`wall`、`offset_m`。

## 錨點（empty，地面高度，+Y 朝向為人物面向）
| 名稱 | 用途 |
|---|---|
| `SEAT_<用途>_<序號>` | 坐下點（SEAT_desk_03、SEAT_meeting_07） |
| `STAND_<用途>_<序號>` | 站立工作點（STAND_whiteboard_01、STAND_machine_02） |
| `POI_<名稱>_<序號>` | 互動點（POI_coffee_01、POI_printer_01） |
| `STATUS_<序號>` | 狀態燈／標籤顯示位置，約 z=2.2 m |

### 高架錨點（015 起）
- 階梯座位、舞台等高於地面的位置，錨點 `position` 的 z 為**人物腳底高度**（z > 0），其餘錨點維持 z = 0（STATUS 除外）。
- 高架錨點不在 z=0 的導航網格上：程式先沿導航網格走到最近的可走點，再直接移動（或播放上階動作）到錨點；
  離開時回到最近的可走點、高度歸零。水平距離導航網格不得超過 3.0 m（`tools/verify.py` 檢查）。
- `viewer/engine.js` 已支援：抵達高架錨點時人物移到錨點並抬升至該高度，離開時歸零。

## 導航網格
- 物件 `NAVMESH`，collection `NAV`；僅含可走地面（z=0 平面），扣除家具與牆體，並內縮 0.3 m。
- 目前實作為 0.25 m 格網四邊形（頂點共用，方便 A*／navmesh 函式庫使用）；門口通道延伸至房間外緣，與鄰接模組的通道銜接。
- 匯出為獨立 `navmesh.glb`，不含於 `scene.glb`。

## Collections
`STRUCTURE`（地板、牆、天花板）、`FURNITURE`、`PROPS`、`LIGHTS`、`ANCHORS`、`NAV`。

## 材質與效能
- Principled BSDF 程序化顏色，不依賴外部貼圖；單一 `scene.glb` < 8 MB。
- 只用自建通用家具設備，不使用任何品牌名稱、商標或 logo。

## 每個場景的輸出（`scenes/<NNN>_<slug>/`）
`scene.blend`、`scene.glb`（Y-up；含錨點 empties 與 extras）、`navmesh.glb`、`scene.json`、`preview.png`（Cycles 等角 1280×720）、`plan.png`（正交頂視，標門與錨點）、`build.py`（可重跑）。

### scene.json
```json
{ "id","name_zh","name_en","category","size_m":[x,y],"height_m",
  "doors":[{"id","wall","offset_m","width_m","position":[x,y,z]}],
  "anchors":[{"id","type","use","position":[x,y,z],"yaw_deg"}],
  "tags":[],"nav":{...},"created" }
```
category：office / meeting / social / factory / lab / service / connector。

## 座標轉換（glb）
glTF 為 Y-up：`gx = x, gy = z, gz = −y`。`scene.json` 的所有座標為 Blender（Z-up）座標。

## 執行期協議（草案 v0.1）
場景檔是靜態的；人物與狀態由「世界引擎」`viewer/engine.js` 管理，外部程式（AI 代理人框架、MES、排程）透過 JSON 訊息驅動。
可直接在頁面呼叫 `world.apply(msg)`，或用 WebSocket 連線（viewer 網址加 `?ws=ws://host:port`，範例後端 `tools/mock_agent_server.py`）。

### 外部 → viewer
| type | 欄位 | 說明 |
|---|---|---|
| `agent.spawn` | `id, name, role, color?, at?`（錨點或門 id） | 產生人物 |
| `agent.state` | `id, state?, task?, energy?(0–1), vars?{}, anchor?/seat?` | 更新狀態變數；給了 `anchor` 會自動走過去 |
| `agent.do` | `id, actions[], replace?(預設 true), dwell_s?` | 依序執行動作（見下表） |
| `agent.say` | `id, text, sec?` | 頭上對話泡泡 |
| `agent.remove` / `world.reset` | `id` / — | 移除人物／全部清空 |

`state`：`idle` 閒置、`walk` 移動中、`work` 工作中、`meet` 開會中、`present` 報告中、`rest` 休息、`use` 使用設備。
`vars` 為任意鍵值（如 `tokens`、`model`、`progress`），面板會照列。

### 動作（actions）
| 動作 | 範例 | 說明 |
|---|---|---|
| `goto` | `{"goto":"SEAT_desk_03"}` | 沿導航網格走到錨點或門；SEAT 會坐下並佔位，自動決定狀態（meeting→開會中…） |
| `use` | `{"use":"POI_coffee_01","action":"brew","duration_s":6}` | 使用設備（不在旁邊會先走過去）；茶水類設備會恢復 `energy` |
| `say` | `{"say":"收到"}` | 說話泡泡 |
| `set` | `{"set":{"state":"work","task":"審查 PR #12","vars":{"tokens":1200}}}` | 改狀態變數 |
| `wait` | `{"wait":5}` | 停留秒數 |
| `auto` | `{"auto":true}` | 交回自動（Demo）行為 |

### viewer → 外部
| type | 何時 |
|---|---|
| `world.hello` | 連線或換場景時，附場景 id、錨點清單（`id,type,use`）、門 id、現有人物 |
| `user.command` | 使用者在人物面板下自然語言指令：`{id, text, context}`，由後端 AI 決定 `agent.do` |
| `agent.arrived` / `agent.used` / `agent.spawned` / `viewer.select` | 事件通知，供後端推進任務 |

未連線後端時，`user.command` 由引擎內建的關鍵字解析器「模擬 AI」處理（咖啡、開會、白板、回座位、離開…）。
接真正的 LLM：把 `text`、人物狀態與 `world.hello` 的錨點清單交給模型，要求只輸出上表的 actions JSON。

### 觀看模式
點人物＝鏡頭平滑跟隨並開啟人物面板；雙擊或「肩後視角」＝第三人稱跟拍；Esc／「返回全景」＝回到原視角。

### 規劃中（尚未實作）
- `interactables`：在 `scene.json` 描述可操作設備（動作名稱、時間、效果、動畫部件），如冰箱開門、販賣機出貨、電腦螢幕即時顯示任務。
- `CAM_<名稱>` 錨點：每個房間的推薦視角。
