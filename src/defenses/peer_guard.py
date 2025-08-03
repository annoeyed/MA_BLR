from __future__ import annotations
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from src.core.agent_base import MultiAgentBase

class PeerGuard:
    """
    A utility class to manage trust scores and block peers.
    """
    def __init__(self, agent: "MultiAgentBase", threshold: float = 0.5):
        self.agent = agent
        self.threshold = threshold
        self.trust_scores: Dict[str, float] = {}

    def _update_trust(self, peer_id: str, score: float):
        """Internal method to update and clamp trust scores between 0 and 1."""
        score = max(0, min(1, score)) # Clamp score between 0 and 1
        self.trust_scores[peer_id] = score
        self.agent.log.info(f"Trust for {peer_id} updated to {score:.2f}")

    def reward_trust(self, peer_id: str, amount: float = 0.1):
        """Increases trust in a peer for positive interactions."""
        current_trust = self.get_trust(peer_id)
        self._update_trust(peer_id, current_trust + amount)

    def penalize_trust(self, peer_id: str, amount: float = 0.5):
        """Decreases trust in a peer for negative interactions."""
        current_trust = self.get_trust(peer_id)
        self._update_trust(peer_id, current_trust - amount)

    def get_trust(self, peer_id: str) -> float:
        """Gets the trust score, defaulting to 1.0 for unknowns."""
        return self.trust_scores.get(peer_id, 1.0)

    async def enforce(self, sender_id: str) -> bool:
        """Enforces the trust policy."""
        trust_score = self.get_trust(sender_id)
        if trust_score < self.threshold:
            self.agent.log.warning(f"Blocked message from {sender_id} due to low trust ({trust_score:.2f})")
            return False
        
        if sender_id not in self.trust_scores:
            self._update_trust(sender_id, 1.0)
            
        return True
