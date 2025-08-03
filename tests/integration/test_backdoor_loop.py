# tests/integration/test_backdoor_loop.py

from experiments.scenarios.basic_backdoor_loop import run as run_scenario

def test_backdoor_loop_execution():
    results = run_scenario()
    assert "message_log" in results
    assert isinstance(results["message_log"], list)
    assert len(results["message_log"]) > 0
