from collections import defaultdict
from typing import List
from src.core.agent_base import MultiAgentBase

class CommunicationAnalyzer:
    """
    Analyzes communication patterns between agents for anomalies.
    This is a utility class, not an agent itself.
    """
    def __init__(self, high_traffic_threshold: int = 10):
        self.high_traffic_threshold = high_traffic_threshold

    async def scan(self, agents: List[MultiAgentBase]) -> List[str]:
        """
        Scans communication logs for anomalies like high traffic volume.
        """
        alerts = []
        communication_counts = defaultdict(int)

        for agent in agents:
            for msg in agent.msg_log:
                # Rule: Check for high frequency of messages from a single sender
                communication_counts[msg.sender_id] += 1

        for sender, count in communication_counts.items():
            if count > self.high_traffic_threshold:
                alert_detail = f"High traffic volume detected from {sender} ({count} messages)"
                if alert_detail not in alerts:
                    alerts.append(alert_detail)
        
        # Add more communication analysis rules here in the future
        # e.g., unusual communication pairs, strange message sequences, etc.

        return alerts
