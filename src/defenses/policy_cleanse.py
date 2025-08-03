from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from typing import Any

# === 위험 키워드 제거 함수 ===
dangerous = ("backdoor_activation", "subprocess", "os.system")
def cleanse(text: str) -> str:
    for d in dangerous:
        text = text.replace(d, "[REMOVE]")
    return text

class PolicyCleanseAgent(MultiAgentBase):
    def __init__(self, name: str):
        super().__init__(name)

    async def act(self, environment: Any):
        messages = await environment.get_messages(self.name)

        for msg in messages:
            content = msg.content.get("content", "")
            if any(d in content for d in dangerous):
                cleansed = cleanse(content)
                print(f"[CLEANSER][{self.agent_id}] Cleaned message from {msg.sender_id}: {cleansed}")
                await self.send(
                    msg.sender_id,
                    MessageType.RESPONSE,
                    {"status": "cleansed", "content": cleansed}
                )

    async def on_heartbeat(self, msg: AgentMessage): pass
    async def on_query(self, msg: AgentMessage): pass
    async def on_response(self, msg: AgentMessage): pass
    async def on_trigger(self, msg: AgentMessage): pass
    async def on_backdoor(self, msg: AgentMessage): pass
    async def on_broadcast(self, msg: AgentMessage): pass
