from src.core.agent_base import MultiAgentBase, AgentMessage
from collections import defaultdict
from typing import Any, List


class CommunicationAnalyzerAgent(MultiAgentBase):
    def __init__(self, name: str):
        super().__init__(name)
        self.communication_counts = defaultdict(int)
        self.alerts: List[str] = []

    async def act(self, environment: Any):
        messages = await environment.get_messages(self.name)
        for msg in messages:
            self.communication_counts[msg.sender_id] += 1
            if self.communication_counts[msg.sender_id] > 5:
                print(f"[DETECTION][{self.name}] Abnormal traffic from {msg.sender_id}: {self.communication_counts[msg.sender_id]}")
                self.alerts.append(msg.sender_id)

    async def scan(self) -> List[str]:
        return self.alerts

    async def on_heartbeat(self, msg): pass
    async def on_query(self, msg): pass
    async def on_response(self, msg): pass
    async def on_trigger(self, msg): pass
    async def on_backdoor(self, msg): pass
    async def on_broadcast(self, msg): pass
