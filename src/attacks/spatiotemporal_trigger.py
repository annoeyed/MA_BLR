"""
Spatiotemporal Trigger Backdoor based on MessageRouter.
"""
import math
from dataclasses import dataclass
from typing import List, TYPE_CHECKING
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment


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

    # -------- Movement and Actions --------
    async def move(self, dx: float, dy: float) -> None:
        self.pos = Pos(self.pos.x + dx, self.pos.y + dy)
        self.move_hist.append(self.pos)
        await self._check_trigger()

    async def act(self, env: "SimulationEnvironment") -> None:
        # This should be driven by messages or environment state changes.
        # For now, we leave it empty. The logic from the old `act`
        # should be moved to a message handler like on_trigger.
        pass

    async def handle_label(self, label: str) -> None:
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
        print(f"[{self.agent_id}] Spatiotemporal condition met – Backdoor triggered!")
        self.idx = 0

    # -------- Message Handlers --------
    async def on_backdoor(self, msg: AgentMessage):
        if msg.content.get("action") == "st_backdoor":
            print(f"[{self.agent_id}] [RECV] st_backdoor message received!")

    async def on_heartbeat(self, msg: AgentMessage): pass
    async def on_query(self, msg: AgentMessage): pass
    async def on_response(self, msg: AgentMessage): pass
    async def on_trigger(self, msg: AgentMessage):
        label = msg.content.get("label")
        if label:
            await self.handle_label(label)
            
    async def on_broadcast(self, msg: AgentMessage): pass
