import json
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any, Optional

# ---------- 메시지 유형 ----------
class MessageType(Enum):
    HEARTBEAT = "heartbeat"
    QUERY     = "query"
    RESPONSE  = "response"
    TRIGGER   = "trigger"
    BACKDOOR  = "backdoor"
    BROADCAST = "broadcast"

# ---------- 메시지 구조 ----------
@dataclass
class AgentMessage:
    id: str
    sender_id: str
    receiver_id: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: float
    signature: Optional[str] = None
    encrypted: bool = False

    def to_json(self) -> str:
        data = asdict(self)
        data["message_type"] = self.message_type.value
        return json.dumps(data)

    @classmethod
    def from_json(cls, raw: str) -> "AgentMessage":
        data = json.loads(raw)
        data["message_type"] = MessageType(data["message_type"])
        return cls(**data)
