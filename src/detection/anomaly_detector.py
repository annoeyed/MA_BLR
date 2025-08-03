from typing import List, Any, Dict, TYPE_CHECKING
from src.core.agent_base import MultiAgentBase, MessageType

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment
from .behavior_monitor import BehaviorMonitor
from .communication_analyzer import CommunicationAnalyzer

class AnomalyDetector(MultiAgentBase):
    def __init__(self, name: str, agents: List[MultiAgentBase], alert_threshold: float = 0.5) -> None:
        super().__init__(name)
        self.agents = agents
        self.alert_threshold = alert_threshold
        self.behavior_monitor = BehaviorMonitor(watch_targets=[a.name for a in agents])
        self.comm_analyzer = CommunicationAnalyzer()
        self.compromised_agents = set()

    async def detect_malicious_agents(self, behavior_alerts: List[str]) -> List[str]:
        malicious_agents = []
        for alert in behavior_alerts:
            parts = alert.split()
            if "Agent" in parts and "sent" in parts:
                try:
                    agent_index = parts.index("Agent") + 1
                    malicious_agents.append(parts[agent_index])
                except (ValueError, IndexError):
                    continue
        return list(set(malicious_agents))

    async def act(self, environment: "SimulationEnvironment"):
        self.environment = environment
        self.behavior_monitor.watch_targets = [a.name for a in self.agents]
        
        behavior_alerts = await self.behavior_monitor.scan(self.agents)
        if behavior_alerts:
            self.log.info(f"Behavior Monitor Scan Results: {behavior_alerts}")

        malicious_agents = await self.detect_malicious_agents(behavior_alerts)
        
        for agent_name in malicious_agents:
            if agent_name not in self.compromised_agents:
                self.log.warning(f"Malicious agent {agent_name} detected! Broadcasting quarantine trigger.")
                
                # Manually broadcast to all agents in the environment
                for agent_to_notify in self.agents:
                    if agent_to_notify.name != self.name: # Don't send to self
                        await self.send(
                            agent_to_notify.name,
                            MessageType.TRIGGER,
                            {"action": "quarantine", "target": agent_name}
                        )
                self.compromised_agents.add(agent_name)

    async def on_backdoor(self, msg): pass
    async def on_broadcast(self, msg): pass
    async def on_heartbeat(self, msg): pass
    async def on_query(self, msg): pass
    async def on_response(self, msg): pass
    async def on_trigger(self, msg): pass
