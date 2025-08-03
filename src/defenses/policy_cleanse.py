import json
from typing import Dict, Any

class PolicyCleanse:
    """
    A utility class to sanitize message content based on a keyword policy.
    Can be attached to any agent as a defense mechanism.
    """
    DANGEROUS_KEYWORDS = ("backdoor_activation", "subprocess", "os.system", "eval")

    def cleanse(self, content: Dict[str, Any]) -> (Dict[str, Any], bool):
        """
        Cleanses a dictionary-like content.
        Returns the cleansed content and a boolean indicating if cleansing occurred.
        """
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
                # If cleansing results in invalid JSON, return an error state.
                return {"error": "Malformed content after cleansing"}, True
        
        return content, False
