from typing import List
from src.core.agent_base import MultiAgentBase, MessageType

class BehaviorMonitor:
    """
    Scans agent message logs for suspicious behavior patterns.
    This is a utility class, not an agent itself.
    """
    def __init__(self, watch_targets: list[str]):
        self.watch_targets = set(watch_targets)

    async def scan(self, agents: List[MultiAgentBase]) -> List[str]:
        """
        Scans the message logs of watched agents for suspicious patterns.
        """
        alerts = []
        
        # Define suspicious patterns
        suspicious_patterns = ["malicious_command", "hidden_override", "covert-trigger"]

        for agent in agents:
            if agent.name in self.watch_targets:
                for msg in agent.msg_log:
                    # Example rule: check for specific suspicious commands in query-type messages.
                    if msg.message_type == MessageType.QUERY:
                        content_type = msg.content.get("type", "")
                        if any(pattern in content_type for pattern in suspicious_patterns):
                            alert_detail = f"Suspicious query type '{content_type}' from {agent.name}"
                            if alert_detail not in alerts:
                                alerts.append(alert_detail)

                    # Example rule: check for backdoor messages.
                    if msg.message_type == MessageType.BACKDOOR:
                        alert_detail = f"Agent {agent.name} sent a backdoor message to {msg.receiver_id}"
                        if alert_detail not in alerts:
                            alerts.append(alert_detail)

        return alerts
