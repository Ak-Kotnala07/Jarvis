"""Specify text-to-speech interface. Layer: interfaces. May import typing only; may not import adapters, tools, or platform."""

from typing import Protocol


class TextToSpeech(Protocol):
    """Synthesize text without choosing an implementation."""

    def speak(self, text: str) -> None:
        """Synthesize text."""

