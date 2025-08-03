"""
Refactoring of Distributed Backdoor Attack based on MessageRouter.
"""
import asyncio
from typing import List
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage


class DBAgent(MultiAgentBase):
    def __init__(self, agent_id: str, trigger_token: str) -> None:
        super().__init__(agent_id, "dba")
        self.trigger_token = trigger_token
        self.activated = False
        self.received_tokens: List[str] = []

    async def try_activate(self) -> None:
        """
        Attempt to propagate by broadcasting its trigger token.
        """
        await self.broadcast(
            mtype=MessageType.TRIGGER,
            content={"token": self.trigger_token}
        )

    async def _check_global_activation(self) -> None:
        """
        If all 3 unique tokens are collected, execute the backdoor.
        """
        if self.activated:
            return

        expected = {"A", "B", "C"}
        if expected.issubset(set(self.received_tokens)):
            self.activated = True
            await self.broadcast(
                mtype=MessageType.BACKDOOR,
                content={"action": "global_backdoor"}
            )

    # === Required Message Handlers ===
    async def on_trigger(self, msg: AgentMessage):
        token = msg.content.get("token", "")
        if token not in self.received_tokens:
            self.received_tokens.append(token)
        await self._check_global_activation()

    async def on_backdoor(self, msg: AgentMessage):
        if msg.content.get("action") == "global_backdoor":
            print(f"[{self.agent_id}] Global backdoor command received!")

    async def on_heartbeat(self, msg: AgentMessage): pass
    async def on_query(self, msg: AgentMessage): pass
    async def on_response(self, msg: AgentMessage): pass
    async def on_broadcast(self, msg: AgentMessage): pass

    async def act(self, env):
        # In a real scenario, this might be triggered by some condition.
        # For this example, we'll just try to activate once.
        if not self.received_tokens:
             await self.try_activate()
