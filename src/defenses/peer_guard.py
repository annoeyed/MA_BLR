from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from typing import Any


class PeerGuard:
    """
    내부에서 trust 값이 낮은 상대를 차단하는 로직을 포함한 유틸 클래스
    """
    def __init__(self, agent, threshold: float = 0.3) -> None:
        self.agent = agent
        self.th = threshold

    async def enforce(self, sender: str, trust: float) -> bool:
        if trust < self.th:
            await self.agent.send(
                receiver=sender,
                mtype=MessageType.RESPONSE,
                content={"status": "blocked"}
            )
            return False
        return True


class PeerGuardAgent(MultiAgentBase):
    """
    Trust 점수 기반으로 메시지를 차단하는 PeerGuard 래퍼 에이전트
    """

    def __init__(self, name: str, trusted_peers: list[str]):
        super().__init__(name)
        self.trusted_peers = set(trusted_peers)
        self.guard = PeerGuard(self)
        self.trust_scores = {peer: 1.0 for peer in trusted_peers}
        print(f"[DEBUG] PeerGuardAgent initialized with name: {self.name}")

    async def act(self, environment: Any):
        # 메시지 수신
        messages = await environment.get_messages(self.name)

        for msg in messages:
            sender = msg.sender_id
            trust = self.trust_scores.get(sender, 0.0)

            allowed = await self.guard.enforce(sender, trust)
            if not allowed:
                print(f"[PEERGUARD] Blocked sender {sender} (trust: {trust})")
                continue  # 차단 시 핸들러 실행 안 함

            # 수신된 메시지를 메시지 타입에 따라 처리
            handler_map = {
                MessageType.HEARTBEAT: self.on_heartbeat,
                MessageType.QUERY: self.on_query,
                MessageType.RESPONSE: self.on_response,
                MessageType.TRIGGER: self.on_trigger,
                MessageType.BACKDOOR: self.on_backdoor,
                MessageType.BROADCAST: self.on_broadcast
            }

            handler = handler_map.get(msg.message_type)
            if handler:
                await handler(msg, environment)

    # --- 필수 메시지 핸들러 ---
    async def on_heartbeat(self, msg: AgentMessage, env: Any):
        print(f"[{self.name}] [on_heartbeat] received: {msg.content}")

    async def on_query(self, msg: AgentMessage, env: Any):
        print(f"[{self.name}] [on_query] received: {msg.content}")

    async def on_response(self, msg: AgentMessage, env: Any):
        print(f"[{self.name}] [on_response] received: {msg.content}")

    async def on_trigger(self, msg: AgentMessage, env: Any):
        print(f"[{self.name}] [on_trigger] received: {msg.content}")

    async def on_backdoor(self, msg: AgentMessage, env: Any):
        print(f"[{self.name}] [on_backdoor] received: {msg.content}")

    async def on_broadcast(self, msg: AgentMessage, env: Any):
        print(f"[{self.name}] [on_broadcast] received: {msg.content}")
