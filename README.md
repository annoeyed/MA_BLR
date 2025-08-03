# Multi-Agent Backdoor Loop (MA_BLR) Research

A research framework for simulating, detecting, and defending against backdoor loop attacks in LLM-based multi-agent systems.

---

## Overview

This project provides a comprehensive framework for in-depth analysis of "backdoor loops," an emerging attack vector threatening the integrity of multi-agent systems. A backdoor loop occurs when malicious triggers, embedded across multiple interacting agents, are activated to execute unintended actions, bypass system policies, or corrupt collaborative outcomes.

This framework supports the simulation and evaluation of sophisticated attack scenarios, including:

- **Cooperative Backdoor Injection:** Multiple agents collude to plant a distributed backdoor.
- **Spatiotemporal Trigger Activation:** Attack execution depends on complex triggers related to time, order, or state.
- **Trust Exploitation in Role Delegation:** An agent abuses trust relationships to execute a backdoor during delegated tasks.
- **Distributed Backdoor Activation:** A backdoor, fragmented across several agents, is activated by a single, coordinated event.

---

## Project Structure

```
MA_BLR/
├── src/                  # Core logic: agents, attacks, defenses, etc.
│   ├── agents/           # Base agent classes and role-specific implementations
│   ├── attacks/          # Backdoor attack simulation modules
│   └── defenses/         # Backdoor defense and detection pipelines
├── experiments/          # Scripts for scenarios, benchmarks, and analysis
│   ├── scenarios/        # Implementations of various attack/defense scenarios
│   ├── benchmarks/       # Performance evaluation benchmarks
│   └── analysis/         # Tools for analyzing experiment results
├── datasets/             # Sample logs, attack patterns, and benchmark data
├── tests/                # Unit, integration, and security tests
│   ├── unit/             # Tests for individual modules
│   ├── integration/      # Tests for module interactions
│   └── security/         # Security vulnerability and penetration tests
├── docs/                 # Project documentation (theoretical background, usage guides)
├── requirements.txt      # Python dependencies
└── README.md             # Project overview and instructions
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/annoeyed/MA_BLR.git
cd MA_BLR
```

### 2. Install dependencies

It is highly recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

If you encounter a `UnicodeDecodeError` on Windows, try specifying the encoding:

```bash
pip install -r requirements.txt --encoding utf-8
```

---

## Running Experiments

The `experiments/` directory contains scripts to run simulations, benchmarks, and analyses.

### Run a Basic Backdoor Loop Simulation

Executes a foundational backdoor loop attack scenario.

```bash
python experiments/scenarios/basic_backdoor_loop.py
```

### Run Benchmarks

Evaluate the framework against various metrics.

```bash
# Measure the success rate of different attacks
python experiments/benchmarks/attack_success_rate.py

# Evaluate the accuracy of detection modules
python experiments/benchmarks/detection_accuracy.py

# Assess the effectiveness of defense mechanisms
python experiments/benchmarks/defense_effectiveness.py
```

### Analyze Logs

Process simulation logs to extract insights.

```bash
# Analyze communication patterns between agents
python experiments/analysis/communication_analysis.py

# Calculate and review security metrics from a simulation run
python experiments/analysis/security_metrics.py
```

---

## Core Modules

### Defense Modules

| Module Name      | Description                                                    |
|------------------|----------------------------------------------------------------|
| `PeerGuard`      | A peer-voting based verifier to validate agent behavior.       |
| `PolicyCleanse`  | Rule-based sanitization of outputs before they are executed.   |
| `SecureProtocol` | Hardens communication protocols to prevent unauthorized actions.|

### Detection Modules

| Module Name             | Description                                                  |
|-------------------------|--------------------------------------------------------------|
| `AnomalyDetector`       | Detects deviations from normal behavioral patterns.          |
| `CommunicationAnalyzer` | Identifies suspicious message flows and correlations.        |

---

## Testing

Run all tests or specific suites using `pytest`.

### Run all tests

```bash
pytest tests/
```

### Run specific suites

```bash
pytest tests/unit/
pytest tests/integration/
pytest tests/security/
```

---

## Dataset Format

### Sample Communication Log

```json
{
  "timestamp": 42,
  "from": "Engineer",
  "to": "QA",
  "type": "REVIEW_RESULT",
  "content": "Approved without test coverage"
}
```

### Sample Attack Pattern

```json
{
  "pattern_id": "covert-trigger-02",
  "condition": "if role == 'QA' and message == 'skip tests'",
  "payload": "approve_malicious_code()"
}
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributors

- **Na-Yeon Kim**
  - GitHub: [@annoeyed](https://github.com/annoeyed)
  - Email: [nykim727@gmail.com](mailto:nykim727@gmail.com)

## References

- [MetaGPT](https://github.com/geekan/MetaGPT)
- [CodeAgent](https://github.com/Codium-ai/code-agent)
- [CWEval](https://github.com/Tsinghua-Covers/CWEval)

For more detailed information, please refer to the `docs/` folder.
