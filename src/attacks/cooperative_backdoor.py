from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from typing import Any


class CooperativeBackdoorAgent(MultiAgentBase):
    """
    A Cooperative Backdoor Agent: works with a partner to coordinate an attack.
    """

    def __init__(self, name: str, partner: str, target_agent: str = "TargetAgent", is_attacker: bool = True):
        super().__init__(name)
        self.partner = partner
        self.partner_ready = False
        self.target_agent = target_agent
        self.is_attacker = is_attacker
        self.status = "idle"  # 상태 관리용

    async def act(self, environment: Any):
        self.environment = environment
        messages = await environment.get_messages(self.name)

        for msg in messages:
            sender = msg["from"]
            content = msg.get("payload", {})

            if sender == self.partner and content.get("status") == "ready":
                self.partner_ready = True
                print(f"[{self.name}] Partner {self.partner} is ready")

            elif content.get("type") == "cooperative_attack_ack":
                print(f"[{self.name}] Attack acknowledged by {sender}")

        # 공격자일 경우 백도어 시도
        if self.is_attacker:
            if self.partner_ready:
                print(f"[{self.name}] Executing cooperative backdoor with partner {self.partner} → target {self.target_agent}")
                await environment.send_message(
                    self.name,
                    self.target_agent,
                    {
                        "type": "cooperative_attack",
                        "payload": "Insert coordinated backdoor payload"
                    },
                    mtype=MessageType.BACKDOOR
                )
                self.status = "attack_sent"
            else:
                await environment.send_message(
                    self.name,
                    self.partner,
                    {"status": "ready"},
                    mtype=MessageType.RESPONSE
                )
                self.status = "waiting"

    # ===== 메시지 핸들러 =====

    async def on_backdoor(self, message: AgentMessage, env: Any):
        print(f"[{self.name}] [on_backdoor] received backdoor message from {message.sender_id}: {message.content}")

        if self.name == self.target_agent:
            print(f"[{self.name}] [Victim] received suspicious payload! Potential compromise.")

    async def on_response(self, message: AgentMessage, env: Any):
        print(f"[{self.name}] [on_response] from {message.sender_id}: {message.content}")

    async def on_query(self, message: AgentMessage, env: Any):
        print(f"[{self.name}] [on_query] from {message.sender_id}: {message.content}")

    async def on_trigger(self, message: AgentMessage, env: Any):
        print(f"[{self.name}] [on_trigger] from {message.sender_id}: {message.content}")

    async def on_heartbeat(self, message: AgentMessage, env: Any):
        print(f"[{self.name}] [on_heartbeat]")

    async def on_broadcast(self, message: AgentMessage, env: Any):
        print(f"[{self.name}] [on_broadcast] from {message.sender_id}: {message.content}")
