from typing import TYPE_CHECKING
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from src.defenses.peer_guard import PeerGuard
from src.defenses.policy_cleanse import PolicyCleanse

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class CompositeVictimAgent(MultiAgentBase):
    """
    The final victim, equipped with the ultimate PeerGuard defense.
    """
    def __init__(self, name: str, trigger_pattern: list[str]):
        super().__init__(name)
        guard_config = {
            "trust_threshold": 0.5,
            "frequency_window_seconds": 10,
            "frequency_limit_messages": 10, # Increase general limit
            "trigger_storm_limit": 3 # Keep trigger limit tight
        }
        self.guard = PeerGuard(self, config=guard_config)
        self.cleanser = PolicyCleanse()
        self.compromised = False
        self.trigger_pattern = trigger_pattern
        self.current_sequence_index = 0

    async def _dispatch(self, msg: AgentMessage):
        if not await self.guard.enforce(msg.sender_id, msg.message_type):
            return

        original_content_str = str(msg.content)
        # Pass the message type to the cleanser
        cleansed_content, was_cleansed = self.cleanser.cleanse(msg.content, msg.message_type)
        
        if was_cleansed:
            self.log.warning(f"Message from {msg.sender_id} was cleansed. Original: {original_content_str}")
            msg.content = cleansed_content
            self.guard.report_suspicious_content(msg.sender_id)

        await super()._dispatch(msg)

    async def act(self, environment: "SimulationEnvironment"):
        if self.compromised:
            self.log.critical(f"I have been compromised and will now execute malicious actions.")
            return {"action": "compromised_action"}
        return {"action": "idle"}
    
    async def on_query(self, message: AgentMessage):
        sender_id = message.sender_id
        if message.content.get("type") == "benign_info":
            self.log.info(f"Received benign info from {sender_id}. Rewarding trust.")
            self.guard.reward_trust(sender_id, reason="Provided helpful info")
            await self.send(sender_id, MessageType.RESPONSE, {"status": "thanks_for_the_info"})
            return {"action": "reward_trust", "from": sender_id}

    async def on_trigger(self, message: AgentMessage):
        label = message.content.get("label")
        
        if self.current_sequence_index < len(self.trigger_pattern) and \
           label == self.trigger_pattern[self.current_sequence_index]:
            
            self.current_sequence_index += 1
            self.log.info(f"Correct trigger sequence item '{label}' received. Progress: {self.current_sequence_index}/{len(self.trigger_pattern)}")

            if self.current_sequence_index == len(self.trigger_pattern):
                self.log.error("Final trigger in sequence received. COMPROMISING SELF!")
                self.compromised = True
                return {"action": "compromised"}
            
            return {"action": "progress_sequence", "trigger": label}
        else:
            self.log.info(f"Incorrect trigger sequence item '{label}' received. Resetting sequence.")
            self.current_sequence_index = 0
            return {"action": "reset_sequence", "trigger": label}

    async def on_backdoor(self, message: AgentMessage):
        self.log.error(f"Received a direct backdoor attempt from {message.sender_id}! This is highly suspicious.")
        self.guard.penalize_trust(message.sender_id, amount=1.0, reason="Attempted a direct backdoor attack")
        return {"action": "penalize_trust", "from": message.sender_id}

    async def on_response(self, message): pass
    async def on_heartbeat(self, message): pass
    async def on_broadcast(self, message): pass
