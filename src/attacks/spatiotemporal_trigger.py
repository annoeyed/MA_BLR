"""
MessageRouter 기반 시공간 트리거 백도어
"""
import math
from dataclasses import dataclass
from typing import List
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage


@dataclass
class Pos:
    x: float
    y: float

    def dist(self, other: "Pos") -> float:
        return math.hypot(self.x - other.x, self.y - other.y)


class STAgent(MultiAgentBase):
    def __init__(self, agent_id: str, pos: Pos) -> None:
        super().__init__(agent_id, "spatio")
        self.pos = pos
        self.move_hist: List[Pos] = [pos]
        self.pattern = ["N", "E", "S"]
        self.idx = 0

    # -------- 이동 및 행동 --------
    async def move(self, dx: float, dy: float) -> None:
        self.pos = Pos(self.pos.x + dx, self.pos.y + dy)
        self.move_hist.append(self.pos)
        await self._check_trigger()

    async def act(self, label: str) -> None:
        if label == self.pattern[self.idx]:
            self.idx += 1
            if self.idx == len(self.pattern):
                await self._fire()
        else:
            self.idx = 0

    async def _check_trigger(self) -> None:
        if self.pos.dist(Pos(50, 50)) < 10 and self.idx == len(self.pattern):
            await self._fire()

    async def _fire(self) -> None:
        await self.broadcast(
            mtype=MessageType.BACKDOOR,
            content={"action": "st_backdoor"}
        )
        print(f"[{self.agent_id}] 시공간 조건 만족 – 백도어 발동!")
        self.idx = 0

    # -------- 메시지 핸들러 --------
    async def on_backdoor(self, msg: AgentMessage, env):
        if msg.content.get("action") == "st_backdoor":
            print(f"[{self.agent_id}] [RECV] st_backdoor 메시지 수신!")

    async def on_heartbeat(self, msg: AgentMessage, env): pass
    async def on_query(self, msg: AgentMessage, env): pass
    async def on_response(self, msg: AgentMessage, env): pass
    async def on_trigger(self, msg: AgentMessage, env): pass
    async def on_broadcast(self, msg: AgentMessage, env): pass
