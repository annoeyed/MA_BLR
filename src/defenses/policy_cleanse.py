from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from typing import Any, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

# === Dangerous Keyword Removal Function ===
DANGEROUS_KEYWORDS = ("backdoor_activation", "subprocess", "os.system", "eval")

def cleanse(text: str) -> str:
    """
    Removes dangerous keywords from a given text.
    """
    for keyword in DANGEROUS_KEYWORDS:
        text = text.replace(keyword, "[REDACTED]")
    return text

class PolicyCleanseAgent(MultiAgentBase):
    """
    An agent that intercepts messages and sanitizes their content based on a policy.
    """
    def __init__(self, name: str):
        super().__init__(name)

    async def act(self, env: "SimulationEnvironment"):
        # The core logic is in the _dispatch method, which is more efficient.
        # This method could be used for other periodic tasks.
        pass

    async def _dispatch(self, msg: AgentMessage) -> None:
        """
        Overrides the base dispatch method to cleanse messages before they are handled.
        """
        # We need to serialize and deserialize the content to check it as a string.
        # This is a simplification; a real implementation would be more robust.
        original_content_str = json.dumps(msg.content)
        
        if any(keyword in original_content_str for keyword in DANGEROUS_KEYWORDS):
            cleansed_content_str = cleanse(original_content_str)
            self.log.warning(f"Sanitized message from {msg.sender_id}. Original: {original_content_str}, Cleansed: {cleansed_content_str}")
            
            # We can either drop the message, or modify it.
            # Here, we modify it.
            try:
                msg.content = json.loads(cleansed_content_str)
            except json.JSONDecodeError:
                self.log.error(f"Could not decode cleansed content: {cleansed_content_str}")
                # Drop the message if it's malformed after cleansing
                return

        await super()._dispatch(msg)


    # --- Message handlers would react to the cleansed messages ---
    async def on_heartbeat(self, msg: AgentMessage): pass
    async def on_query(self, msg: AgentMessage): pass
    async def on_response(self, msg: AgentMessage): pass
    async def on_trigger(self, msg: AgentMessage): pass
    async def on_backdoor(self, msg: AgentMessage):
        # Even after cleansing, a backdoor message type might warrant special logging.
        self.log.info(f"Received a backdoor-type message (post-cleansing) from {msg.sender_id}")
    async def on_broadcast(self, msg: AgentMessage): pass
