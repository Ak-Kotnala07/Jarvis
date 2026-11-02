"""Specify trigger interface. Layer: interfaces. May import typing only; may not import adapters, tools, or platform."""

from typing import Protocol


class Trigger(Protocol):
    """Receive an activation event without choosing an implementation."""

    def wait_for_activation(self) -> None:
        """Wait for an activation event."""

