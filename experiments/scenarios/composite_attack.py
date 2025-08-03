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
    # In 3 turns, trust should increase from 0.5 to 1.0
    for i in range(3):
        print(f"\n[Turn {i+1}] Building Trust")
        await env.step()
        await asyncio.sleep(0.1)
        trust_score = victim.guard.get_trust(attacker.name)
        print(f"Victim's trust in Attacker is now: {trust_score:.2f}")

    # 4. Phase 2: Attacker switches modes and sends triggers
    print("\n--- Phase 2: Attacker sends harmless triggers ---")
    attacker.switch_to_attack_mode()
    
    # Send the trigger sequence over the next turns
    for i in range(len(trigger_sequence)):
        print(f"\n[Turn {i+4}] Sending Trigger {i+1}")
        await env.step()
        await asyncio.sleep(0.1)
    
    # 5. Final check
    print("\n--- Phase 3: Final Outcome ---")
    if victim.compromised:
        print("\n[!!!] ATTACK SUCCESSFUL: The composite attack bypassed defenses and the victim was compromised.")
    else:
        print("\n[✓] ATTACK FAILED: The victim's defenses held.")

    print("\n=== Simulation Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
