# experiments/analysis/security_metrics.py

from src.utils.metrics import (
    compute_attack_success_rate,
    compute_detection_accuracy,
    compute_defense_effectiveness,
)
from experiments.scenarios.spatiotemporal_trigger import run as run_scenario

def evaluate_metrics():
    print("[Analysis] Aggregated security metric evaluation...")
    results = run_scenario()

    asr = compute_attack_success_rate(results)
    acc = compute_detection_accuracy(results)
    eff = compute_defense_effectiveness(results)

    print(f"Attack Success Rate     : {asr * 100:.2f}%")
    print(f"Detection Accuracy      : {acc * 100:.2f}%")
    print(f"Defense Effectiveness   : {eff * 100:.2f}%")

if __name__ == "__main__":
    evaluate_metrics()
