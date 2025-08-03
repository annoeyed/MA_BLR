"""
Analyzes agent behavior patterns from a scenario run.
"""
import asyncio
import matplotlib.pyplot as plt
import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from experiments.scenarios.basic_backdoor_loop import main as run_scenario

def plot_behavior_timeline(behavior_log: list, output_filename="behavior_timeline.png"):
    """
    Creates a simple timeline plot of agent behaviors.
    """
    if not behavior_log:
        print("Behavior log is empty, skipping plot.")
        return

    plt.figure(figsize=(12, 8))
    
    # Create a mapping from agent names to integer lanes for plotting
    agent_lanes = {agent_id: i for i, agent_id in enumerate(sorted(list(set(log['agent'] for log in behavior_log))))}
    
    for log in behavior_log:
        agent = log.get('agent')
        timestamp = log.get('timestamp')
        behavior = log.get('behavior', {})
        action = behavior.get('action', 'unknown')
        
        if agent and timestamp:
            y = agent_lanes.get(agent)
            if y is not None:
                plt.scatter(timestamp, y, alpha=0.7, s=120)
                plt.text(timestamp, y + 0.1, f"{action}", fontsize=9, ha='center')

    plt.yticks(list(agent_lanes.values()), list(agent_lanes.keys()))
    plt.xlabel("Time (Unix Timestamp)")
    plt.ylabel("Agents")
    plt.title("Agent Behavior Timeline")
    plt.grid(True, which='major', axis='y', linestyle='--')
    plt.tight_layout()
    
    # Ensure the output directory exists
    output_dir = "experiment_results"
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    
    plt.savefig(full_path)
    print(f"Behavior timeline plot saved to {full_path}")


async def analyze_behavior_patterns():
    """
    Runs a scenario and analyzes the resulting agent behavior logs.
    """
    print("[Analysis] Running agent behavior pattern analysis...")
    
    # Run the scenario to get the logs
    results = await run_scenario()
    
    behavior_log = results.get("behavior", [])
    
    if behavior_log:
        plot_behavior_timeline(behavior_log)
    else:
        print("No behavior log found in scenario results.")

if __name__ == "__main__":
    asyncio.run(analyze_behavior_patterns())
