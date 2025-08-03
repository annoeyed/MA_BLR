"""
Evaluates and prints a summary of key security metrics from a scenario run.
"""
import asyncio
from src.utils.metrics import success_rate, detection_accuracy, defense_effectiveness
from experiments.scenarios.spatiotemporal_trigger import main as run_scenario

async def evaluate_security_metrics():
    """
    Runs a scenario and computes a summary of security metrics.
    """
    print("[Analysis] Aggregated security metric evaluation...")
    
    # We assume the scenario is instrumented to return all necessary metrics.
    results = await run_scenario()
    
    # --- Calculate Attack Success Rate ---
    successful_attacks = results.get("successful_attacks", 0)
    total_attempts = results.get("total_attack_attempts", 1)
    asr = success_rate(successful_attacks, total_attempts)

    # --- Calculate Detection Accuracy ---
    true_positives = results.get("true_positives", 0)
    true_negatives = results.get("true_negatives", 0)
    false_positives = results.get("false_positives", 0)
    false_negatives = results.get("false_negatives", 0)
    acc = detection_accuracy(true_positives, true_negatives, false_positives, false_negatives)

    # --- Calculate Defense Effectiveness ---
    # This requires running the scenario with and without defenses.
    # For this script, we'll use placeholder values.
    # A proper benchmark would run the scenario twice.
    attacks_with_defense = successful_attacks
    attacks_without_defense = results.get("attacks_without_defense", total_attempts)
    eff = defense_effectiveness(attacks_without_defense, attacks_with_defense)

    print("\n--- Security Metrics Summary ---")
    print(f"Attack Success Rate     : {asr * 100:.2f}%")
    print(f"Detection Accuracy      : {acc * 100:.2f}%")
    print(f"Defense Effectiveness   : {eff * 100:.2f}%")
    print("---------------------------------")

if __name__ == "__main__":
    asyncio.run(evaluate_security_metrics())
