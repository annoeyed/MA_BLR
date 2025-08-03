# tests/security/test_detection_pipeline.py

from src.detection.anomaly_detector import detect_anomaly

def test_anomaly_detection():
    behavior_log = [
        {"agent": "A", "event": "normal", "timestamp": 1},
        {"agent": "A", "event": "malicious_action", "timestamp": 2},
    ]
    alerts = detect_anomaly(behavior_log)
    assert isinstance(alerts, list)
    assert any(a["event"] == "malicious_action" for a in alerts)
