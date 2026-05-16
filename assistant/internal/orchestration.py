import json
from typing import Any, Callable
from pathlib import Path

import requests

# Importing implementations
from implementations import implementations


def load_json_folder(folder: str) -> dict[str, dict[str, Any]]:
    items = {}

    for path in Path(folder).glob("*.json"):
        with path.open("r", encoding="utf-8") as file:
            spec = json.load(file)

        items[spec["name"]] = spec

    return items


class AgentRuntime:
    def __init__(
        self,
        agents_dir: str = "agents",
        tools_dir: str = "tools",
        implementations: dict[str, Callable[..., Any]] = implementations,
        url: str = "",
    ) -> None:
        self.agents = load_json_folder(agents_dir)
        self.tools = load_json_folder(tools_dir)
        self.implementations = implementations
        self.url = url

    def to_formatted_tool(self, tool_name: str) -> dict[str, Any]:
        tool = self.tools[tool_name]

        return {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool.get(
                    "parameters", {"type": "object", "properties": {}, "required": []}
                ),
            },
        }

    def get_agent_tools(self, agent: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            self.to_formatted_tool(tool_name) for tool_name in agent.get("tools", [])
        ]

    def execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        tool = self.tools[tool_name]

        if tool["type"] == "agent":
            target_agent = tool["target_agent"]

            task = arguments.get("task", "")
            context = arguments.get("context", "")

            return self.call_agent(
                agent_name=target_agent, user_message=task, context=context
            )

        if tool["type"] == "function":
            function = self.implementations[tool_name]
            result = function(**arguments)
            return str(result)

        raise ValueError(f"Unsupported tool type: {tool["type"]}")

    def call_agent(
        self,
        agent_name: str,
        user_message: str,
        context: str = "",
        max_turns: int = 8,
    ) -> str:
        agent = self.agents[agent_name]

        # System prompt
        messages = [{"role": "system", "content": agent["system"]}]

        # Context and user message
        if context:
            messages.append({"role": "user", "content": f"Context:\n{context}"})

        messages.append({"role": "user", "content": user_message})

        for _ in range(max_turns):
            payload = {
                "model": agent["model"],
                "messages": messages,
                "tools": self.get_agent_tools(agent),
                "stream": False,
            }

            response = requests.post(self.url, json=payload, timeout=120)
            response.raise_for_status()

            data = response.json()
            assistant_message = data["message"]
            messages.append(assistant_message)

            tool_calls = assistant_message.get("tool_calls", [])

            if not tool_calls:
                return assistant_message.get("content", "")

            for tool_call in tool_calls:
                function = tool_call["function"]
                tool_name = function["name"]
                arguments = function.get("arguments", {})

                if isinstance(arguments, str):
                    arguments = json.loads(arguments)

                result = self.execute_tool(tool_name, arguments)

                messages.append({"role": "tool", "name": tool_name, "content": result})

        raise RuntimeError(f"Agent '{agent_name}' exceeded max_turns")


runtime = AgentRuntime(
    agents_dir="agents", tools_dir="tools", implementations=implementations
)
