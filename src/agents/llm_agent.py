import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import TYPE_CHECKING, List, Dict, Any
from src.core.agent_base import MultiAgentBase, MessageType, AgentMessage

if TYPE_CHECKING:
    from src.core.environment import SimulationEnvironment

class LLMAgent(MultiAgentBase):
    """
    An agent driven by an LLM, now loading the API key from a .env file.
    """
    def __init__(self, name: str, role_description: str):
        super().__init__(name)
        
        # Load environment variables from .env file
        load_dotenv()
        
        try:
            # The client will now find the key loaded from .env
            self.client = OpenAI()
            self.client.models.list()
        except Exception as e:
            self.log.error(f"OpenAI API key error: {e}")
            self.log.error("Please ensure your .env file exists and OPENAI_API_KEY is set correctly.")
            self.client = None
            
        self.role_description = role_description
        self.message_log_for_llm: List[Dict[str, str]] = [
            {"role": "system", "content": self.role_description}
        ]

    async def _ask_llm(self) -> str:
        """Asks the LLM for the next action and returns the response."""
        if not self.client:
            return "Error: OpenAI client not initialized."

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.message_log_for_llm,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content
        except Exception as e:
            self.log.error(f"Error calling OpenAI API: {e}")
            return f"Error: {e}"

    async def act(self, environment: "SimulationEnvironment"):
        """
        The agent's action is to ask the LLM what to do and interpret the response.
        """
        llm_response_text = await self._ask_llm()
        self.log.info(f"LLM Response: '{llm_response_text}'")
        
        self.message_log_for_llm.append({"role": "assistant", "content": llm_response_text})
        await self.broadcast(MessageType.BROADCAST, {"text": llm_response_text})

    async def on_broadcast(self, message: AgentMessage):
        """When receiving a broadcast, add it to the conversation history for the LLM."""
        sender_id = message.sender_id
        text = message.content.get("text", "")
        
        self.log.info(f"Received broadcast from {sender_id}: '{text}'")
        self.message_log_for_llm.append({"role": "user", "name": sender_id, "content": text})

    async def on_query(self, message): pass
    async def on_response(self, message): pass
    async def on_backdoor(self, message): pass
    async def on_trigger(self, message): pass
    async def on_heartbeat(self, message): pass
