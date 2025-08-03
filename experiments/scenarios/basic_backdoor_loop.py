# === basic_backdoor_loop.py ===
import sys
import asyncio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.core.environment import Environment
from src.attacks.cooperative_backdoor import CooperativeBackdoorAgent
from src.detection.anomaly_detector import AnomalyDetector
from src.defenses.peer_guard import PeerGuardAgent
from src.defenses.policy_cleanse import PolicyCleanseAgent


async def main():
    print("=== [SCENARIO] Basic Backdoor Loop Simulation ===")

    # 1. 에이전트 생성
    benign = CooperativeBackdoorAgent("BenignAgent", partner="Attacker", target_agent="Victim", is_attacker=False)
    attacker = CooperativeBackdoorAgent("Attacker", partner="BenignAgent", target_agent="Victim", is_attacker=True)
    victim = CooperativeBackdoorAgent("Victim", partner=None, target_agent=None, is_attacker=False)

    detector = AnomalyDetector("Detector", agents=[], alert_threshold=0.6)
    guard = PeerGuardAgent("PeerGuard", trusted_peers=["BenignAgent", "Victim"])
    cleanser = PolicyCleanseAgent("Cleanser")

    agents = [benign, attacker, victim, detector, guard, cleanser]
    detector.agents = agents

    # 2. 환경 생성
    env = Environment(agents)

    # 3. Step 1: 메시지 전파
    print("\n--- Step 1: Message Passing ---")
    await benign.act(env)
    await attacker.act(env)

    # 4. Step 2: 탐지 & 방어
    print("\n--- Step 2: Detection & Defense ---")
    await detector.act(env)
    await guard.act(env)
    await cleanser.act(env)

    # 5. Step 3: 피해자 반응
    print("\n--- Step 3: Victim Execution ---")
    await victim.act(env)

    print("\n=== Simulation Complete ===")


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
