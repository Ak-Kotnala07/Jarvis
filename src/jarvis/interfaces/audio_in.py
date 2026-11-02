"""Specify audio input interface. Layer: interfaces. May import typing only; may not import adapters, tools, or platform."""

from typing import Protocol


class AudioInput(Protocol):
    """Capture audio without choosing an implementation."""

    def capture(self) -> bytes:
        """Capture one audio payload."""

