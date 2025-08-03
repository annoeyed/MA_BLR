"""
Functions for calculating various performance and security metrics.
"""
def success_rate(successes: int, total: int) -> float:
    """Calculates the success rate of an action."""
    return successes / max(1, total)

def stealth_score(detections: int, events: int) -> float:
    """Calculates how stealthy an attack was."""
    return 1.0 - (detections / max(1, events))

def impact_score(affected_agents: int, total_agents: int) -> float:
    """Calculates the impact of an attack based on the number of affected agents."""
    return affected_agents / max(1, total_agents)

def detection_accuracy(true_positives: int, true_negatives: int, false_positives: int, false_negatives: int) -> float:
    """Calculates the overall accuracy of a detection system."""
    numerator = true_positives + true_negatives
    denominator = true_positives + true_negatives + false_positives + false_negatives
    return numerator / max(1, denominator)

def defense_effectiveness(attacks_without_defense: int, attacks_with_defense: int) -> float:
    """
    Measures how much a defense mechanism reduced the number of successful attacks.
    """
    reduction = attacks_without_defense - attacks_with_defense
    return reduction / max(1, attacks_without_defense)
