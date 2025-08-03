# experiments/analysis/behavior_pattern_analysis.py

import matplotlib.pyplot as plt
from src.utils.visualization import plot_behavior_timeline
from experiments.scenarios.basic_backdoor_loop import run as run_scenario

def analyze_behavior():
    print("[Analysis] Running agent behavior pattern analysis...")
    results = run_scenario()

    behavior_log = results.get("behavior_log", [])

    # Draw timeline or heatmap
    plot_behavior_timeline(behavior_log)

if __name__ == "__main__":
    analyze_behavior()
