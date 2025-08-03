"""
Benchmark for measuring detection accuracy.
"""
import asyncio
from experiments.scenarios.trust_exploitation import main as run_scenario

def calculate_accuracy(true_positives, true_negatives, false_positives, false_negatives):
    """
    Calculates detection accuracy.
    """
    numerator = true_positives + true_negatives
    denominator = true_positives + true_negatives + false_positives + false_negatives
    return numerator / max(1, denominator)

async def benchmark_detection_accuracy():
    """
    Runs a scenario and computes the detection accuracy.
    """
    print("[Benchmark] Running detection accuracy benchmark...")
    
    # We assume the scenario is instrumented to return detection statistics.
    # This is a placeholder for what the scenario should return.
    results = await run_scenario()
    
    # Hypothetical results structure
    true_positives = results.get("true_positives", 0)
    true_negatives = results.get("true_negatives", 0)
    false_positives = results.get("false_positives", 0)
    false_negatives = results.get("false_negatives", 0)

    accuracy = calculate_accuracy(true_positives, true_negatives, false_positives, false_negatives)
    
    print(f"[Result] Detection Accuracy: {accuracy * 100:.2f}%")
    return accuracy

if __name__ == "__main__":
    asyncio.run(benchmark_detection_accuracy())
