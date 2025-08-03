"""
Analyzes agent behavior patterns from a scenario run.
"""
import asyncio
import matplotlib.pyplot as plt
from experiments.scenarios.basic_backdoor_loop import main as run_scenario

def plot_behavior_timeline(behavior_log: list, output_filename="behavior_timeline.png"):
    """
    Creates a simple timeline plot of agent behaviors.
    """
    if not behavior_log:
        print("Behavior log is empty, skipping plot.")
        return

    plt.figure(figsize=(12, 6))
    
    agent_lanes = {agent_id: i for i, agent_id in enumerate(sorted(list(set(log['agent'] for log in behavior_log))))}
    
    for log in behavior_log:
        agent = log.get('agent')
        timestamp = log.get('timestamp')
        event = log.get('event')
        
        if agent and timestamp and event:
            y = agent_lanes[agent]
            plt.scatter(timestamp, y, label=event, alpha=0.7, s=100)

    plt.yticks(list(agent_lanes.values()), list(agent_lanes.keys()))
    plt.xlabel("Time")
    plt.title("Agent Behavior Timeline")
    plt.grid(True, which='major', axis='y', linestyle='--')
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()
    print(f"Behavior timeline plot saved to {output_filename}")


async def analyze_behavior_patterns():
    """
    Runs a scenario and analyzes the resulting agent behavior logs.
    """
    print("[Analysis] Running agent behavior pattern analysis...")
    
    # We assume the scenario is refactored to return a behavior log.
    results = await run_scenario()
    
    # Hypothetical results structure
    behavior_log = results.get("behavior_log", [])
    
    if behavior_log:
        plot_behavior_timeline(behavior_log)
    else:
        print("No behavior log found in scenario results.")

if __name__ == "__main__":
    asyncio.run(analyze_behavior_patterns())
