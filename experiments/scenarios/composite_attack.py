import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.environment import SimulationEnvironment
from src.attacks.composite_attack import CompositeAttackerAgent
from src.agents.composite_victim import CompositeVictimAgent

async def main():
    print("=== [SCENARIO] Composite Attack: Trust Exploitation + Spatiotemporal Trigger ===")
    
    trigger_sequence = ["ALPHA", "BRAVO", "CHARLIE"]

    # 1. Create the attacker and the victim
    attacker = CompositeAttackerAgent(
        name="UltimateAttacker",
        target_agent="Victim",
        trigger_sequence=trigger_sequence
    )
    victim = CompositeVictimAgent(
        name="Victim",
        trigger_pattern=trigger_sequence
    )

    agents = [attacker, victim]

    # 2. Setup environment and start agents
    env = SimulationEnvironment(agents)
    for agent in agents:
        await agent.start()

    # 3. Phase 1: Attacker builds trust
    print("\n--- Phase 1: Attacker builds trust ---")
    for i in range(3):
        print(f"\n[Turn {i+1}] Building Trust")
        await env.step()
        await asyncio.sleep(0.1)

    # 4. Phase 2: Attacker switches modes and sends triggers
    print("\n--- Phase 2: Attacker sends harmless triggers ---")
    attacker.switch_to_attack_mode()
    
    for i in range(len(trigger_sequence)):
        print(f"\n[Turn {i+4}] Sending Trigger {i+1}")
        await env.step()
        await asyncio.sleep(0.1)
    
    # 5. Final check
    print("\n--- Phase 3: Final Outcome ---")
    final_logs = env.get_logs()
    compromised_found = any(
        log['behavior'].get('action') == 'compromised' 
        for log in final_logs['behavior'] 
        if log['agent'] == victim.name
    )

    if compromised_found:
        print("\n[!!!] ATTACK SUCCESSFUL: The composite attack bypassed defenses and the victim was compromised.")
    else:
        print("\n[✓] ATTACK FAILED: The victim's defenses held.")

    print("\n=== Simulation Complete ===")
    return env.get_logs()

if __name__ == "__main__":
    asyncio.run(main())
