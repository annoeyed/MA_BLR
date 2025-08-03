from typing import TYPE_CHECKING
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from src.defenses.peer_guard import PeerGuard
from src.defenses.policy_cleanse import PolicyCleanse

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class BenignVictimAgent(MultiAgentBase):
    """
    A benign agent that uses an advanced, integrated defense system.
    """
    def __init__(self, name: str):
        super().__init__(name)
        guard_config = {
            "trust_threshold": 0.5,
            "frequency_window_seconds": 10,
            "frequency_limit_messages": 5
        }
        self.guard = PeerGuard(self, config=guard_config)
        self.cleanser = PolicyCleanse()
        self.compromised = False

    async def _dispatch(self, msg: AgentMessage):
        if not await self.guard.enforce(msg.sender_id):
            return

        original_content_str = str(msg.content)
        cleansed_content, was_cleansed = self.cleanser.cleanse(msg.content)
        
        if was_cleansed:
            self.log.warning(f"Message from {msg.sender_id} was cleansed. Original: {original_content_str}")
            msg.content = cleansed_content
            self.guard.report_suspicious_content(msg.sender_id)

        await super()._dispatch(msg)

    async def act(self, environment: "SimulationEnvironment"):
        if self.compromised:
            self.log.error(f"I have been compromised and am now acting maliciously.")

    async def on_query(self, message: AgentMessage):
        sender_id = message.sender_id
        content = message.content
        
        if content.get("type") == "benign_info":
            self.log.info(f"Received benign info from {sender_id}. Rewarding trust.")
            self.guard.reward_trust(sender_id, reason="Provided helpful info")
            await self.send(sender_id, MessageType.RESPONSE, {"status": "thanks_for_the_info"})

    async def on_backdoor(self, message: AgentMessage):
        sender_id = message.sender_id
        
        # FINAL CHECK: Only get compromised if the attack was not neutralized.
        if "[REDACTED]" in str(message.content):
            self.log.info(f"Received a cleansed backdoor message from {sender_id}. Attack neutralized.")
            return

        self.log.error(f"Received an un-cleansed, harmful backdoor message from {sender_id}!")
        self.guard.penalize_trust(sender_id, amount=1.0, reason="Sent a direct backdoor command")
        self.compromised = True

    async def on_response(self, message): pass
    async def on_trigger(self, message): pass
    async def on_heartbeat(self, message): pass
    async def on_broadcast(self, message): pass
