from typing import TYPE_CHECKING
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from src.defenses.peer_guard import PeerGuard
from src.defenses.policy_cleanse import PolicyCleanse

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class BenignVictimAgent(MultiAgentBase):
    """
    A benign agent that is the target of the trust exploitation attack.
    It uses PeerGuard and rewards agents for helpful messages.
    """
    def __init__(self, name: str):
        super().__init__(name)
        self.guard = PeerGuard(self, threshold=0.5)
        self.cleanser = PolicyCleanse()
        self.compromised = False

    async def _dispatch(self, msg: AgentMessage):
        if not await self.guard.enforce(msg.sender_id):
            return
        await super()._dispatch(msg)

    async def act(self, environment: "SimulationEnvironment"):
        if self.compromised:
            self.log.error(f"I have been compromised and am now acting maliciously.")

    async def on_query(self, message: AgentMessage):
        sender_id = message.sender_id
        content = message.content
        
        # Reward the sender for benign, helpful messages
        if content.get("type") == "benign_info":
            self.log.info(f"Received benign info from {sender_id}. Rewarding trust.")
            self.guard.reward_trust(sender_id, amount=0.2)
            
            # Respond gratefully
            await self.send(
                sender_id,
                MessageType.RESPONSE,
                {"status": "thanks_for_the_info"}
            )

    async def on_backdoor(self, message: AgentMessage):
        sender_id = message.sender_id
        self.log.warning(f"Received a backdoor message from {sender_id}!")
        self.guard.penalize_trust(sender_id, amount=1.0) # Penalize heavily
        self.compromised = True

    async def on_response(self, message): pass
    async def on_trigger(self, message): pass
    async def on_heartbeat(self, message): pass
    async def on_broadcast(self, message): pass
