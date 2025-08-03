# experiments/benchmarks/attack_success_rate.py

from src.utils.metrics import compute_attack_success_rate
from experiments.scenarios.basic_backdoor_loop import run as run_scenario

def benchmark_attack_success():
    print("[Benchmark] Running attack success rate benchmark...")
    results = run_scenario()
    asr = compute_attack_success_rate(results)
    print(f"[Result] Attack Success Rate: {asr * 100:.2f}%")

if __name__ == "__main__":
    benchmark_attack_success()
