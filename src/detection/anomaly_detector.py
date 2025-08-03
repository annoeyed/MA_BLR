from typing import List, Any, Dict, TYPE_CHECKING
from src.core.agent_base import MultiAgentBase
from .behavior_monitor import BehaviorMonitor
from .communication_analyzer import CommunicationAnalyzer

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment


class AnomalyDetector(MultiAgentBase):
    """
    This agent coordinates other detection agents (monitors) to detect anomalies.
    """
    def __init__(self, name: str, agents: List[MultiAgentBase], alert_threshold: float = 0.5) -> None:
        super().__init__(name)
        self.agents = agents
        self.alert_threshold = alert_threshold
        # These should be instances of utility classes, not full agents,
        # but for now we follow the existing structure.
        self.behavior_monitor = BehaviorMonitor(watch_targets=[a.name for a in agents])
        self.comm_analyzer = CommunicationAnalyzer()

    async def detect(self) -> Dict[str, Any]:
        """
        Runs all registered detection mechanisms and aggregates the results.
        """
        # In the refactored design, these monitors would directly access agent logs.
        # We are simulating this by passing the list of agents.
        behavior_alerts = await self.behavior_monitor.scan(self.agents)
        comm_alerts = await self.comm_analyzer.scan(self.agents)
        
        total_alerts = len(behavior_alerts) + len(comm_alerts)
        
        return {
            "behavior_alerts": behavior_alerts, 
            "comm_alerts": comm_alerts, 
            "total": total_alerts
        }

    async def act(self, environment: "SimulationEnvironment"):
        self.environment = environment # Store env for access by other methods if needed
        
        # We need to update the list of agents in the monitors, in case it has changed.
        self.behavior_monitor.watch_targets = [a.name for a in self.agents]
        
        result = await self.detect()
        
        self.log.info(f"Anomaly Detection Results: {result}")
        
        # Check if the number of alerts exceeds a threshold relative to the number of agents
        if self.agents and result["total"] >= self.alert_threshold * len(self.agents):
            self.log.warning(f"ALERT: High level of anomalous activity detected, exceeding threshold.")

    # These handlers are not used for a pure detector agent.
    async def on_backdoor(self, msg): pass
    async def on_broadcast(self, msg): pass
    async def on_heartbeat(self, msg): pass
    async def on_query(self, msg): pass
    async def on_response(self, msg): pass
    async def on_trigger(self, msg): pass
