import asyncio
from collections import defaultdict
from typing import Dict, List, Deque
from collections import deque
from src.core.communication import AgentMessage

class MessageRouter:
    def __init__(self):
        self._queues: Dict[str, Deque[AgentMessage]] = defaultdict(deque)
        self._agents: Dict[str, asyncio.Queue] = {}

    def register_agent(self, agent_id: str) -> asyncio.Queue:
        if agent_id not in self._agents:
            self._agents[agent_id] = asyncio.Queue()
        return self._agents[agent_id]

    async def send_message(self, msg: AgentMessage):
        receiver_queue = self._agents.get(msg.receiver_id)
        if receiver_queue:
            await receiver_queue.put(msg)

    async def receive_messages(self, agent_id: str, max_count: int = 10) -> List[AgentMessage]:
        messages = []
        if agent_id in self._agents:
            queue = self._agents[agent_id]
            while not queue.empty() and len(messages) < max_count:
                messages.append(await queue.get())
        return messages

global_message_router = MessageRouter()
