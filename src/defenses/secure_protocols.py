"""
Double Signature Protocol
"""
import hashlib
from src.core.communication import AgentMessage

def double_sign(msg: AgentMessage, private_key: str) -> str:
    """
    Applies a second signature to an already signed message.
    """
    first_signature = msg.signature or ""
    return hashlib.sha256((first_signature + private_key).encode()).hexdigest()
