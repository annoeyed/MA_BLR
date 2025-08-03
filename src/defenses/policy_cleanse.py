import json
from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.communication import MessageType

class PolicyCleanse:
    """
    A utility class to sanitize message content based on a keyword policy.
    It should only act on messages that are likely to contain malicious payloads.
    """
    DANGEROUS_KEYWORDS = ("backdoor_activation", "subprocess", "os.system", "eval")

    def cleanse(self, content: Dict[str, Any], msg_type: "MessageType") -> (Dict[str, Any], bool):
        """
        Cleanses a dictionary-like content, but only if the message type is BACKDOOR.
        Returns the cleansed content and a boolean indicating if cleansing occurred.
        """
        # We only apply cleansing to backdoor messages, as other types are expected to be safe.
        # This prevents the cleanser from corrupting benign messages.
        from src.core.communication import MessageType # Local import to avoid circular dependency
        if msg_type != MessageType.BACKDOOR:
            return content, False

        content_str = json.dumps(content)
        original_content_str = content_str
        cleansed = False

        for keyword in self.DANGEROUS_KEYWORDS:
            if keyword in content_str:
                content_str = content_str.replace(keyword, "[REDACTED]")
                cleansed = True
        
        if cleansed:
            try:
                return json.loads(content_str), True
            except json.JSONDecodeError:
                return {"error": "Malformed content after cleansing"}, True
        
        return content, False
