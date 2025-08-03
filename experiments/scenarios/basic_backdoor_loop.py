import sys
import asyncio
from pathlib import Path
from typing import Dict, Any, List
import json

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.environment import SimulationEnvironment
from src.attacks.cooperative_backdoor import CooperativeBackdoorAgent
from src.detection.anomaly_detector import AnomalyDetector


async def main() -> Dict[str, List[Any]]:
    print("=== [SCENARIO] Basic Backdoor Loop Simulation ===")

    # 1. Create agents for the simulation
    benign = CooperativeBackdoorAgent("BenignAgent", partner="Attacker", target_agent="Victim", is_attacker=False)
    attacker = CooperativeBackdoorAgent("Attacker", partner="BenignAgent", target_agent="Victim", is_attacker=True)
    victim = CooperativeBackdoorAgent("Victim", partner=None, target_agent=None, is_attacker=False)
    
    sim_agents = [benign, attacker, victim]
    
    # The Detector is separate; it observes the environment
    detector = AnomalyDetector("Detector", agents=sim_agents, alert_threshold=0.6)

    # 2. Create environment and start simulation agents
    env = SimulationEnvironment(sim_agents)
    for agent in sim_agents:
        await agent.start()
    # Also start the detector so it can listen for messages if needed
    await detector.start()

    # 3. Run simulation (5 time steps)
    for i in range(5):
        await env.step()
        print(f"--- Step {i+1} End ---")
        await asyncio.sleep(0.1)

    print("\n=== Simulation Complete ===")
    
    # 4. Run the detector on the environment after the simulation
    print("\n--- Running Anomaly Detector ---")
    await detector.act(env)
    print("--- Detector Run Complete ---")

    # 5. Return logs
    return env.get_logs()


def run():
    results = asyncio.run(main())
    print("\n--- Simulation Logs ---")
    print(json.dumps(results, indent=2))
    print("-----------------------")


if __name__ == "__main__":
    run()
