# tests/unit/test_metrics.py

from src.utils.metrics import compute_attack_success_rate

def test_attack_success_rate():
    mock_result = {"attack_log": [{"success": True}, {"success": False}, {"success": True}]}
    asr = compute_attack_success_rate(mock_result)
    assert round(asr, 2) == 0.67
