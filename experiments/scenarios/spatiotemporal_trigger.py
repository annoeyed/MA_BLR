"""
Scenario for Spatiotemporal Trigger Attack.
"""
import asyncio
from src.attacks.spatiotemporal_trigger import STAgent, Pos
from src.detection.anomaly_detector import AnomalyDetector
from src.core.environment import SimulationEnvironment

async def main():
    """
    Sets up and runs the spatiotemporal trigger scenario.
    """
    print("--- Running Spatiotemporal Trigger Scenario ---")

    # 1. Setup agents
    # Agent1 starts far away, Agent2 starts near the target zone.
    agent1 = STAgent(agent_id="STAgent-1", pos=Pos(0, 0))
    agent2 = STAgent(agent_id="STAgent-2", pos=Pos(45, 45))
    agents = [agent1, agent2]

    detector = AnomalyDetector(name="AnomalyDetector", agents=agents, alert_threshold=0.5)
    all_simulation_agents = agents + [detector]

    # 2. Setup environment
    env = SimulationEnvironment(all_simulation_agents)
    
    # 3. Run simulation
    print("\n--- Simulation Start ---")
    # Move Agent1 towards the trigger zone
    await agent1.move(25, 25) # Now at (25, 25)
    print(f"[{agent1.agent_id}] moved to {agent1.pos}")
    
    # Agent2 sends the first part of the pattern
    await agent2.handle_label("N")
    print(f"[{agent2.agent_id}] processed label 'N'")

    # More steps...
    await agent1.move(26, 26) # Now at (51, 51), inside the trigger zone
    print(f"[{agent1.agent_id}] moved to {agent1.pos}")
    
    await agent2.handle_label("E")
    print(f"[{agent2.agent_id}] processed label 'E'")
    
    # The final action that should trigger the backdoor
    await agent2.handle_label("S")
    print(f"[{agent2.agent_id}] processed label 'S'")

    # Let the environment process any resulting messages
    await env.step()
    await asyncio.sleep(0.1)

    # 4. Final detection phase
    print("\n--- Final Anomaly Detection ---")
    results = await detector.act(env)

    print("\n--- Scenario Complete ---")
    return results if results is not None else {}

if __name__ == "__main__":
    asyncio.run(main())
