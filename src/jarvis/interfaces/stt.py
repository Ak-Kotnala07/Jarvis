"""Specify speech-to-text interface. Layer: interfaces. May import typing only; may not import adapters, tools, or platform."""

from typing import Protocol


class SpeechToText(Protocol):
    """Transcribe audio without choosing a provider."""

    def transcribe(self, audio: bytes) -> str:
        """Return a transcription for audio."""

