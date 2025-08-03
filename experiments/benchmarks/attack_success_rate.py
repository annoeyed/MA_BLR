"""
Benchmark for measuring the attack success rate.
"""
import asyncio
from src.utils.metrics import success_rate
from experiments.scenarios.basic_backdoor_loop import main as run_scenario

async def benchmark_attack_success():
    """
    Runs a scenario and computes the attack success rate based on the results.
    """
    print("[Benchmark] Running attack success rate benchmark...")
    
    # The scenario needs to return metrics, including successful attacks and total attempts.
    # We assume `run_scenario` is refactored to return such a dictionary.
    # For now, we'll use placeholder values.
    
    # In a real implementation, the scenario itself would need to be instrumented
    # to track and return these numbers.
    # e.g., was a backdoor message successfully delivered and acted upon?
    
    # Placeholder results
    results = await run_scenario() # Assuming this now returns metrics
    
    # Let's define what success means. For this example, let's say a backdoor
    # message being logged by the victim agent is a success.
    # This requires inspecting the results from the simulation.
    # This part of the code is highly dependent on what `run_scenario` returns.
    
    # Let's assume a hypothetical structure for results for now.
    successful_attacks = results.get("successful_attacks", 0)
    total_attempts = results.get("total_attack_attempts", 1) # Avoid division by zero
    
    attack_rate = success_rate(successful_attacks, total_attempts)
    
    print(f"[Result] Attack Success Rate: {attack_rate * 100:.2f}%")
    return attack_rate

if __name__ == "__main__":
    asyncio.run(benchmark_attack_success())
