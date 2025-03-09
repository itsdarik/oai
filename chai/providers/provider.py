from .chat import Chat

from abc import ABC, abstractmethod

import os


class Provider(ABC):
    """Abstract base class for LLM providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        pass

    @property
    @abstractmethod
    def api_key_name(self) -> str:
        """Return the name of the API key environment variable."""
        pass

    @property
    def api_key(self) -> str | None:
        """Return the API key, or None if not set."""
        return os.getenv(self.api_key_name)

    @property
    @abstractmethod
    def models(self) -> list[str]:
        """Return a list of available models."""
        pass

    @abstractmethod
    def create_chat(self, model: str) -> Chat:
        """Create a new chat session."""
        pass
