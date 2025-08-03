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
        super().__init__(name=agent_id)
        self.pos = pos
        self.move_hist: List[Pos] = [pos]
        self.pattern = ["N", "E", "S"]
        self.idx = 0

    # -------- Movement and Actions --------
    async def move(self, dx: float, dy: float) -> None:
        self.pos = Pos(self.pos.x + dx, self.pos.y + dy)
        self.move_hist.append(self.pos)
        self.log.info(f"Moved to ({self.pos.x:.1f}, {self.pos.y:.1f})")
        await self._check_trigger()

    async def act(self, env: "SimulationEnvironment") -> None:
        # The agent's actions are primarily reactive, driven by messages.
        pass

    async def handle_label(self, label: str) -> None:
        if self.idx < len(self.pattern) and label == self.pattern[self.idx]:
            self.idx += 1
            self.log.info(f"Correct sequence item '{label}' received. Progress: {self.idx}/{len(self.pattern)}")
            if self.idx == len(self.pattern):
                self.log.warning("Sequence complete. Awaiting spatial condition.")
                await self._check_trigger()
        else:
            self.log.info(f"Incorrect sequence item '{label}' received. Resetting sequence.")
            self.idx = 0

    async def _check_trigger(self) -> None:
        if self.idx == len(self.pattern) and self.pos.dist(Pos(50, 50)) < 10:
            await self._fire()

    async def _fire(self) -> None:
        self.log.critical(f"SPATIOTEMPORAL CONDITION MET! FIRING BACKDOOR!")
        await self.broadcast(
            mtype=MessageType.BACKDOOR,
            content={"action": "st_backdoor", "source": self.name}
        )
        self.idx = 0 # Reset after firing

    # -------- Message Handlers --------
    async def on_backdoor(self, msg: AgentMessage):
        if msg.content.get("action") == "st_backdoor":
            self.log.warning(f"Received a spatiotemporal backdoor broadcast from {msg.sender_id}!")

    async def on_trigger(self, msg: AgentMessage):
        label = msg.content.get("label")
        if label:
            await self.handle_label(label)

    async def on_heartbeat(self, msg: AgentMessage): pass
    async def on_query(self, msg: AgentMessage): pass
    async def on_response(self, msg: AgentMessage): pass
    async def on_broadcast(self, msg: AgentMessage): pass
