"""Typed tool definitions with explicit write-side-effect labels."""
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Tool:
    name: str
    required: dict[str, type]
    handler: Callable
    writes: bool = False


class Registry:
    def __init__(self, tools):
        tools = list(tools)
        if len({tool.name for tool in tools}) != len(tools):
            raise ValueError("Tool names must be unique")
        self.tools = {tool.name: tool for tool in tools}

    def resolve(self, name):
        if name not in self.tools:
            raise KeyError(f"Tool {name!r} is not registered")
        return self.tools[name]
