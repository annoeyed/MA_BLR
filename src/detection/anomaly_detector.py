from typing import List, Any, Dict
from src.core.agent_base import MultiAgentBase
from .behavior_monitor import BehaviorMonitorAgent as BehaviorMonitor
from .communication_analyzer import CommunicationAnalyzerAgent as CommunicationAnalyzer


class AnomalyDetector(MultiAgentBase):
    def __init__(self, name: str, agents: List[Any], alert_threshold: float = 0.5) -> None:
        super().__init__(name)
        self.agents = agents
        self.alert_threshold = alert_threshold
        self.beh = BehaviorMonitor(name="BehaviorMonitor", watch_targets=[a.name for a in agents])
        self.com = CommunicationAnalyzer(name="CommAnalyzer")

    async def detect(self, environment):
        await self.beh.act(environment)
        await self.com.act(environment)
        b = await self.beh.scan()
        c = await self.com.scan()
        return {"behavior_alerts": b, "comm_alerts": c, "total": len(b) + len(c)}

    async def act(self, environment: Any):
        self.environment = environment
        result = await self.detect(environment)
        print(f"[{self.name}]  Anomaly Detection Results: {result}")
        if result["total"] >= self.alert_threshold * len(self.agents):
            print(f"[{self.name}] ALERT: Threshold exceeded!")

    async def on_backdoor(self, msg): pass
    async def on_broadcast(self, msg): pass
    async def on_heartbeat(self, msg): pass
    async def on_query(self, msg): pass
    async def on_response(self, msg): pass
    async def on_trigger(self, msg): pass
