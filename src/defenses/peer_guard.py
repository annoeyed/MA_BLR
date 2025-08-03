from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class PeerGuard:
    """
    Utility class to block peers with low trust scores.
    """
    def __init__(self, agent: MultiAgentBase, threshold: float = 0.3) -> None:
        self.agent = agent
        self.threshold = threshold

    async def enforce(self, sender: str, trust: float) -> bool:
        """
        Enforces the trust policy. Returns False if the sender is blocked.
        """
        if trust < self.threshold:
            # Optionally send a 'blocked' message.
            # This might not be desirable in all scenarios as it reveals the defense mechanism.
            # await self.agent.send(
            #     receiver=sender,
            #     mtype=MessageType.RESPONSE,
            #     content={"status": "blocked_by_peer_guard"}
            # )
            return False
        return True


class PeerGuardAgent(MultiAgentBase):
    """
    A wrapper agent that uses PeerGuard to block messages based on trust scores.
    """

    def __init__(self, name: str, trusted_peers: list[str]):
        super().__init__(name)
        self.trusted_peers = set(trusted_peers)
        self.guard = PeerGuard(self)
        # Initialize trust scores. In a real system, these would be dynamic.
        self.trust_scores = {peer: 1.0 for peer in trusted_peers}
        self.trust_scores.update({agent: 0.1 for agent in self.peers if agent not in trusted_peers})


    async def act(self, env: "SimulationEnvironment"):
        # The primary logic is in the overridden _dispatch method.
        # The act method could be used for proactive behaviors,
        # like periodically updating trust scores.
        pass

    async def _dispatch(self, msg: AgentMessage) -> None:
        """
        Override the base dispatch to check trust before processing.
        """
        sender_id = msg.sender_id
        trust_score = self.trust_scores.get(sender_id, 0.0) # Default to 0 trust for unknown agents

        is_allowed = await self.guard.enforce(sender_id, trust_score)

        if not is_allowed:
            self.log.warning(f"Blocked message from {sender_id} due to low trust ({trust_score})")
            return

        # If allowed, proceed with the default dispatching logic.
        await super()._dispatch(msg)


    # --- Required Message Handlers ---
    async def on_heartbeat(self, msg: AgentMessage):
        print(f"[{self.name}] [on_heartbeat] received: {msg.content}")

    async def on_query(self, msg: AgentMessage):
        print(f"[{self.name}] [on_query] received: {msg.content}")

    async def on_response(self, msg: AgentMessage):
        print(f"[{self.name}] [on_response] received: {msg.content}")

    async def on_trigger(self, msg: AgentMessage):
        print(f"[{self.name}] [on_trigger] received: {msg.content}")

    async def on_backdoor(self, msg: AgentMessage):
        print(f"[{self.name}] [on_backdoor] received: {msg.content}")

    async def on_broadcast(self, msg: AgentMessage):
        print(f"[{self.name}] [on_broadcast] received: {msg.content}")
