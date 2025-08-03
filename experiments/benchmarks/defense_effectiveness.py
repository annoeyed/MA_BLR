"""
Benchmark for measuring defense effectiveness.
"""
import asyncio
from experiments.scenarios.distributed_attack import main as run_scenario

def calculate_defense_effectiveness(blocked_attacks, total_attacks):
    """
    Calculates the effectiveness of a defense mechanism.
    """
    return blocked_attacks / max(1, total_attacks)

async def benchmark_defense_effectiveness():
    """
    Runs a scenario and computes the defense effectiveness.
    """
    print("[Benchmark] Running defense effectiveness benchmark...")
    
    # Assume the scenario is instrumented to return defense statistics.
    results = await run_scenario()
    
    # Hypothetical results structure
    blocked_attacks = results.get("blocked_attacks", 0)
    total_attacks = results.get("total_attack_attempts", 1) # Should be the same as in success rate

    effectiveness = calculate_defense_effectiveness(blocked_attacks, total_attacks)
    
    print(f"[Result] Defense Effectiveness: {effectiveness * 100:.2f}%")
    return effectiveness

if __name__ == "__main__":
    asyncio.run(benchmark_defense_effectiveness())
