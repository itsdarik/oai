from .chat import Chat

from .openai import OpenAIProvider, API_KEY as OPENAI_API_KEY

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
    def models(self) -> list[str]:
        """Return a list of available models."""
        pass

    @abstractmethod
    def create_chat(self, model: str) -> Chat:
        """Create a new chat session."""
        pass


def get_api_key(key: str) -> str:
    """Get an API key from an environment variable."""
    api_key = os.getenv(key)
    if api_key is None:
        raise RuntimeError(f"{key} environment variable not set")
    return api_key


def get_providers() -> list[Provider]:
    """Return a list of available providers."""
    providers = []
    if os.getenv(OPENAI_API_KEY):
        providers.append(OpenAIProvider())
    return providers
