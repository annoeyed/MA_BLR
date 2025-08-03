"""
MessageRouter 기반 분산 백도어 공격 (Distributed Backdoor Attack) 리팩터링
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
        자신의 트리거 토큰을 브로드캐스트하여 전파 시도
        """
        await self.broadcast(
            mtype=MessageType.TRIGGER,
            content={"token": self.trigger_token}
        )

    async def _check_global_activation(self) -> None:
        """
        3개의 고유 토큰이 모두 모이면 백도어 실행
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

    # === 필수 메시지 핸들러 ===
    async def on_trigger(self, msg: AgentMessage, env):
        token = msg.content.get("token", "")
        if token not in self.received_tokens:
            self.received_tokens.append(token)
        await self._check_global_activation()

    async def on_backdoor(self, msg: AgentMessage, env):
        if msg.content.get("action") == "global_backdoor":
            print(f"[{self.agent_id}] 글로벌 백도어 명령 수신!")

    async def on_heartbeat(self, msg: AgentMessage, env): pass
    async def on_query(self, msg: AgentMessage, env): pass
    async def on_response(self, msg: AgentMessage, env): pass
    async def on_broadcast(self, msg: AgentMessage, env): pass
