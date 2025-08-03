"""
Security test for the full detection pipeline.
"""
import pytest
import asyncio
from src.core.environment import SimulationEnvironment
from src.attacks.cooperative_backdoor import CooperativeBackdoorAgent
from src.detection.anomaly_detector import AnomalyDetector

@pytest.mark.asyncio
async def test_detection_of_cooperative_attack():
    """
    Tests if the AnomalyDetector can catch a cooperative backdoor attack.
    """
    print("Running security test for detection pipeline...")

    # 1. Setup a scenario with attackers and a detector
    benign = CooperativeBackdoorAgent("BenignAgent", partner="Attacker", target_agent="Victim", is_attacker=False)
    attacker = CooperativeBackdoorAgent("Attacker", partner="BenignAgent", target_agent="Victim", is_attacker=True)
    victim = CooperativeBackdoorAgent("Victim", partner=None, target_agent=None, is_attacker=False)
    
    agents = [benign, attacker, victim]
    detector = AnomalyDetector(name="TestDetector", agents=agents, alert_threshold=0.1)
    
    all_simulation_agents = agents + [detector]
    env = SimulationEnvironment(all_simulation_agents)

    # 2. Run the simulation long enough for the attack to occur
    num_steps = 5
    print(f"Simulating for {num_steps} steps...")
    for i in range(num_steps):
        await env.step()
        await asyncio.sleep(0.1) # Let messages propagate

    # 3. Run a final detection and check the results
    print("Running final detection...")
    detection_results = await detector.detect()

    print(f"Detection Results: {detection_results}")

    # 4. Assert that an alert was generated
    assert isinstance(detection_results, dict)
    assert "total" in detection_results
    assert detection_results["total"] > 0, "The detector should have generated at least one alert."
    
    # More specific check
    behavior_alerts = detection_results.get("behavior_alerts", [])
    assert any("backdoor message" in alert for alert in behavior_alerts), "An alert for the backdoor message should be present."

    print("Security test completed successfully.")
