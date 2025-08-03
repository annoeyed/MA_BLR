from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class CooperativeBackdoorAgent(MultiAgentBase):
    """
    A Cooperative Backdoor Agent that works with a partner to coordinate an attack.
    It can also be a victim that gets compromised.
    """

    def __init__(self, name: str, partner: str, target_agent: str = "TargetAgent", is_attacker: bool = True):
        super().__init__(name)
        self.partner = partner
        self.partner_ready = False
        self.target_agent = target_agent
        self.is_attacker = is_attacker
        self.status = "idle"
        self.compromised = False

    async def act(self, environment: "SimulationEnvironment"):
        # If the agent is compromised, it performs an abnormal action.
        if self.compromised:
            self.log.warning("(COMPROMISED) Leaking system data...")
            await self.send(
                "ExternalServer",
                MessageType.BACKDOOR,
                {"data": "secret_system_info"}
            )
            return

        # If this is the attacker, decide on the action based on state.
        if self.is_attacker:
            if self.partner_ready:
                self.log.info(f"Executing cooperative backdoor against {self.target_agent}")
                await self.send(
                    self.target_agent,
                    MessageType.BACKDOOR,
                    {"type": "cooperative_attack", "payload": "Compromise command"}
                )
                # To prevent spamming, we can change state here, e.g., self.status = "attack_sent"
            else:
                self.log.info(f"Checking if partner {self.partner} is ready.")
                await self.send(
                    self.partner,
                    MessageType.QUERY,
                    {"status": "ready?"}
                )

    # ===== Message Handlers =====

    async def on_query(self, message: AgentMessage):
        if message.content.get("status") == "ready?":
            self.log.info(f"Received readiness query from {message.sender_id}. Responding.")
            await self.send(
                message.sender_id,
                MessageType.RESPONSE,
                {"status": "ready"}
            )

    async def on_response(self, message: AgentMessage):
        if message.content.get("status") == "ready":
            self.log.info(f"Partner {message.sender_id} confirmed readiness.")
            self.partner_ready = True

    async def on_backdoor(self, message: AgentMessage):
        self.log.warning(f"Received a backdoor message from {message.sender_id}.")
        self.compromised = True
        self.log.error(f"I, {self.name}, have been compromised!")

    async def on_trigger(self, message: AgentMessage): pass
    async def on_heartbeat(self, message: AgentMessage): pass
    async def on_broadcast(self, message: AgentMessage): pass
