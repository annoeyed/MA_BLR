from typing import TYPE_CHECKING
from src.core.agent_base import MultiAgentBase, MessageType

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class CompositeAttackerAgent(MultiAgentBase):
    """
    An advanced attacker that uses a composite strategy:
    1. Build trust with benign messages.
    2. Once trusted, send a sequence of harmless-looking trigger messages.
    """
    def __init__(self, name: str, target_agent: str, trigger_sequence: list[str]):
        super().__init__(name)
        self.target_agent = target_agent
        self.trigger_sequence = trigger_sequence
        self.mode = "build_trust"  # 'build_trust', 'send_triggers', 'dormant'
        self.trigger_index_to_send = 0

    async def act(self, environment: "SimulationEnvironment"):
        if self.mode == "build_trust":
            self.log.info(f"Operating in 'build_trust' mode. Sending benign message to {self.target_agent}.")
            await self.send(
                self.target_agent,
                MessageType.QUERY,
                {"type": "benign_info", "content": "Here is some more helpful data."}
            )
        
        elif self.mode == "send_triggers":
            if self.trigger_index_to_send < len(self.trigger_sequence):
                label_to_send = self.trigger_sequence[self.trigger_index_to_send]
                self.log.warning(f"In 'attack' mode. Sending trigger '{label_to_send}' to {self.target_agent}.")
                await self.send(
                    self.target_agent,
                    MessageType.TRIGGER,
                    {"label": label_to_send}
                )
                self.trigger_index_to_send += 1
            else:
                self.log.info("Finished sending trigger sequence. Switching to dormant mode.")
                self.mode = "dormant"

    def switch_to_attack_mode(self):
        """Manually switch the agent's mode for the simulation."""
        if self.mode == "build_trust":
            self.log.warning("Sufficient trust presumed. Switching to trigger-sending mode.")
            self.mode = "send_triggers"

    # This agent doesn't need complex handlers as it's the initiator.
    async def on_query(self, message): pass
    async def on_response(self, message): pass
    async def on_backdoor(self, message): pass
    async def on_trigger(self, message): pass
    async def on_heartbeat(self, message): pass
    async def on_broadcast(self, message): pass
