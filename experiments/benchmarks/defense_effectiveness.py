# experiments/benchmarks/defense_effectiveness.py

from src.utils.metrics import compute_defense_effectiveness
from experiments.scenarios.distributed_attack import run as run_scenario

def benchmark_defense():
    print("[Benchmark] Running defense effectiveness benchmark...")
    results = run_scenario()
    effectiveness = compute_defense_effectiveness(results)
    print(f"[Result] Defense Effectiveness: {effectiveness * 100:.2f}%")

if __name__ == "__main__":
    benchmark_defense()
