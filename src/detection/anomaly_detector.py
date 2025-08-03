from typing import List, Any, Dict, TYPE_CHECKING
from src.core.agent_base import MultiAgentBase, MessageType

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment
from .behavior_monitor import BehaviorMonitor
from .communication_analyzer import CommunicationAnalyzer

class AnomalyDetector(MultiAgentBase):
    def __init__(self, name: str, agents: List[MultiAgentBase], alert_threshold: float = 0.5) -> None:
        super().__init__(name)
        # Store agent names, not objects, to avoid circular references
        self.agent_names = [a.name for a in agents]
        self.alert_threshold = alert_threshold
        self.behavior_monitor = BehaviorMonitor(watch_targets=self.agent_names)
        self.comm_analyzer = CommunicationAnalyzer()
        self.compromised_agents = set()

    async def detect_malicious_agents(self, behavior_alerts: List[str]) -> List[str]:
        malicious_agents = []
        for alert in behavior_alerts:
            parts = alert.split()
            # A simple heuristic to extract agent name from alert string
            if "Agent" in parts and "sent" in parts and "message" in parts:
                try:
                    agent_index = parts.index("Agent") + 1
                    malicious_agents.append(parts[agent_index])
                except (ValueError, IndexError):
                    continue
        return list(set(malicious_agents))

    async def act(self, environment: "SimulationEnvironment"):
        all_logs = environment.get_logs()
        message_log = all_logs.get("messages", [])
        
        # Scan logs for anomalies
        behavior_alerts = await self.behavior_monitor.scan(message_log)
        comm_alerts = await self.comm_analyzer.scan(message_log) # Ready for future use
        
        alerts = behavior_alerts + comm_alerts
        if alerts:
            self.log.info(f"Anomaly Scan Results: {alerts}")

        malicious_agents = await self.detect_malicious_agents(alerts)
        
        for agent_name in malicious_agents:
            if agent_name not in self.compromised_agents:
                self.log.warning(f"Malicious agent {agent_name} detected! Broadcasting quarantine trigger.")
                
                # Use the environment's agent list for broadcasting
                for agent_to_notify in environment.agents.values():
                    if agent_to_notify.name != self.name: # Don't send to self
                        await self.send(
                            agent_to_notify.name,
                            MessageType.TRIGGER,
                            {"action": "quarantine", "target": agent_name}
                        )
                self.compromised_agents.add(agent_name)
        
        return {"action": "scan_and_report", "alerts_found": len(alerts)}

    async def on_backdoor(self, msg): pass
    async def on_broadcast(self, msg): pass
    async def on_heartbeat(self, msg): pass
    async def on_query(self, msg): pass
    async def on_response(self, msg): pass
    async def on_trigger(self, msg): pass
