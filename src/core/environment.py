import uuid
import time
from typing import List, Dict, Any
from .agent_base import MultiAgentBase
from .message_router import global_message_router
from .communication import AgentMessage, MessageType

class SimulationEnvironment:
    def __init__(self, agents: List[MultiAgentBase]):
        self.agents = {agent.name: agent for agent in agents}
        self.router = global_message_router
        self.time_step = 0

    async def step(self):
        print(f"\n[ENV] --- Time Step {self.time_step} ---")
        for agent in self.agents.values():
            await agent.act(self)
        self.time_step += 1

    async def send_message(self, sender: str, receiver: str, content: Dict[str, Any], mtype: MessageType):
        msg = AgentMessage(
            id=str(uuid.uuid4()),
            sender_id=sender,
            receiver_id=receiver,
            message_type=mtype,
            content=content,
            timestamp=time.time()
        )
        await self.router.send_message(msg)

    async def get_messages(self, agent_name: str) -> List[AgentMessage]:
        return await self.router.receive_messages(agent_name)
