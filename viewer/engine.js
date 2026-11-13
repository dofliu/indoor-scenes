// DofLab 室內場景庫 — 世界引擎（Three.js r160，ES module）
// 負責：導航網格 A*、人物（狀態變數、行為佇列）、指令解析、執行期協議、鏡頭跟隨與人物面板。
// 頁面只要負責載入 scene.glb / navmesh.glb / scene.json，再呼叫 world.setScene(meta, navObj)。
// 協議說明見 SPEC.md「執行期協議」。
import * as THREE from 'three';

export const B2T = p => new THREE.Vector3(p[0], p[2], -p[1]);   // Blender(Z-up) → Three(Y-up)

export const STATES = {
  idle: ['閒置', '#c8c8c8'], walk: ['移動中', '#ffffff'], work: ['工作中', '#7CFC9A'],
  meet: ['開會中', '#ffd166'], present: ['報告中', '#ff9f6b'], rest: ['休息', '#7fd6ff'], use: ['使用設備', '#d0a8ff'],
};
const BREAK_USES = new Set(['coffee', 'water', 'fridge', 'vending', 'sink', 'microwave']);
const USE_ZH = {
  desk: '工位', meeting: '會議座位', whiteboard: '白板', presenter: '簡報位', phone: '電話亭', bar: '吧台', cafe: '咖啡座',
  coffee: '咖啡機', water: '飲水機', fridge: '冰箱', vending: '販賣機', sink: '水槽', microwave: '微波爐',
  printer: '影印機', cabinet: '櫃子', credenza: '邊櫃', projector: '投影機', screen: '螢幕', door: '門口',
};
const QUICK = [ // [use, 按鈕文字（同時也是送出的自然語言指令）]
  ['coffee', '去泡咖啡'], ['water', '去喝水'], ['fridge', '去開冰箱'], ['vending', '去買飲料'],
  ['sink', '去洗杯子'], ['microwave', '去微波便當'], ['printer', '去影印'],
];
const KEYWORDS = [ // 本地「模擬 AI」解析用：關鍵字 → 錨點篩選
  [/咖啡|coffee/i, a => a.type === 'POI' && a.use === 'coffee'],
  [/喝水|飲水|倒水|water/i, a => a.type === 'POI' && (a.use === 'water' || a.use === 'sink')],
  [/冰箱|fridge/i, a => a.use === 'fridge'],
  [/販賣機|飲料|零食|vending/i, a => a.use === 'vending'],
  [/微波|加熱|便當|microwave/i, a => a.use === 'microwave'],
  [/水槽|洗|sink/i, a => a.use === 'sink'],
  [/影印|列印|印|printer/i, a => a.use === 'printer'],
  [/投影|projector/i, a => a.use === 'projector'],
  [/白板|whiteboard/i, a => a.type === 'STAND' && a.use === 'whiteboard'],
  [/報告|簡報|上台|present/i, a => a.type === 'STAND' && /^present/.test(a.use)],
  [/開會|會議|meeting/i, a => a.type === 'SEAT' && a.use === 'meeting'],
  [/電話|phone/i, a => a.type === 'SEAT' && a.use === 'phone'],
  [/吧台|bar/i, a => a.type === 'SEAT' && a.use === 'bar'],
  [/櫃|文具|cabinet/i, a => a.use === 'cabinet' || a.use === 'credenza'],
];
const DEMO_CAST = [
  ['planner', '規劃者', 'Planner'], ['coder-1', '工程師 A', 'Coder'], ['coder-2', '工程師 B', 'Coder'],
  ['reviewer', '審查員', 'Reviewer'], ['tester', '測試員', 'Tester'], ['pm', '專案經理', 'PM'],
  ['designer', '設計師', 'Designer'], ['ops', '維運', 'Ops'],
];
const DEMO_TASKS = {
  Planner: ['拆解需求', '規劃 Sprint', '排定優先序'], Coder: ['實作 API', '修 bug #34', '重構模組', '寫單元測試'],
  Reviewer: ['審查 PR #12', '審查 PR #15'], Tester: ['跑回歸測試', '寫 E2E 測試'], PM: ['更新進度', '對齊需求'],
  Designer: ['畫線框稿', '調整 UI'], Ops: ['監看部署', '調整 CI'],
};
const COLORS = [0xff8a65, 0x4dd0e1, 0xba68c8, 0xaed581, 0xffd54f, 0x90a4ae, 0xf06292, 0x7986cb];
const rnd = a => a[Math.floor(Math.random() * a.length)];
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const anchorZh = a => a ? (USE_ZH[a.use] || a.use || a.id) + (a.type === 'DOOR' ? '' : ' ' + a.id.split('_').pop()) : '';

// ---------------------------------------------------------------- 文字標籤（canvas sprite）
function textSprite(h = 0.25) {
  const cv = document.createElement('canvas'), x = cv.getContext('2d');
  const tex = new THREE.CanvasTexture(cv); tex.colorSpace = THREE.SRGBColorSpace;
  const spr = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, depthTest: false, transparent: true }));
  spr.renderOrder = 10;
  const set = (text, color = '#fff', bg = '#0b1210d0', dot = null) => {
    const fs = 30, pad = 18, font = `bold ${fs}px "Noto Sans TC","WenQuanYi Zen Hei","Microsoft JhengHei",sans-serif`;
    x.font = font;
    const tw = Math.ceil(x.measureText(text).width) + (dot ? 30 : 0);
    cv.width = Math.max(96, tw + pad * 2); cv.height = 60;
    x.font = font; x.clearRect(0, 0, cv.width, 60);
    x.fillStyle = bg; x.beginPath(); x.roundRect(3, 4, cv.width - 6, 52, 16); x.fill();
    let tx = pad;
    if (dot) { x.fillStyle = dot; x.beginPath(); x.arc(pad + 10, 30, 10, 0, 7); x.fill(); tx += 30; }
    x.fillStyle = color; x.textBaseline = 'middle'; x.fillText(text, tx, 32);
    tex.needsUpdate = true;
    spr.scale.set(h * cv.width / 60, h, 1);
  };
  return { sprite: spr, set };
}

// ---------------------------------------------------------------- 面板樣式（只注入一次）
const CSS = `
.iw-panel{position:absolute;top:10px;right:10px;width:286px;max-height:calc(100% - 20px);overflow:auto;z-index:5;
  background:rgba(12,18,20,.9);color:#e8eef0;border:1px solid rgba(255,255,255,.14);border-radius:10px;
  font:13px/1.5 "Noto Sans TC","Microsoft JhengHei",system-ui,sans-serif;backdrop-filter:blur(6px)}
.iw-panel[data-empty]{display:none}
.iw-narrow .iw-panel{top:auto;bottom:8px;left:8px;right:8px;width:auto;max-height:44%}
.iw-hd{display:flex;align-items:center;justify-content:space-between;padding:8px 10px;border-bottom:1px solid rgba(255,255,255,.1)}
.iw-hd b{font-size:13px}
.iw-ws{font:11px ui-monospace,monospace;color:#9fb0b4}
.iw-ws[data-on]{color:#3cc4ae}
.iw-x{all:unset;cursor:pointer;padding:0 6px;font-size:16px;color:#9fb0b4}
.iw-x:focus-visible,.iw-chip:focus-visible,.iw-b:focus-visible{outline:2px solid #3cc4ae}
.iw-roster{display:flex;flex-wrap:wrap;gap:5px;padding:8px 10px}
.iw-chip{all:unset;cursor:pointer;display:flex;align-items:center;gap:6px;padding:3px 9px;border-radius:999px;background:rgba(255,255,255,.07);font-size:12px}
.iw-chip:hover{background:rgba(255,255,255,.14)}
.iw-chip[aria-pressed=true]{background:#3cc4ae;color:#06201b}
.iw-chip i{width:9px;height:9px;border-radius:50%;display:inline-block}
.iw-chip s{text-decoration:none;opacity:.75}
.iw-det{padding:4px 12px 12px;display:flex;flex-direction:column;gap:8px;border-top:1px solid rgba(255,255,255,.1)}
.iw-det[hidden]{display:none}
.iw-name{display:flex;align-items:baseline;gap:8px;margin-top:6px}
.iw-name b{font-size:16px}.iw-name span{color:#9fb0b4;font-size:12px}
.iw-kv{display:grid;grid-template-columns:44px 1fr;gap:2px 8px;font-size:12.5px}
.iw-kv dt{color:#9fb0b4}.iw-kv dd{margin:0;min-width:0;overflow-wrap:anywhere}
.iw-bar{height:6px;background:rgba(255,255,255,.12);border-radius:3px;overflow:hidden;margin-top:6px}
.iw-bar i{display:block;height:100%;background:#3cc4ae}
.iw-row{display:flex;flex-wrap:wrap;gap:5px}
.iw-b{all:unset;cursor:pointer;padding:3px 9px;border-radius:6px;border:1px solid rgba(255,255,255,.18);font-size:12px}
.iw-b:hover{border-color:#3cc4ae}.iw-b[aria-pressed=true]{background:#3cc4ae;color:#06201b;border-color:#3cc4ae}
.iw-sec{font-size:11px;color:#9fb0b4;letter-spacing:.06em}
.iw-form{display:flex;gap:5px}
.iw-form input{flex:1;min-width:0;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);color:inherit;border-radius:6px;padding:5px 8px;font:inherit}
.iw-form button{all:unset;cursor:pointer;background:#3cc4ae;color:#06201b;border-radius:6px;padding:4px 10px;font-weight:700}
.iw-log{margin:0;padding:0;list-style:none;font-size:12px;color:#c4d0d3;max-height:132px;overflow:auto}
.iw-log li{padding:2px 0;border-bottom:1px dashed rgba(255,255,255,.08)}
.iw-log li[data-k=you]{color:#ffd166}.iw-log li[data-k=ai]{color:#7fd6ff}
`;

export function createWorld({ scene, camera, controls, dom, container }) {
  if (!document.getElementById('iw-css')) {
    const st = document.createElement('style'); st.id = 'iw-css'; st.textContent = CSS; document.head.appendChild(st);
  }
  let meta = null, nav = null, anchors = [], doors = [];
  const seatStatus = new Map(), statusLabels = new Map(), statusOcc = new Map(), reserved = new Map();
  let agents = []; const byId = new Map();
  let sel = null, demoOn = false, ws = null, panelT = 0;
  const listeners = new Set();
  const cam = { mode: 'free', anim: null, last: new THREE.Vector3(), overview: null };
  const emit = ev => { listeners.forEach(f => f(ev)); if (ws && ws.readyState === 1) ws.send(JSON.stringify(ev)); };

  // ============================================================ 導航
  function buildNav(obj) {
    const cell = (meta.nav && meta.nav.cell_m) || 0.25, walk = new Set(), key = (i, j) => i + ',' + j;
    obj.updateMatrixWorld(true);
    const v = new THREE.Vector3();
    obj.traverse(o => {
      if (!o.isMesh) return;
      const pos = o.geometry.attributes.position, idx = o.geometry.index;
      const P = i => v.fromBufferAttribute(pos, i).applyMatrix4(o.matrixWorld).clone();
      const tri = (a, b, c) => { const A = P(a), B = P(b), C = P(c); walk.add(key(Math.floor((A.x + B.x + C.x) / 3 / cell), Math.floor((A.z + B.z + C.z) / 3 / cell))); };
      if (idx) for (let i = 0; i < idx.count; i += 3) tri(idx.getX(i), idx.getX(i + 1), idx.getX(i + 2));
      else for (let i = 0; i < pos.count; i += 3) tri(i, i + 1, i + 2);
    });
    nav = { cell, walk, key, free: (x, z) => walk.has(key(Math.floor(x / cell), Math.floor(z / cell))) };
  }
  function snap(x, z) {
    if (nav.free(x, z)) return [x, z];
    let b = null, bd = 1e9; const c = nav.cell;
    for (const k of nav.walk) { const [i, j] = k.split(',').map(Number), cx = (i + .5) * c, cz = (j + .5) * c, d = (cx - x) ** 2 + (cz - z) ** 2; if (d < bd) { bd = d; b = [cx, cz]; } }
    return b;
  }
  function astar(sx, sz, gx, gz) {
    const c = nav.cell, ci = v => Math.floor(v / c), [s0, s1] = snap(sx, sz), [g0, g1] = snap(gx, gz);
    const si = ci(s0), sj = ci(s1), gi = ci(g0), gj = ci(g1), k = (i, j) => i + ',' + j;
    const open = new Map(), came = new Map(), G = new Map(), h = (i, j) => Math.hypot(i - gi, j - gj);
    G.set(k(si, sj), 0); open.set(k(si, sj), h(si, sj));
    const N = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]];
    while (open.size) {
      let bk = null, bf = 1e9; for (const [kk, f] of open) if (f < bf) { bf = f; bk = kk; }
      open.delete(bk); const [i, j] = bk.split(',').map(Number); if (i === gi && j === gj) break;
      for (const [di, dj] of N) {
        const ni = i + di, nj = j + dj, nk = k(ni, nj); if (!nav.walk.has(nk)) continue;
        if (di && dj && (!nav.walk.has(k(i + di, j)) || !nav.walk.has(k(i, j + dj)))) continue;
        const g = G.get(bk) + Math.hypot(di, dj);
        if (g < (G.get(nk) ?? 1e9)) { G.set(nk, g); came.set(nk, bk); open.set(nk, g + h(ni, nj)); }
      }
    }
    const gk = k(gi, gj); if (!came.has(gk) && gk !== k(si, sj)) return [[sx, sz], [gx, gz]];
    const cells = []; let cu = gk; while (cu) { cells.push(cu); cu = came.get(cu); } cells.reverse();
    const pts = cells.map(q => { const [i, j] = q.split(',').map(Number); return [(i + .5) * c, (j + .5) * c]; });
    pts[0] = [s0, s1]; pts[pts.length - 1] = [g0, g1];
    const los = (a, b) => { const n = Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / (c * .4)); for (let t = 1; t < n; t++) if (!nav.free(a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n)) return false; return true; };
    const out = [pts[0]]; let a = 0;
    while (a < pts.length - 1) { let b = pts.length - 1; while (b > a + 1 && !los(pts[a], pts[b])) b--; out.push(pts[b]); a = b; }
    // 最後一段直接走到錨點本身（錨點可能在可走區邊緣外，例如椅子上）
    out.push([gx, gz]);
    return out;
  }

  // ============================================================ 錨點查詢
  const findAnchor = id => anchors.find(a => a.id === id) || doors.find(d => d.id === id);
  const isFree = (a, ag) => !reserved.has(a.id) || reserved.get(a.id) === ag.id;
  const dist = (ag, a) => { const p = B2T(a.position); return Math.hypot(p.x - ag.root.position.x, p.z - ag.root.position.z); };
  function nearest(ag, list, freeOnly = true) {
    let b = null, bd = 1e9;
    for (const a of list) { if (freeOnly && a.type === 'SEAT' && !isFree(a, ag)) continue; const d = dist(ag, a); if (d < bd) { bd = d; b = a; } }
    return b;
  }

  // ============================================================ STATUS 標籤
  function setStatusLabel(stId) {
    const L = statusLabels.get(stId); if (!L) return;
    const occ = statusOcc.get(stId);
    const ag = occ && occ.size ? byId.get([...occ].pop()) : null;
    if (!ag) { L.set('閒置', '#c8c8c8'); return; }
    const [t, c] = STATES[ag.state] || STATES.idle;
    L.set(occ.size > 1 ? `${t}（${occ.size}人）` : (ag.task && ag.state === 'work' ? `${t}・${ag.task}` : t), c);
  }

  // ============================================================ 人物
  function spawn({ id, name, role = '', color, at, auto = false, task = '', energy = 1, vars = {}, home } = {}) {
    if (!nav) return null;
    if (byId.has(id)) return byId.get(id);
    const col = new THREE.Color(color ?? COLORS[agents.length % COLORS.length]);
    const root = new THREE.Group();
    const body = new THREE.Mesh(new THREE.CapsuleGeometry(.22, 1.0, 4, 12), new THREE.MeshStandardMaterial({ color: col, roughness: .55 }));
    body.position.y = .75;
    const visor = new THREE.Mesh(new THREE.BoxGeometry(.26, .09, .1), new THREE.MeshStandardMaterial({ color: 0x1b2328, roughness: .3 }));
    visor.position.set(0, .45, -.18); body.add(visor);
    const ring = new THREE.Mesh(new THREE.RingGeometry(.32, .42, 36), new THREE.MeshBasicMaterial({ color: 0x3cc4ae, transparent: true, opacity: .95, side: THREE.DoubleSide, depthWrite: false }));
    ring.rotation.x = -Math.PI / 2; ring.position.y = .03; ring.visible = false;
    const tag = textSprite(.2); tag.sprite.position.y = 1.78;
    const bubble = textSprite(.24); bubble.sprite.position.y = 2.12; bubble.sprite.visible = false;
    root.add(body, ring, tag.sprite, bubble.sprite);
    scene.add(root);
    const ag = {
      id, name: name || id, role, color: '#' + col.getHexString(), root, body, ring, tag, bubble, bubbleT: 0,
      state: 'idle', task, energy, vars: { ...vars }, queue: [], path: [], wait: 0, busy: null, dest: null, at: null,
      seat: null, status: null, auto, mode: auto ? 'auto' : 'idle', dwell: 0, log: [], home: home || null,
    };
    body.userData.agent = ag; visor.userData.agent = ag;
    const a0 = at && findAnchor(at);
    if (a0) { const p = B2T(a0.position); root.position.set(p.x, 0, p.z); }
    else { const [ci, cj] = rnd([...nav.walk]).split(',').map(Number); root.position.set((ci + .5) * nav.cell, 0, (cj + .5) * nav.cell); }
    agents.push(ag); byId.set(id, ag);
    setState(ag, 'idle'); log(ag, '進入場景');
    emit({ type: 'agent.spawned', id, name: ag.name });
    renderRoster();
    return ag;
  }
  function remove(id) {
    const ag = byId.get(id); if (!ag) return;
    releaseSeat(ag); scene.remove(ag.root); agents = agents.filter(a => a !== ag); byId.delete(id);
    if (sel === ag) deselect(false);
    renderRoster();
  }
  function log(ag, text, kind = '') {
    ag.log.unshift({ t: new Date().toTimeString().slice(0, 8), text, kind }); ag.log.length = Math.min(ag.log.length, 40);
    if (sel === ag) renderLog();
  }
  function setState(ag, s) {
    if (STATES[s]) ag.state = s;
    const [t, c] = STATES[ag.state];
    ag.tag.set(ag.name, '#fff', sel === ag ? '#0d6f62e8' : '#0b1210c8', c);
    if (ag.status) setStatusLabel(ag.status);
  }
  function say(ag, text, sec = 4) { ag.bubble.set(text, '#10181a', '#ffffffee'); ag.bubble.sprite.visible = true; ag.bubbleT = sec; }
  function releaseSeat(ag) {
    if (ag.seat) { if (reserved.get(ag.seat) === ag.id) reserved.delete(ag.seat); ag.seat = null; }
    if (ag.status) { const o = statusOcc.get(ag.status); o && o.delete(ag.id); const s = ag.status; ag.status = null; setStatusLabel(s); }
    ag.body.position.y = .75; ag.root.position.y = 0;   // 離開高架錨點（階梯座位／舞台）時高度歸零
  }
  function arrive(ag) {
    const a = ag.dest; ag.busy = null; ag.dest = null; if (!a) return;
    ag.at = a.id; ag.root.rotation.y = a.yaw_deg * Math.PI / 180;
    if (a.position[2] > .05) { const p = B2T(a.position); ag.root.position.set(p.x, a.position[2], p.z); }   // 高架錨點：直接移到錨點並抬升
    if (a.type === 'SEAT') {
      ag.seat = a.id; reserved.set(a.id, ag.id); ag.body.position.y = .5;
      const st = seatStatus.get(a.id);
      if (st) { if (!statusOcc.has(st)) statusOcc.set(st, new Set()); statusOcc.get(st).add(ag.id); ag.status = st; }
      setState(ag, a.use === 'meeting' ? 'meet' : (a.use === 'bar' || a.use === 'cafe') ? 'rest' : 'work');
    } else if (a.type === 'STAND') setState(ag, /^(present|whiteboard)/.test(a.use) ? 'present' : 'work');
    else setState(ag, 'idle');
    log(ag, '抵達 ' + anchorZh(a));
    emit({ type: 'agent.arrived', id: ag.id, anchor: a.id });
  }
  function runAction(ag, act) {
    if (act.goto) {
      const a = findAnchor(act.goto);
      if (!a) { log(ag, '找不到錨點 ' + act.goto); return; }
      releaseSeat(ag);
      if (a.type === 'SEAT') reserved.set(a.id, ag.id);
      const g = B2T(a.position);
      ag.path = astar(ag.root.position.x, ag.root.position.z, g.x, g.z).slice(1);
      ag.dest = a; ag.busy = 'walk'; ag.at = null; setState(ag, 'walk');
    } else if (act.use) {
      const a = findAnchor(act.use);
      if (!a) { log(ag, '找不到設備 ' + act.use); return; }
      if (dist(ag, a) > .7) { ag.queue.unshift({ goto: a.id }, act); return; }
      const brk = BREAK_USES.has(a.use);
      ag.root.rotation.y = a.yaw_deg * Math.PI / 180;
      setState(ag, brk ? 'rest' : 'use');
      ag.busy = 'wait'; ag.wait = act.duration_s ?? (brk ? 6 : 4);
      ag.onDone = () => { if (brk) ag.energy = clamp(ag.energy + .25, 0, 1); emit({ type: 'agent.used', id: ag.id, anchor: a.id, action: act.action || 'use' }); };
      log(ag, '使用 ' + anchorZh(a) + (act.action ? `（${act.action}）` : ''));
    } else if (act.say) {
      say(ag, act.say); log(ag, '說：' + act.say, 'ai'); ag.busy = 'wait'; ag.wait = .4;
    } else if (act.wait != null) {
      ag.busy = 'wait'; ag.wait = +act.wait || 0;
    } else if (act.set) {
      const s = act.set;
      if (s.task != null) ag.task = s.task;
      if (s.energy != null) ag.energy = clamp(+s.energy, 0, 1);
      if (s.vars) Object.assign(ag.vars, s.vars);
      if (s.state) setState(ag, s.state); else setState(ag, ag.state);
      if (s.task) log(ag, '任務：' + s.task);
    } else if (act.auto) {
      ag.auto = true; ag.mode = 'auto'; ag.queue = []; log(ag, '交回自動行為');
    }
  }
  function planAuto(ag) {
    const seats = anchors.filter(a => a.type === 'SEAT'), stands = anchors.filter(a => a.type === 'STAND');
    const pois = anchors.filter(a => a.type === 'POI'), breaks = pois.filter(a => BREAK_USES.has(a.use));
    const r = Math.random(); let a = null, task = '';
    if (ag.energy < .35 && breaks.length) a = rnd(breaks);
    else if (r < .5 && ag.home && isFree(findAnchor(ag.home) || {}, ag)) { a = findAnchor(ag.home); task = rnd(DEMO_TASKS[ag.role] || ['處理工作']); }
    else if (r < .65) { const m = seats.filter(s => s.use === 'meeting' && isFree(s, ag)); a = m.length ? rnd(m) : null; task = '會議'; }
    else if (r < .8 && stands.length) a = rnd(stands);
    else if (pois.length) a = rnd(pois);
    if (!a) { const f = seats.filter(s => isFree(s, ag)); a = f.length ? rnd(f) : (pois[0] || stands[0]); }
    if (!a) { ag.busy = 'wait'; ag.wait = 3; return; }
    ag.queue.push({ goto: a.id });
    if (a.type === 'POI') ag.queue.push({ use: a.id }, { set: { task: '' } });
    else if (a.type === 'SEAT') ag.queue.push({ set: { task } }, { wait: 8 + Math.random() * 12 });
    else ag.queue.push({ wait: 4 + Math.random() * 6 });
  }
  function stepAgent(ag, dt) {
    const rate = { work: -.010, meet: -.006, present: -.012, walk: -.003, rest: .05, use: 0, idle: .004 }[ag.state] || 0;
    ag.energy = clamp(ag.energy + rate * dt, 0, 1);
    if (ag.busy === 'walk') {
      if (!ag.path.length) arrive(ag);
      else {
        const p = ag.root.position, t = ag.path[0], dx = t[0] - p.x, dz = t[1] - p.z, d = Math.hypot(dx, dz), sp = 1.3 * dt;
        if (d <= sp) { p.x = t[0]; p.z = t[1]; ag.path.shift(); }
        else { p.x += dx / d * sp; p.z += dz / d * sp; ag.root.rotation.y = Math.atan2(-dx, -dz); }
      }
    } else if (ag.busy === 'wait') {
      ag.wait -= dt;
      if (ag.wait <= 0) { ag.busy = null; if (ag.onDone) { const f = ag.onDone; ag.onDone = null; f(); } }
    }
    if (!ag.busy) {
      if (ag.queue.length) runAction(ag, ag.queue.shift());
      else if (ag.mode === 'manual') { ag.dwell -= dt; if (ag.dwell <= 0 && ag.auto) { ag.mode = 'auto'; log(ag, '指令完成，回到自動行為'); } }
      else if (ag.mode === 'auto') planAuto(ag);
    }
    if (ag.bubbleT > 0) { ag.bubbleT -= dt; if (ag.bubbleT <= 0) ag.bubble.sprite.visible = false; }
  }

  // ============================================================ 指令（本地模擬 AI）
  function parseCommand(text, ag) {
    const actions = [], notes = [];
    const clauses = text.split(/然後|接著|之後|再來|[，,。；;、\n]|->|→/).map(s => s.trim()).filter(Boolean);
    const all = anchors.concat(doors);
    for (const c of clauses) {
      let m;
      if ((m = c.match(/^(?:說|講|告訴大家|say)[:：\s]*(.+)$/i))) { actions.push({ say: m[1] }); notes.push('說話'); continue; }
      if (/自動|自由活動|auto/i.test(c)) { actions.push({ auto: true }); notes.push('交回自動'); continue; }
      if ((m = c.match(/(?:等|待命|wait)\s*(\d+)?/i)) && !/等一下去/.test(c)) { actions.push({ wait: +(m[1] || 10) }); notes.push('等待'); continue; }
      let task = null;
      if ((m = c.match(/(?:任務|負責|處理|做)[:：\s]+(.+)$/))) task = m[1];
      let target = null;
      if (/回座位|回位子|回去工作|上班|寫程式|coding|^工作/i.test(c)) {
        target = (ag.home && findAnchor(ag.home)) || nearest(ag, anchors.filter(a => a.type === 'SEAT' && a.use === 'desk')) || nearest(ag, anchors.filter(a => a.type === 'SEAT'));
      } else if (/離開|出去|下班|門口|leave/i.test(c)) target = nearest(ag, doors, false);
      else {
        let missing = null;
        for (const [re, f] of KEYWORDS) if (re.test(c)) { target = nearest(ag, all.filter(f)); if (target) break; missing = missing || c.match(re)[0]; }
        if (!target && missing) {
          notes.push(`這個房間沒有「${missing}」`);
          if (/咖啡|飲料|喝/.test(c)) target = nearest(ag, anchors.filter(a => a.type === 'POI' && BREAK_USES.has(a.use)));
          if (!target) { actions.push({ say: `這個房間沒有${missing}耶` }); continue; }
        }
        if (!target && /休息|累|break/i.test(c)) target = nearest(ag, anchors.filter(a => a.type === 'POI' && BREAK_USES.has(a.use))) || nearest(ag, anchors.filter(a => a.type === 'SEAT' && /bar|cafe/.test(a.use)));
      }
      if (target) {
        actions.push({ goto: target.id });
        if (target.type === 'POI') actions.push({ use: target.id });
        notes.push('→ ' + target.id);
      }
      if (task) { actions.push({ set: { task, state: target && target.type === 'SEAT' ? undefined : 'work' } }); notes.push('任務=' + task); }
      if (!target && !task) notes.push('看不懂「' + c + '」');
    }
    return { actions, notes };
  }
  function command(id, text) {
    const ag = byId.get(id); if (!ag || !text.trim()) return;
    log(ag, '你：' + text, 'you');
    if (ws && ws.readyState === 1) {
      ws.send(JSON.stringify({ type: 'user.command', id, text, context: agentInfo(ag) }));
      log(ag, '已送給 AI 後端，等待回覆…');
      return;
    }
    const { actions, notes } = parseCommand(text, ag);
    if (!actions.length) { say(ag, '抱歉，我聽不懂 🤔'); log(ag, '（模擬 AI）' + notes.join('；'), 'ai'); return; }
    log(ag, '（模擬 AI）' + notes.join('；'), 'ai');
    say(ag, rnd(['好，馬上去！', '收到 👍', '沒問題', 'OK，交給我']), 2.5);
    apply({ type: 'agent.do', id, actions, replace: true });
    emit({ type: 'user.command', id, text, parsed: actions });
  }

  // ============================================================ 執行期協議
  function apply(ev) {
    if (!ev || !ev.type) return;
    if (ev.type === 'agent.spawn') { spawn(ev); return; }
    if (ev.type === 'agent.remove') { remove(ev.id); return; }
    if (ev.type === 'world.reset') { [...agents].forEach(a => remove(a.id)); return; }
    let ag = byId.get(ev.id);
    if (!ag && ev.id) ag = spawn({ id: ev.id, name: ev.name || ev.id, role: ev.role });
    if (!ag) return;
    if (ev.type === 'agent.state') {
      if (ev.name) ag.name = ev.name;
      if (ev.task != null) ag.task = ev.task;
      if (ev.energy != null) ag.energy = clamp(+ev.energy, 0, 1);
      if (ev.vars) Object.assign(ag.vars, ev.vars);
      const target = ev.anchor || ev.seat;
      if (target && ag.at !== target) { ag.queue = [{ goto: target }]; if (ev.state) ag.queue.push({ set: { state: ev.state } }); ag.mode = 'manual'; ag.dwell = 1e9; }
      else if (ev.state) setState(ag, ev.state); else setState(ag, ag.state);
      if (ev.task) log(ag, '任務：' + ev.task);
    } else if (ev.type === 'agent.do') {
      if (ev.replace !== false) { ag.queue = []; ag.path = []; ag.busy = null; ag.dest = null; ag.wait = 0; ag.onDone = null; }
      ag.queue.push(...(ev.actions || []));
      ag.mode = 'manual'; ag.dwell = ev.dwell_s ?? 15;
    } else if (ev.type === 'agent.say') say(ag, ev.text || '', ev.sec || 4);
    if (sel === ag) renderDetail();
  }
  function connect(url) {
    try { ws = new WebSocket(url); } catch (e) { console.warn(e); return; }
    ws.onopen = () => { hello(); renderHeader(); };
    ws.onclose = () => { renderHeader(); };
    ws.onmessage = e => { try { const m = JSON.parse(e.data); (Array.isArray(m) ? m : [m]).forEach(apply); } catch (er) { console.warn('bad msg', er); } };
  }
  function hello() {
    if (!ws || ws.readyState !== 1 || !meta) return;
    ws.send(JSON.stringify({
      type: 'world.hello', scene: meta.id, name_zh: meta.name_zh,
      anchors: anchors.map(a => ({ id: a.id, type: a.type, use: a.use })), doors: doors.map(d => d.id),
      agents: agents.map(agentInfo),
    }));
  }
  const agentInfo = ag => ({ id: ag.id, name: ag.name, role: ag.role, state: ag.state, task: ag.task, energy: +ag.energy.toFixed(2), at: ag.at, vars: ag.vars });

  // ============================================================ 鏡頭
  const focusPoint = ag => ag.root.position.clone().add(new THREE.Vector3(0, ag.body.position.y + .2, 0));
  function select(id, mode = 'follow') {
    const ag = byId.get(id); if (!ag) return;
    if (cam.mode === 'free' || !cam.overview) cam.overview = { pos: camera.position.clone(), tgt: controls.target.clone() };
    if (sel && sel !== ag) { sel.ring.visible = false; sel.tag.sprite.visible = true; const s = sel; sel = null; setState(s, s.state); }
    sel = ag; ag.ring.visible = true; setState(ag, ag.state);
    setCamMode(mode);
    renderRoster(); renderDetail();
    emit({ type: 'viewer.select', id });
  }
  function setCamMode(mode) {
    if (!sel) return;
    cam.mode = mode; controls.enabled = mode !== 'shoulder';
    agents.forEach(a => a.tag.sprite.visible = !(mode === 'shoulder' && a === sel));
    const p = focusPoint(sel);
    let dir = camera.position.clone().sub(controls.target); if (dir.length() < .01) dir.set(0, 1, 1);
    dir.normalize(); if (dir.y < .35) { dir.y = .35; dir.normalize(); }
    cam.anim = { t: 0, dur: .8, pos0: camera.position.clone(), tgt0: controls.target.clone(), off: dir.multiplyScalar(4.8) };
    cam.last.copy(p);
    renderCamButtons();
  }
  function deselect(back = true) {
    if (sel) { sel.ring.visible = false; sel.tag.sprite.visible = true; const s = sel; sel = null; setState(s, s.state); }
    controls.enabled = true;
    if (back && cam.overview) cam.anim = { t: 0, dur: .8, pos0: camera.position.clone(), tgt0: controls.target.clone(), back: cam.overview };
    cam.mode = back ? 'back' : 'free';
    renderRoster(); renderDetail();
  }
  const ease = t => t < .5 ? 2 * t * t : 1 - (-2 * t + 2) ** 2 / 2;
  // 選取人物時把投影中心移到面板以外的可見區，讓人物不被面板擋住
  const vo = { x: 0, y: 0 };
  function stepViewOffset(dt) {
    const w = dom.clientWidth, h = dom.clientHeight; if (!w || !h) return;
    const narrow = container.classList.contains('iw-narrow');
    const open = sel && !panel.hasAttribute('data-empty') && !q('.iw-body').hidden;
    const tx = open && !narrow ? (panel.offsetWidth + 20) / 2 : 0;
    const ty = open && narrow ? (panel.offsetHeight + 16) / 2 : 0;
    const k = 1 - Math.exp(-dt * 6);
    vo.x += (tx - vo.x) * k; vo.y += (ty - vo.y) * k;
    if (Math.abs(vo.x) < .5 && Math.abs(vo.y) < .5 && !tx && !ty) { if (camera.view && camera.view.enabled) camera.clearViewOffset(); return; }
    camera.setViewOffset(w, h, vo.x, vo.y, w, h);
  }
  function stepCam(dt) {
    stepViewOffset(dt);
    if (cam.mode === 'back' && cam.anim) {
      const A = cam.anim; A.t += dt / A.dur; const e = ease(Math.min(A.t, 1));
      camera.position.lerpVectors(A.pos0, A.back.pos, e); controls.target.lerpVectors(A.tgt0, A.back.tgt, e);
      if (A.t >= 1) { cam.anim = null; cam.mode = 'free'; cam.overview = null; }
      return;
    }
    if (!sel) return;
    const p = focusPoint(sel);
    if (cam.mode === 'shoulder') {
      const r = sel.root.rotation.y, fwd = new THREE.Vector3(-Math.sin(r), 0, -Math.cos(r)), right = new THREE.Vector3(Math.cos(r), 0, -Math.sin(r));
      const base = sel.root.position;
      const wantPos = base.clone().add(new THREE.Vector3(0, 2.25, 0)).addScaledVector(fwd, -2.4).addScaledVector(right, .6);
      const wantTgt = base.clone().add(new THREE.Vector3(0, .8, 0)).addScaledVector(fwd, 3.2);
      const k = cam.anim ? Math.min(1, (cam.anim.t += dt / cam.anim.dur)) : 1;
      const s = 1 - Math.exp(-dt * (cam.anim ? 3 + 6 * k : 5));
      camera.position.lerp(wantPos, s); controls.target.lerp(wantTgt, s);
      if (cam.anim && cam.anim.t >= 1) cam.anim = null;
    } else if (cam.mode === 'follow') {
      if (cam.anim) {
        const A = cam.anim; A.t += dt / A.dur; const e = ease(Math.min(A.t, 1));
        controls.target.lerpVectors(A.tgt0, p, e);
        camera.position.lerpVectors(A.pos0, p.clone().add(A.off), e);
        if (A.t >= 1) cam.anim = null;
      } else {
        const d = p.clone().sub(cam.last); controls.target.add(d); camera.position.add(d);
      }
    }
    cam.last.copy(p);
  }

  // ============================================================ 點選
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2(); let down = null;
  function pick(e) {
    const r = dom.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObjects(agents.map(a => a.body), true)[0];
    return hit ? hit.object.userData.agent : null;
  }
  dom.addEventListener('pointerdown', e => { down = [e.clientX, e.clientY]; });
  dom.addEventListener('pointerup', e => {
    if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 5) return;
    const ag = pick(e); if (ag) select(ag.id, cam.mode === 'shoulder' && sel === ag ? 'shoulder' : 'follow');
  });
  dom.addEventListener('dblclick', e => { const ag = pick(e); if (ag) select(ag.id, 'shoulder'); });
  dom.addEventListener('pointermove', e => { if (e.buttons) return; dom.style.cursor = pick(e) ? 'pointer' : ''; });
  addEventListener('keydown', e => { if (e.key === 'Escape' && sel && document.activeElement?.tagName !== 'INPUT') deselect(); });

  // ============================================================ 面板
  const panel = document.createElement('div'); panel.className = 'iw-panel'; panel.dataset.empty = '';
  panel.innerHTML = `
    <div class="iw-hd"><b>人物 <span class="iw-n"></span></b><span class="iw-ws" title="AI 後端連線狀態"></span><button class="iw-x iw-fold" type="button" aria-label="收合">▾</button></div>
    <div class="iw-body">
      <div class="iw-roster" role="group" aria-label="人物清單"></div>
      <div class="iw-det" hidden>
        <div class="iw-name"><i class="iw-dot"></i><b></b><span class="iw-role"></span><span style="flex:1"></span><button class="iw-x iw-close" type="button" aria-label="取消選取">×</button></div>
        <dl class="iw-kv">
          <dt>狀態</dt><dd class="iw-state"></dd><dt>任務</dt><dd class="iw-task"></dd>
          <dt>位置</dt><dd class="iw-at"></dd><dt>精力</dt><dd><span class="iw-en"></span><div class="iw-bar"><i></i></div></dd>
          <dt>變數</dt><dd class="iw-vars"></dd>
        </dl>
        <div class="iw-sec">鏡頭</div>
        <div class="iw-row iw-cam">
          <button class="iw-b" type="button" data-cam="follow">跟隨</button>
          <button class="iw-b" type="button" data-cam="shoulder">肩後視角</button>
          <button class="iw-b" type="button" data-cam="back">返回全景</button>
        </div>
        <div class="iw-sec">下指令</div>
        <div class="iw-row iw-quick"></div>
        <form class="iw-form"><input type="text" placeholder="例：去泡咖啡，然後回座位" aria-label="對人物下指令"><button type="submit">送出</button></form>
        <div class="iw-sec iw-mode"></div>
        <ul class="iw-log" aria-label="行為紀錄"></ul>
      </div>
    </div>`;
  container.appendChild(panel);
  const q = s => panel.querySelector(s);
  q('.iw-fold').onclick = () => { const b = q('.iw-body'); b.hidden = !b.hidden; q('.iw-fold').textContent = b.hidden ? '▸' : '▾'; };
  q('.iw-close').onclick = () => deselect();
  q('.iw-cam').onclick = e => { const m = e.target.dataset.cam; if (!m) return; m === 'back' ? deselect() : setCamMode(m); };
  q('.iw-form').onsubmit = e => { e.preventDefault(); const i = q('.iw-form input'); if (sel) command(sel.id, i.value); i.value = ''; };
  q('.iw-quick').onclick = e => { const t = e.target.dataset.cmd; if (t && sel) command(sel.id, t); };
  new ResizeObserver(() => container.classList.toggle('iw-narrow', container.clientWidth < 700)).observe(container);

  function renderHeader() {
    q('.iw-n').textContent = agents.length ? `(${agents.length})` : '';
    const on = ws && ws.readyState === 1;
    q('.iw-ws').textContent = ws ? (on ? '● AI 後端已連線' : '○ 後端未連線') : '本地模擬';
    if (on) q('.iw-ws').dataset.on = ''; else delete q('.iw-ws').dataset.on;
    if (agents.length) delete panel.dataset.empty; else panel.dataset.empty = '';
  }
  function renderRoster() {
    renderHeader();
    const box = q('.iw-roster'); box.innerHTML = '';
    for (const ag of agents) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'iw-chip';
      b.setAttribute('aria-pressed', sel === ag);
      b.innerHTML = `<i style="background:${ag.color}"></i>${ag.name} <s>${STATES[ag.state][0]}</s>`;
      b.onclick = () => sel === ag ? deselect() : select(ag.id);
      box.appendChild(b);
    }
  }
  function renderCamButtons() { panel.querySelectorAll('[data-cam]').forEach(b => b.setAttribute('aria-pressed', b.dataset.cam === cam.mode)); }
  function renderLog() {
    if (!sel) return;
    q('.iw-log').innerHTML = sel.log.slice(0, 12).map(l => `<li data-k="${l.kind}">${l.t} ${l.text.replace(/</g, '&lt;')}</li>`).join('');
  }
  function renderDetail() {
    const d = q('.iw-det');
    if (!sel) { d.hidden = true; return; }
    d.hidden = false;
    q('.iw-dot').style.cssText = `width:10px;height:10px;border-radius:50%;display:inline-block;background:${sel.color}`;
    q('.iw-name b').textContent = sel.name; q('.iw-role').textContent = sel.role;
    // 快捷指令：依目前場景有的錨點產生
    const uses = new Set(anchors.map(a => a.use)), btn = [];
    if (anchors.some(a => a.type === 'SEAT' && a.use !== 'meeting') || sel.home) btn.push('回座位工作');
    if (uses.has('meeting')) btn.push('去開會');
    if (uses.has('whiteboard')) btn.push('去白板');
    if ([...uses].some(u => /^present/.test(u))) btn.push('上台簡報');
    for (const [u, t] of QUICK) if (uses.has(u)) btn.push(t);
    if (doors.length) btn.push('離開房間');
    btn.push('說：大家好');
    if (sel.auto) btn.push('交回自動');
    q('.iw-quick').innerHTML = btn.map(t => `<button class="iw-b" type="button" data-cmd="${t}">${t}</button>`).join('');
    renderCamButtons(); renderLog(); refreshDetail();
  }
  function refreshDetail() {
    if (!sel) return;
    const [t, c] = STATES[sel.state];
    q('.iw-state').innerHTML = `<span style="color:${c}">●</span> ${t}`;
    q('.iw-task').textContent = sel.task || '—';
    q('.iw-at').textContent = sel.dest ? '前往 ' + anchorZh(sel.dest) : (sel.at ? anchorZh(findAnchor(sel.at)) : '走道');
    q('.iw-en').textContent = Math.round(sel.energy * 100) + '%';
    q('.iw-bar i').style.width = (sel.energy * 100).toFixed(0) + '%';
    q('.iw-bar i').style.background = sel.energy < .35 ? '#ff6b6b' : '#3cc4ae';
    const v = Object.entries(sel.vars); q('.iw-vars').textContent = v.length ? v.map(([k, x]) => k + '=' + x).join('、') : '—';
    q('.iw-mode').textContent = '行為模式：' + ({ auto: '自動（Demo 隨機行程）', manual: '執行指令中', idle: '待命（由外部程式驅動）' }[sel.mode] || sel.mode)
      + (sel.queue.length ? `｜佇列 ${sel.queue.length}` : '');
  }

  // ============================================================ 對外 API
  const world = {
    get meta() { return meta; }, get nav() { return nav; }, get agents() { return agents; }, get selected() { return sel; },
    get camMode() { return cam.mode; }, get ws() { return ws; },
    setScene(m, navObj) {
      [...agents].forEach(a => remove(a.id)); deselect(false); cam.overview = null;
      statusLabels.forEach(L => scene.remove(L.sprite)); statusLabels.clear(); statusOcc.clear(); seatStatus.clear(); reserved.clear();
      meta = m; nav = null; anchors = []; doors = [];
      if (!m) return;
      anchors = m.anchors;
      doors = m.doors.map(d => ({ id: d.id, type: 'DOOR', use: 'door', position: d.position, yaw_deg: { S: 180, N: 0, W: 90, E: -90 }[d.wall] }));
      buildNav(navObj);
      const status = anchors.filter(a => a.type === 'STATUS');
      for (const s of anchors.filter(a => a.type === 'SEAT')) {
        let b = null, bd = 3.5; for (const t of status) { const d = Math.hypot(t.position[0] - s.position[0], t.position[1] - s.position[1]); if (d < bd) { bd = d; b = t; } }
        if (b) seatStatus.set(s.id, b.id);
      }
      for (const t of status) { const L = textSprite(.22); L.set('閒置', '#c8c8c8'); L.sprite.position.copy(B2T(t.position)); L.sprite.visible = false; scene.add(L.sprite); statusLabels.set(t.id, L); }
      hello();
    },
    startDemo() {
      this.stopDemo(); if (!nav) return; demoOn = true;
      statusLabels.forEach(L => L.sprite.visible = true);
      const seats = anchors.filter(a => a.type === 'SEAT');
      const homes = seats.filter(a => a.use === 'desk').concat(seats.filter(a => a.use !== 'desk' && a.use !== 'meeting'), seats.filter(a => a.use === 'meeting'));
      const n = Math.min(8, Math.max(2, Math.floor(seats.length * .5)));
      for (let i = 0; i < n; i++) {
        const [id, name, role] = DEMO_CAST[i];
        const ag = spawn({ id, name, role, auto: true, home: homes[i] && homes[i].id, energy: .45 + Math.random() * .55 });
        if (ag) ag.vars = { 模型: rnd(['大型', '中型', '小型']) };
      }
    },
    stopDemo() { demoOn = false; DEMO_CAST.forEach(([id]) => remove(id)); statusLabels.forEach(L => { L.set('閒置', '#c8c8c8'); L.sprite.visible = agents.length > 0; }); },
    showStatus(v) { statusLabels.forEach(L => L.sprite.visible = v); },
    update(dt) {
      for (const ag of agents) stepAgent(ag, dt);
      const showSt = agents.length > 0 && cam.mode !== 'shoulder';
      statusLabels.forEach(L => L.sprite.visible = showSt);
      stepCam(dt);
      panelT -= dt; if (panelT <= 0) { panelT = .25; refreshDetail(); if (agents.length) { const box = q('.iw-roster'); agents.forEach((ag, i) => { const s = box.children[i]?.querySelector('s'); if (s) s.textContent = STATES[ag.state][0]; }); } }
    },
    apply, command, select, deselect, setCamMode, connect, parseCommand: (t, id) => parseCommand(t, byId.get(id)),
    on(fn) { listeners.add(fn); return () => listeners.delete(fn); },
    get demoOn() { return demoOn; },
  };
  return world;
}
