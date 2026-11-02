"""Specify tool interface. Layer: interfaces. May import typing only; may not import adapters, tools, or platform."""

from typing import Protocol


class Tool(Protocol):
    """Execute a configured tool through the safety boundary."""

    def execute(self, parameters: dict[str, object]) -> object:
        """Accept validated tool parameters."""

