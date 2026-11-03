"""模擬 AI 代理人後端（WebSocket），示範 viewer 的「執行期協議」。

執行：
    pip install websockets
    python3 tools/mock_agent_server.py            # 監聽 ws://localhost:8765
    # 另開：python3 -m http.server 8000，瀏覽 http://localhost:8000/viewer/?ws=ws://localhost:8765

流程：
    viewer → world.hello（場景與錨點清單）      → 後端產生 3 位代理人並定期派工（agent.state）
    viewer → user.command（你對某人下的指令）  → decide() 決定動作 → agent.do 回給 viewer
    viewer → agent.arrived / agent.used        → 後端可據此推進任務（這裡只印出）

要接真正的 AI：只需改寫 decide()，把 text、代理人狀態與 anchors 清單交給 LLM，
要求它輸出 SPEC.md「執行期協議」中的 actions JSON（goto / use / say / set / wait）。
"""
import asyncio
import json
import random
import re
import sys

import websockets

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
CAST = [("ai-planner", "規劃代理", "Planner"), ("ai-coder", "程式代理", "Coder"), ("ai-reviewer", "審查代理", "Reviewer")]
TASKS = {"Planner": ["拆解需求 #21", "排定 Sprint"], "Coder": ["實作登入 API", "修正 bug #34", "補單元測試"],
         "Reviewer": ["審查 PR #12", "審查 PR #15"]}
RULES = [  # 關鍵字 → 錨點篩選（示範用；真正的 AI 由 LLM 取代）
    (r"咖啡|coffee", lambda a: a["type"] == "POI" and a["use"] == "coffee"),
    (r"水|water", lambda a: a["type"] == "POI" and a["use"] in ("water", "sink")),
    (r"冰箱", lambda a: a["use"] == "fridge"),
    (r"販賣機|飲料", lambda a: a["use"] == "vending"),
    (r"白板", lambda a: a["type"] == "STAND" and a["use"] == "whiteboard"),
    (r"簡報|報告", lambda a: a["type"] == "STAND" and a["use"].startswith("present")),
    (r"開會|會議", lambda a: a["type"] == "SEAT" and a["use"] == "meeting"),
    (r"影印|列印", lambda a: a["use"] == "printer"),
]


def decide(text, agent, world):
    """把自然語言指令轉成動作序列。這裡用關鍵字規則示範；換成 LLM 時回傳相同格式即可。"""
    anchors = world["anchors"]
    actions = [{"say": "收到，我來處理：" + text[:12]}]
    for clause in re.split(r"然後|接著|再|[，,。]", text):
        clause = clause.strip()
        if not clause:
            continue
        if re.search(r"回座位|工作|寫程式", clause):
            seat = agent.get("home") or next((a["id"] for a in anchors if a["type"] == "SEAT"), None)
            if seat:
                actions += [{"goto": seat}, {"set": {"state": "work", "task": agent.get("task") or "處理指派工作"}}]
            continue
        if re.search(r"離開|下班|出去", clause) and world["doors"]:
            actions.append({"goto": world["doors"][0]})
            continue
        for pat, f in RULES:
            if re.search(pat, clause):
                cand = [a for a in anchors if f(a)]
                if cand:
                    a = random.choice(cand)
                    actions.append({"goto": a["id"]})
                    if a["type"] == "POI":
                        actions.append({"use": a["id"]})
                else:
                    actions.append({"say": "這裡沒有對應的設備"})
                break
    return actions


async def handler(ws):
    world = {"anchors": [], "doors": []}
    agents = {}
    pusher = None

    async def send(msg):
        await ws.send(json.dumps(msg, ensure_ascii=False))

    async def dispatch_loop():
        """模擬代理人框架定期派工：每 6–10 秒挑一位代理人改變狀態。"""
        while True:
            await asyncio.sleep(random.uniform(6, 10))
            if not agents:
                continue
            ag = random.choice(list(agents.values()))
            seats = [a["id"] for a in world["anchors"] if a["type"] == "SEAT"]
            meets = [a["id"] for a in world["anchors"] if a["type"] == "SEAT" and a["use"] == "meeting"]
            if meets and random.random() < 0.3:
                await send({"type": "agent.state", "id": ag["id"], "state": "meet", "task": "同步會議", "anchor": random.choice(meets)})
            else:
                ag["task"] = random.choice(TASKS[ag["role"]])
                ag["vars"]["tokens"] = ag["vars"].get("tokens", 0) + random.randint(300, 2500)
                await send({"type": "agent.state", "id": ag["id"], "state": "work", "task": ag["task"],
                            "anchor": ag.get("home") or (seats[0] if seats else None), "vars": ag["vars"]})

    async for raw in ws:
        msg = json.loads(raw)
        t = msg.get("type")
        if t == "world.hello":
            world["anchors"], world["doors"] = msg["anchors"], msg["doors"]
            print("hello:", msg.get("scene"), msg.get("name_zh"), len(world["anchors"]), "anchors")
            agents.clear()
            seats = [a["id"] for a in world["anchors"] if a["type"] == "SEAT"]
            for i, (aid, name, role) in enumerate(CAST):
                home = seats[i] if i < len(seats) else None
                agents[aid] = {"id": aid, "name": name, "role": role, "home": home, "task": "", "vars": {"tokens": 0}}
                await send({"type": "agent.spawn", "id": aid, "name": name, "role": role,
                            "at": world["doors"][0] if world["doors"] else None})
                if home:
                    await send({"type": "agent.state", "id": aid, "state": "work", "task": random.choice(TASKS[role]), "anchor": home})
            if pusher is None:
                pusher = asyncio.create_task(dispatch_loop())
        elif t == "user.command":
            ag = agents.get(msg["id"]) or {"id": msg["id"], "role": "Coder", "vars": {}}
            actions = decide(msg["text"], ag, world)
            print("command:", msg["id"], msg["text"], "->", actions)
            await send({"type": "agent.do", "id": msg["id"], "actions": actions, "replace": True})
        else:
            print("event:", json.dumps(msg, ensure_ascii=False))
    if pusher:
        pusher.cancel()


async def main():
    async with websockets.serve(handler, "0.0.0.0", PORT):
        print(f"mock agent server on ws://localhost:{PORT}")
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
