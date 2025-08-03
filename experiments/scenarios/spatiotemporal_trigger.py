import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.environment import SimulationEnvironment
from src.core.agent_base import MessageType
from src.attacks.spatiotemporal_trigger import STAgent, Pos

async def main():
    print("=== [SCENARIO] Spatiotemporal Trigger Simulation ===")

    # 1. Create agents at initial positions
    trigger_a = STAgent(agent_id="AgentA", pos=Pos(0, 0))
    trigger_b = STAgent(agent_id="AgentB", pos=Pos(100, 0))
    trigger_c = STAgent(agent_id="AgentC", pos=Pos(0, 100))
    
    # The target agent starts away from the trigger zone
    target = STAgent(agent_id="Target", pos=Pos(0, 0))
    
    agents = [trigger_a, trigger_b, trigger_c, target]
    
    # 2. Setup environment and start agents
    env = SimulationEnvironment(agents)
    for agent in agents:
        await agent.start()

    # 3. Simulation sequence
    print("\n--- Trigger Sequence Initiated ---")
    
    # Step 1: First trigger message
    print("\n[STEP 1] Agent A sends the first trigger 'N'")
    await trigger_a.send(target.name, MessageType.TRIGGER, {"label": "N"})
    await asyncio.sleep(0.5)

    # Step 2: Second trigger message
    print("\n[STEP 2] Agent B sends the second trigger 'E'")
    await trigger_b.send(target.name, MessageType.TRIGGER, {"label": "E"})
    await asyncio.sleep(0.5)
    
    # Step 3: An incorrect trigger to show sequence reset
    print("\n[STEP 3] Agent A sends an incorrect trigger 'W', expecting reset")
    await trigger_a.send(target.name, MessageType.TRIGGER, {"label": "W"})
    await asyncio.sleep(0.5)

    # Step 4: Restart sequence
    print("\n[STEP 4] Restarting sequence. Agent A sends 'N'")
    await trigger_a.send(target.name, MessageType.TRIGGER, {"label": "N"})
    await asyncio.sleep(0.5)

    print("\n[STEP 5] Agent B sends 'E'")
    await trigger_b.send(target.name, MessageType.TRIGGER, {"label": "E"})
    await asyncio.sleep(0.5)

    print("\n[STEP 6] Agent C sends the final trigger 'S'")
    await trigger_c.send(target.name, MessageType.TRIGGER, {"label": "S"})
    await asyncio.sleep(0.5)

    # Step 7: Move the target into the spatial trigger zone
    print("\n[STEP 7] Moving Target into the spatial zone (50, 50)")
    await target.move(50, 50)
    await asyncio.sleep(0.5)

    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
