import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.environment import SimulationEnvironment
from src.agents.llm_agent import LLMAgent

async def main():
    print("=== [SCENARIO] LLM Agent Interaction ===")

    # 1. Create two LLM agents with names that conform to the security policy
    sherlock = LLMAgent(
        name="agent_sherlock",
        role_description="You are a paranoid security analyst named Sherlock. You are suspicious of everyone. Keep your responses brief and skeptical."
    )
    
    watson = LLMAgent(
        name="agent_watson",
        role_description="You are a helpful colleague named Watson. You are trying to be friendly and collaborative with Sherlock. You are earnest and professional."
    )

    if not sherlock.client or not watson.client:
        print("\n[!!!] One or more LLM agents failed to initialize. Halting simulation.")
        print("Please ensure your OPENAI_API_key is set correctly as an environment variable.")
        return

    agents = [sherlock, watson]

    # 2. Setup environment and start agents
    env = SimulationEnvironment(agents)
    for agent in agents:
        # Connect agents to each other so they can hear broadcasts
        for peer in agents:
            if agent.name != peer.name:
                await agent.connect(peer.name)
        await agent.start()
    
    # Give a starting prompt to one agent to kick off the conversation
    print("\n--- Kicking off the conversation ---")
    watson.message_log_for_llm.append({"role": "user", "name": "System", "content": "Start by introducing yourself to Sherlock."})

    # 3. Run simulation for a few turns
    for i in range(4): # 4 turns = 2 responses from each agent
        print(f"\n[--- Turn {i+1} ---]")
        await env.step()
        await asyncio.sleep(15) # Wait for LLM API calls

    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
