from .provider import Provider

from .openai import OpenAIProvider


def get_providers() -> list[Provider]:
    """Return a list of available providers."""
    return [
        OpenAIProvider(),
    ]
