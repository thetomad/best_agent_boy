import json
import requests
# Va trebui sa nu mai import aici - poate injection?
from tools import TOOLS_IMPLS


class Agent:

    # Cred ca merge ca format general. Il putem face dinamic daca e mai tarziu.
    format = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "used_tools": {
                "type": "array",
                "items": {"type": "string"}
            },
            "confidence": {
                "type": "string",
                "enum": ["low", "medium", "high"]
            }
        },
        "required": ["answer", "used_tools", "confidence"]
    }


    def __init__(self, url: str, model: str, agent_description: str, tools: list):
        self.url = url
        self.model = model
        self.tools = tools
        self.messages = [
                    {
                        "role": "system",
                        "content": agent_description
                    }
                ]

    def chat(self, user_input: str):

        self.messages.append({"role": "user", "content": user_input})

        used_tools = []
        while True:

            payload = {
                        "model": self.model,
                        "messages": self.messages,
                        "stream": False
                    }

            if self.tools:
                payload["tools"] = self.tools
            if self.format:
                payload["format"] = self.format

            
            response = requests.post(self.url, json = payload, timeout=120)
            response.raise_for_status()

            response = response.json()

            message = response.get("message")

            self.messages.append(message)

            tool_calls = message.get("tool_calls", [])
            
            if not tool_calls:
                return self.messages
                break

            for tc in tool_calls:
                name = tc["function"]["name"]
                args = tc["function"].get("arguments", {})

                if name not in TOOLS_IMPLS:
                    result = {"error": f"Unknown tool: {name}"}
                else:
                    try:
                        result = TOOLS_IMPLS[name](**args)
                        used_tools.append(name)
                    except Exception as e:
                        result = {"error": str(e)}

                self.messages.append({"role": "tool", "content": json.dumps(result)})


