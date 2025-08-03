# src/core/secure_comm.py
from .message_router import global_message_router

class SecureCommunicationProtocol:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        global_message_router.register_agent(agent_id)

    async def send(self, msg):
        await global_message_router.send_message(msg)

    def receive(self, agent_id: str):
        return global_message_router.receive(agent_id)
