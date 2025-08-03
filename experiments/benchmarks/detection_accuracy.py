# experiments/benchmarks/detection_accuracy.py

from src.utils.metrics import compute_detection_accuracy
from experiments.scenarios.trust_exploitation import run as run_scenario

def benchmark_detection():
    print("[Benchmark] Running detection accuracy benchmark...")
    results = run_scenario()
    acc = compute_detection_accuracy(results)
    print(f"[Result] Detection Accuracy: {acc * 100:.2f}%")

if __name__ == "__main__":
    benchmark_detection()
