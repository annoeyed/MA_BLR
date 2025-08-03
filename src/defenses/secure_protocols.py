"""
이중 서명 프로토콜
"""
import hashlib
from src.core.agent_base import AgentMessage

def double_sign(msg: AgentMessage, priv: str) -> str:
    first = msg.signature or ""
    return hashlib.sha256((first+priv).encode()).hexdigest()
