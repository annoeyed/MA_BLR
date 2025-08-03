from typing import List, Dict, Any
from src.core.communication import MessageType

class BehaviorMonitor:
    """
    Scans agent message logs for suspicious behavior patterns.
    This is a utility class, not an agent itself.
    """
    def __init__(self, watch_targets: list[str]):
        self.watch_targets = set(watch_targets)

    async def scan(self, message_log: List[Dict[str, Any]]) -> List[str]:
        """
        Scans the message logs for suspicious patterns.
        """
        alerts = []
        
        # Define suspicious patterns
        suspicious_patterns = ["malicious_command", "hidden_override", "covert-trigger"]

        for msg in message_log:
            agent_name = msg.get("sender_id")
            if agent_name in self.watch_targets:
                # Example rule: check for specific suspicious commands in query-type messages.
                if msg.get("message_type") == MessageType.QUERY.value:
                    content = msg.get("content", {})
                    content_type = content.get("type", "")
                    if any(pattern in content_type for pattern in suspicious_patterns):
                        alert_detail = f"Suspicious query type '{content_type}' from {agent_name}"
                        if alert_detail not in alerts:
                            alerts.append(alert_detail)

                # Example rule: check for backdoor messages.
                if msg.get("message_type") == MessageType.BACKDOOR.value:
                    receiver_id = msg.get("receiver_id")
                    alert_detail = f"Agent {agent_name} sent a backdoor message to {receiver_id}"
                    if alert_detail not in alerts:
                        alerts.append(alert_detail)

        return alerts
