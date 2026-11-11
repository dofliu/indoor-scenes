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

選用欄位 `status`（003 起）：SEAT／STAND 錨點可在 `scene.json` 與 glb 自訂屬性中帶 `"status": "STATUS_<序號>"`，明確指定它對應的狀態燈（例如一間小會議室的所有座位共用門楣上的一盞燈）。場景內只要有任一錨點帶 `status`，程式端就只用明確對應，未指定的錨點不顯示狀態；完全沒有 `status` 的舊場景則以「最近的 STATUS」推定。

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
