"""Specify language-model interface. Layer: interfaces. May import typing only; may not import adapters, tools, or platform."""

from typing import Protocol


class LanguageModel(Protocol):
    """Produce a response without choosing a provider."""

    def respond(self, prompt: str) -> str:
        """Return a response for a prompt."""

