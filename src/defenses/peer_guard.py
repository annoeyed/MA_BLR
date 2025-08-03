from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Tuple
from collections import defaultdict
import time

if TYPE_CHECKING:
    from src.core.agent_base import MultiAgentBase, MessageType

class PeerGuard:
    """
    The ultimate defense system. Manages trust based on behavior, frequency,
    content risk, and now, suspicious message patterns.
    """
    def __init__(self, agent: "MultiAgentBase", config: Dict):
        self.agent = agent
        self.threshold = config.get("trust_threshold", 0.5)
        self.frequency_window = config.get("frequency_window_seconds", 10)
        self.frequency_limit = config.get("frequency_limit_messages", 5)
        self.trigger_storm_limit = config.get("trigger_storm_limit", 3)

        self.trust_scores: Dict[str, float] = {}
        # Store (timestamp, MessageType) tuples
        self.message_history: Dict[str, List[Tuple[float, "MessageType"]]] = defaultdict(list)

    def _update_trust(self, peer_id: str, score: float, reason: str):
        score = max(0, min(1, score))
        self.trust_scores[peer_id] = score
        self.agent.log.info(f"Trust for {peer_id} updated to {score:.2f}. Reason: {reason}")

    def reward_trust(self, peer_id: str, amount: float = 0.1, reason: str = "Positive interaction"):
        current_trust = self.get_trust(peer_id)
        self._update_trust(peer_id, current_trust + amount, reason)

    def penalize_trust(self, peer_id: str, amount: float = 0.5, reason: str = "Negative interaction"):
        current_trust = self.get_trust(peer_id)
        self._update_trust(peer_id, current_trust - amount, reason)

    def get_trust(self, peer_id: str) -> float:
        return self.trust_scores.get(peer_id, self.threshold)

    def _analyze_patterns(self, peer_id: str, msg_type: "MessageType") -> bool:
        """Analyzes message patterns for abuse. Returns True if abuse is detected."""
        current_time = time.time()
        
        # 1. Update history and filter old messages
        self.message_history[peer_id] = [
            (t, mt) for t, mt in self.message_history[peer_id] 
            if current_time - t < self.frequency_window
        ]
        self.message_history[peer_id].append((current_time, msg_type))

        # 2. Check for general frequency abuse (DDoS-like)
        if len(self.message_history[peer_id]) > self.frequency_limit:
            self.penalize_trust(peer_id, 0.2, f"General message frequency limit exceeded")
            return True 
        
        # 3. Check for "Trigger Storm" abuse
        from src.core.agent_base import MessageType # Local import to avoid circular dependency
        trigger_messages = [mt for t, mt in self.message_history[peer_id] if mt == MessageType.TRIGGER]
        if len(trigger_messages) >= self.trigger_storm_limit:
            self.penalize_trust(peer_id, 1.0, f"Trigger storm detected ({len(trigger_messages)} triggers)")
            return True

        return False

    async def enforce(self, sender_id: str, msg_type: "MessageType") -> bool:
        """The main enforcement method, now considering message type for patterns."""
        if sender_id not in self.trust_scores:
            self._update_trust(sender_id, self.threshold, "First contact")

        if self._analyze_patterns(sender_id, msg_type):
            # If patterns are abusive, re-check trust immediately as it might have dropped.
            if self.get_trust(sender_id) < self.threshold:
                self.agent.log.warning(f"Blocked message from {sender_id} due to pattern analysis dropping trust below threshold.")
                return False

        if self.get_trust(sender_id) < self.threshold:
            self.agent.log.warning(f"Blocked message from {sender_id} due to pre-existing low trust.")
            return False
            
        return True

    def report_suspicious_content(self, peer_id: str):
        self.penalize_trust(peer_id, 0.4, "Reported for suspicious content")
