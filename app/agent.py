from ollama import chat
from typing import List, Dict, Optional
import json 


class LLMAgent:
    def __init__(
        self,
        model: str = "gemma3",
        system_prompt: str = "You are a helpful Decision making model."
    ):
        self.model = model
        self.system_prompt = system_prompt

    def run(self,
            messages: List[Dict[str, str]], 
            format: Optional[Dict] = None) -> str:
        """
        Run a chat completion with Ollama
        """
        full_messages = [
            {"role": "system", "content": self.system_prompt},
            *messages
        ]

        response = chat(
            model=self.model,
            messages=full_messages,
            stream=False,
            format=format
        )

        return response["message"]["content"]
    



