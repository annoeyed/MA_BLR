import asyncio
from collections import defaultdict

class MessageRouter:
    def __init__(self):
        self.queues = defaultdict(asyncio.Queue)

    def register_agent(self, agent_id: str):
        # This will create a new queue if one doesn't exist for the agent_id
        return self.queues[agent_id]

    async def send_message(self, message):
        receiver_queue = self.queues.get(message.receiver_id)
        if receiver_queue:
            await receiver_queue.put(message)
    
    def reset(self):
        """
        Clears all agent queues. Should be called between independent
        simulation runs within the same process to prevent state leakage.
        """
        self.queues = defaultdict(asyncio.Queue)

# Global singleton instance of the MessageRouter
global_message_router = MessageRouter()
