from .provider import Provider

from .openai import OpenAIProvider, API_KEY as OPENAI_API_KEY

import os


def get_providers() -> list[Provider]:
    """Return a list of available providers."""
    providers = []
    if os.getenv(OPENAI_API_KEY):
        providers.append(OpenAIProvider())
    return providers
