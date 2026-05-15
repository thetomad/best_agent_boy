import os
import json
from dataclasses import dataclass
from collections.abc import Callable 
from typing import Any


# Implementations
from documents import read_internal_documents


@dataclass(frozen=True, slots=True)
class Tool:
    """Class for holding the tools data and implementations."""
    name: str
    agent_descr: dict
    implementation: Callable[..., Any]


def get_tool_registry() -> list[Tool]:
    with open(os.path.dirname(__file__) + "/tools.json", "r") as tools_file:
        tools: list = json.load(tools_file) 

    return [
        Tool(tool.get("function").get("name"), tool, globals()[tool.get("function").get("name")])
        for tool in tools
    ]


tools_registry = get_tool_registry()

