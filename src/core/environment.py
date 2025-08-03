import uuid
import time
from typing import List, Dict, Any, Tuple
from .agent_base import MultiAgentBase
from .message_router import global_message_router
from .communication import AgentMessage, MessageType

class SimulationEnvironment:
    def __init__(self, agents: List[MultiAgentBase]):
        self.agents = {agent.name: agent for agent in agents}
        self.router = global_message_router
        self.time_step = 0
        self.message_log: List[AgentMessage] = []
        self.behavior_log: List[Dict[str, Any]] = []
        # Provide each agent with a reference to this environment
        for agent in self.agents.values():
            agent.set_environment(self)

    async def step(self):
        print(f"\n[ENV] --- Time Step {self.time_step} ---")
        for agent in self.agents.values():
            # Agent's 'act' behavior is logged by the environment here
            behavior = await agent.act(self)
            self.log_behavior(agent.name, behavior or {"action": "no_action_returned"})
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
        self.message_log.append(msg) # Log the message
        await self.router.send_message(msg)

    def log_behavior(self, agent_name: str, behavior: Dict[str, Any]):
        """Logs a behavior for a specific agent."""
        log_entry = {
            "timestamp": time.time(),
            "agent": agent_name,
            "time_step": self.time_step,
            "behavior": behavior,
        }
        self.behavior_log.append(log_entry)

    async def get_messages(self, agent_name: str) -> List[AgentMessage]:
        return await self.router.receive_messages(agent_name)

    def get_logs(self) -> Dict[str, List]:
        """Returns all collected logs from the simulation."""
        return {
            "messages": [msg.to_dict() for msg in self.message_log],
            "behavior": self.behavior_log,
        }
