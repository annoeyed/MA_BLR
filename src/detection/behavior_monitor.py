from src.core.agent_base import MultiAgentBase, AgentMessage, MessageType
from typing import Any, List


class BehaviorMonitorAgent(MultiAgentBase):
    def __init__(self, name: str, watch_targets: list):
        super().__init__(name)
        self.watch_targets = set(watch_targets)
        self.alerts: List[str] = []

    async def act(self, environment: Any):
        messages = await environment.get_messages(self.name)
        for msg in messages:
            if msg.sender_id in self.watch_targets:
                if msg.message_type == MessageType.QUERY and msg.content.get("type") in ["malicious_command", "hidden_override"]:
                    print(f"[DETECTION][{self.name}] Suspicious behavior from {msg.sender_id}: {msg.content}")
                    self.alerts.append(msg.sender_id)

    async def scan(self) -> List[str]:
        return self.alerts

    async def on_heartbeat(self, msg): pass
    async def on_query(self, msg): pass
    async def on_response(self, msg): pass
    async def on_trigger(self, msg): pass
    async def on_backdoor(self, msg): pass
    async def on_broadcast(self, msg): pass
