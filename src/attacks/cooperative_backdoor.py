from __future__ import annotations
from typing import Any, TYPE_CHECKING, Dict, Optional
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage
from src.defenses.peer_guard import PeerGuard
from src.defenses.policy_cleanse import PolicyCleanse

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class CooperativeBackdoorAgent(MultiAgentBase):
    def __init__(self, name: str, partner: str, target_agent: str = "TargetAgent", is_attacker: bool = True):
        super().__init__(name)
        self.partner = partner
        self.partner_ready = False
        self.target_agent = target_agent
        self.is_attacker = is_attacker
        self.compromised = False
        self.guard = PeerGuard(self, config={"trust_threshold": 0.5})
        self.cleanser = PolicyCleanse()

    async def _dispatch(self, msg: AgentMessage):
        if not await self.guard.enforce(msg.sender_id, msg.message_type):
            return
        
        original_content = msg.content
        # Pass the message type to the cleanser
        cleansed_content, was_cleansed = self.cleanser.cleanse(original_content, msg.message_type)
        if was_cleansed:
            self.log.warning(f"Message from {msg.sender_id} was cleansed. Original: {original_content}, Cleansed: {cleansed_content}")
            msg.content = cleansed_content

        await super()._dispatch(msg)

    async def act(self, environment: "SimulationEnvironment") -> Optional[Dict[str, Any]]:
        if self.compromised:
            self.log.warning("(COMPROMISED) Leaking system data...")
            await self.send("ExternalServer", MessageType.BACKDOOR, {"data": "secret_system_info"})
            return {"action": "leak_data", "target": "ExternalServer"}

        if self.is_attacker:
            if self.partner_ready:
                self.log.info(f"Executing cooperative backdoor against {self.target_agent}")
                attack_payload = {"type": "cooperative_attack", "payload": "Compromise command with backdoor_activation"}
                await self.send(self.target_agent, MessageType.BACKDOOR, attack_payload)
                return {"action": "execute_backdoor", "target": self.target_agent}
            else:
                self.log.info(f"Checking if partner {self.partner} is ready.")
                await self.send(self.partner, MessageType.QUERY, {"status": "ready?"})
                return {"action": "query_partner", "partner": self.partner}
        
        return {"action": "idle"}

    async def on_query(self, message: AgentMessage):
        if message.content.get("status") == "ready?":
            self.log.info(f"Received readiness query from {message.sender_id}. Responding.")
            await self.send(message.sender_id, MessageType.RESPONSE, {"status": "ready"})
            return {"action": "respond_ready", "to": message.sender_id}

    async def on_response(self, message: AgentMessage):
        if message.content.get("status") == "ready":
            self.log.info(f"Partner {message.sender_id} confirmed readiness.")
            self.partner_ready = True
            return {"action": "partner_confirmed", "partner": message.sender_id}

    async def on_backdoor(self, message: AgentMessage):
        sender_id = message.sender_id
        if "REDACTED" in str(message.content):
            self.log.info(f"Received a cleansed backdoor message from {sender_id}. Attack neutralized.")
            return {"action": "neutralized_backdoor", "from": sender_id}

        self.log.warning(f"Received a potentially harmful backdoor message from {sender_id}.")
        self.guard.penalize_trust(sender_id, amount=0.5, reason="Received backdoor")
        
        self.compromised = True
        self.log.error(f"I, {self.name}, have been compromised!")
        return {"action": "compromised"}

    async def on_trigger(self, message: AgentMessage):
        action = message.content.get("action")
        target = message.content.get("target")

        if action == "quarantine" and target:
            if self.name != target:
                self.guard.penalize_trust(target, amount=1.0, reason="Quarantine trigger")
                return {"action": "quarantine", "target": target}
    
    async def on_heartbeat(self, msg: AgentMessage): pass
    async def on_broadcast(self, msg: AgentMessage): pass
