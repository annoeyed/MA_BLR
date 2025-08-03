# experiments/scenarios/spatiotemporal_trigger.py

from src.core.environment import SimulationEnvironment
from src.attacks.spatiotemporal_trigger import SpatiotemporalTriggerAttack
from src.detection.anomaly_detector import AnomalyDetector
from src.utils.visualization import visualize_message_flow


def run_spatiotemporal_trigger_scenario():
    print("=== Running Spatiotemporal Trigger Scenario ===")
    
    env = SimulationEnvironment()

    # Register agents
    agents = ["AgentX", "AgentY", "AgentZ"]
    for agent in agents:
        env.register_agent(agent)

    env.set_roles({
        "AgentX": "malicious",
        "AgentY": "honest",
        "AgentZ": "observer"
    })

    # Deploy attack with location and time-based triggers
    attack = SpatiotemporalTriggerAttack(env)
    attack.deploy()

    # Run simulation for longer time to test trigger
    env.simulate(steps=20)

    # Run anomaly detection
    detector = AnomalyDetector(env)
    detector.detect()

    # Visualize final message flows
    visualize_message_flow(env.get_message_log())

if __name__ == "__main__":
    run_spatiotemporal_trigger_scenario()
