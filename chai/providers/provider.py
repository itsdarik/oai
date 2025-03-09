from abc import ABC, abstractmethod
from .chat import Chat


class Provider(ABC):
    """Abstract base class for LLM providers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name."""
        pass

    @property
    @abstractmethod
    def models(self) -> list[str]:
        """Return a list of available models."""
        pass

    @abstractmethod
    def create_chat(self, model: str) -> Chat:
        """Create a new chat session."""
        pass
