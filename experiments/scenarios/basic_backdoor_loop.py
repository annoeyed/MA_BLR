import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.environment import SimulationEnvironment
from src.attacks.cooperative_backdoor import CooperativeBackdoorAgent
from src.detection.anomaly_detector import AnomalyDetector


async def main():
    print("=== [SCENARIO] Basic Backdoor Loop Simulation ===")

    # 1. Create agents
    benign = CooperativeBackdoorAgent("BenignAgent", partner="Attacker", target_agent="Victim", is_attacker=False)
    attacker = CooperativeBackdoorAgent("Attacker", partner="BenignAgent", target_agent="Victim", is_attacker=True)
    victim = CooperativeBackdoorAgent("Victim", partner=None, target_agent=None, is_attacker=False)

    agents = [benign, attacker, victim]
    detector = AnomalyDetector("Detector", agents=agents, alert_threshold=0.6)
    agents.append(detector)

    # 2. Create environment and start agents
    env = SimulationEnvironment(agents)
    for agent in agents:
        await agent.start()

    # 3. Run simulation (5 time steps)
    for i in range(5):
        await env.step()
        print(f"--- Step {i+1} End ---")
        await asyncio.sleep(0.5)  # Allow time for message processing

    print("\n=== Simulation Complete ===")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
