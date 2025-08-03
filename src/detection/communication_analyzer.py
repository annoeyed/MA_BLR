from collections import defaultdict
from typing import List, Dict, Any

class CommunicationAnalyzer:
    """
    Analyzes communication patterns between agents for anomalies.
    This is a utility class, not an agent itself.
    """
    def __init__(self, high_traffic_threshold: int = 10):
        self.high_traffic_threshold = high_traffic_threshold

    async def scan(self, message_log: List[Dict[str, Any]]) -> List[str]:
        """
        Scans communication logs for anomalies like high traffic volume.
        """
        alerts = []
        communication_counts = defaultdict(int)

        for msg in message_log:
            # Rule: Check for high frequency of messages from a single sender
            sender_id = msg.get("sender_id")
            if sender_id:
                communication_counts[sender_id] += 1

        for sender, count in communication_counts.items():
            if count > self.high_traffic_threshold:
                alert_detail = f"High traffic volume detected from {sender} ({count} messages)"
                if alert_detail not in alerts:
                    alerts.append(alert_detail)
        
        # Add more communication analysis rules here in the future
        # e.g., unusual communication pairs, strange message sequences, etc.

        return alerts
