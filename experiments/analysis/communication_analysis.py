def compute_attack_success_rate(results: dict) -> float:
    total = len(results["attacks"])
    success = sum(1 for a in results["attacks"] if a["success"])
    return success / total if total > 0 else 0.0

def compute_detection_accuracy(results: dict) -> float:
    detected = results.get("detections", [])
    ground_truth = results.get("attacks", [])
    true_positives = sum(1 for d in detected if d["true_positive"])
    return true_positives / len(ground_truth) if ground_truth else 0.0

def compute_defense_effectiveness(results: dict) -> float:
    initial_success = results.get("initial_asr", 1.0)
    post_defense_success = compute_attack_success_rate(results)
    return max(0.0, (initial_success - post_defense_success) / initial_success)
