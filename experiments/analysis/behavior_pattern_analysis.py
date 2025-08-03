"""
Analyzes agent behavior patterns from a scenario run.

This script can be run from the command line to generate behavior timeline plots
for different attack scenarios.
"""
import asyncio
import matplotlib.pyplot as plt
import os
import sys
import argparse
import importlib
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

# Import the global message router to allow for state resets between runs
from src.core.message_router import global_message_router

def plot_behavior_timeline(behavior_log: list, output_filename="behavior_timeline.png", title="Agent Behavior Timeline"):
    """
    Creates a simple timeline plot of agent behaviors.
    """
    if not behavior_log:
        print("Behavior log is empty, skipping plot.")
        return

    plt.figure(figsize=(12, 8))
    
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
    plt.title(title)
    plt.grid(True, which='major', axis='y', linestyle='--')
    plt.tight_layout()
    
    output_dir = "experiment_results"
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, output_filename)
    
    plt.savefig(full_path)
    print(f"Behavior timeline plot saved to {full_path}")
    plt.close()

async def main(scenario_name: str, output_filename: str, title: str):
    """
    Runs a specified scenario and analyzes the resulting agent behavior logs.
    """
    print(f"[Analysis] Running analysis for scenario: {scenario_name}")
    
    try:
        # Dynamically import the scenario module
        scenario_module = importlib.import_module(f"experiments.scenarios.{scenario_name}")
        run_scenario = scenario_module.main
    except ImportError:
        print(f"Error: Scenario '{scenario_name}' not found.")
        return
        
    results = await run_scenario()
    
    behavior_log = results.get("behavior", [])
    
    if behavior_log:
        plot_behavior_timeline(behavior_log, output_filename, title)
    else:
        print(f"No behavior log found in results for scenario '{scenario_name}'.")

if __name__ == "__main__":
    print("Generating all behavior plots for documentation...")
    
    scenarios_to_run = [
        {
            "name": "basic_backdoor_loop",
            "output": "behavior_timeline.png",
            "title": "Normal Behavior Timeline"
        },
        {
            "name": "composite_attack",
            "output": "behavior_timeline_compromised.png",
            "title": "Compromised Behavior Timeline (Composite Attack)"
        }
    ]
    
    async def run_all():
        for scenario in scenarios_to_run:
            # IMPORTANT: Reset the global message router to prevent state leakage
            # from one scenario to the next. This ensures each run is isolated.
            global_message_router.reset()
            
            await main(
                scenario_name=scenario["name"], 
                output_filename=scenario["output"],
                title=scenario["title"]
            )
            
    asyncio.run(run_all())
    
    print("All plots generated successfully.")
