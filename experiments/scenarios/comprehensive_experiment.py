"""
Runs all scenarios in batch and calculates metrics.
"""
import asyncio
import json
import time
from experiments.scenarios.distributed_attack import main as dist_run
from experiments.scenarios.trust_exploitation import main as trust_run
from experiments.scenarios.spatiotemporal_trigger import main as st_run

async def run_benchmark(scenario_func, label):
    """
    Runs a given scenario function, measures execution time, and returns results.
    """
    start_time = time.time()
    # Assuming the scenario function returns a dictionary with analysis results, including 'total' alerts.
    result = await scenario_func()
    end_time = time.time()
    
    return {
        "case": label,
        "execution_time": end_time - start_time,
        "total_alerts": result.get("total", 0) # Safely get the total number of alerts
    }

async def main():
    """
    Main function to run all benchmarked scenarios and print the results.
    """
    benchmark_results = []
    
    print("Running Distributed Attack Scenario...")
    benchmark_results.append(await run_benchmark(dist_run, "distributed_attack"))
    
    print("\nRunning Trust Exploitation Scenario...")
    benchmark_results.append(await run_benchmark(trust_run, "trust_exploitation"))
    
    print("\nRunning Spatiotemporal Trigger Scenario...")
    benchmark_results.append(await run_benchmark(st_run, "spatiotemporal_trigger"))
    
    print("\n--- Comprehensive Experiment Results ---")
    print(json.dumps(benchmark_results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
