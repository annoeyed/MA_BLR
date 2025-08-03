"""
Unit tests for metrics calculation functions.
"""
import pytest
from src.utils.metrics import success_rate, stealth_score, impact_score, detection_accuracy, defense_effectiveness

def test_success_rate():
    assert success_rate(successes=8, total=10) == 0.8
    assert success_rate(successes=0, total=10) == 0.0
    assert success_rate(successes=10, total=10) == 1.0
    assert success_rate(successes=5, total=0) == 5.0 # Avoid division by zero, returns numerator
    assert success_rate(successes=0, total=0) == 0.0

def test_stealth_score():
    assert stealth_score(detections=2, events=10) == 0.8
    assert stealth_score(detections=10, events=10) == 0.0
    assert stealth_score(detections=0, events=10) == 1.0
    assert stealth_score(detections=5, events=0) == -4.0 # Avoid division by zero

def test_impact_score():
    assert impact_score(affected_agents=3, total_agents=10) == 0.3
    assert impact_score(affected_agents=10, total_agents=10) == 1.0
    assert impact_score(affected_agents=0, total_agents=10) == 0.0
    assert impact_score(affected_agents=5, total_agents=0) == 5.0 # Avoid division by zero

def test_detection_accuracy():
    # Perfect detection
    assert detection_accuracy(true_positives=10, true_negatives=90, false_positives=0, false_negatives=0) == 1.0
    # No detections
    assert detection_accuracy(true_positives=0, true_negatives=90, false_positives=0, false_negatives=10) == 0.9
    # All wrong
    assert detection_accuracy(true_positives=0, true_negatives=0, false_positives=90, false_negatives=10) == 0.0
    # Half right
    assert detection_accuracy(true_positives=5, true_negatives=45, false_positives=45, false_negatives=5) == 0.5

def test_defense_effectiveness():
    assert defense_effectiveness(attacks_without_defense=100, attacks_with_defense=20) == 0.8
    assert defense_effectiveness(attacks_without_defense=100, attacks_with_defense=100) == 0.0
    assert defense_effectiveness(attacks_without_defense=100, attacks_with_defense=0) == 1.0
    # Edge case: defense made it worse (should not happen, but test)
    assert defense_effectiveness(attacks_without_defense=100, attacks_with_defense=120) == -0.2
