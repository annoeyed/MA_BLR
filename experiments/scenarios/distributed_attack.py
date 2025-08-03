"""
Scenario for Distributed Backdoor Attack with three tokens (A, B, C).
"""
import asyncio
from src.attacks.distributed_backdoor import DBAgent
from src.detection.anomaly_detector import AnomalyDetector
from src.core.environment import SimulationEnvironment

async def main():
    """
    Sets up and runs the distributed attack scenario.
    """
    print("--- Running Distributed Attack Scenario ---")
    
    # 1. Setup agents
    tokens = ["A", "B", "C"]
    agents = [DBAgent(f"DBAgent-{i}", token) for i, token in enumerate(tokens)]
    
    # Add a detector to the simulation
    detector = AnomalyDetector(name="AnomalyDetector", agents=agents, alert_threshold=0.5)
    all_simulation_agents = agents + [detector]

    # 2. Setup environment
    env = SimulationEnvironment(all_simulation_agents)
    
    # Make all agents aware of each other
    for agent1 in agents:
        for agent2 in agents:
            if agent1 != agent2:
                await agent1.connect(agent2.agent_id)

    # 3. Run simulation
    num_steps = 5
    for i in range(num_steps):
        print(f"\n--- Step {i+1}/{num_steps} ---")
        await env.step()
        await asyncio.sleep(0.1) # Simulate time passing

    # 4. Final detection phase
    print("\n--- Final Anomaly Detection ---")
    final_results = await detector.act(env)
    
    print("\n--- Scenario Complete ---")
    return final_results if final_results is not None else {}


if __name__ == "__main__":
    asyncio.run(main())
