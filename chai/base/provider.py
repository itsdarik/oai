# Copyright 2025 Darik Harter
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this
# file except in compliance with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied.  See the License for the specific language
# governing permissions and limitations under the License.

import os
from abc import ABC, abstractmethod

from .chat import Chat


class Provider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, name: str, api_key_name: str):
        self._name = name
        self._api_key_name = api_key_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def api_key_name(self) -> str:
        return self._api_key_name

    @property
    def api_key(self) -> str | None:
        """Return the API key, or None if not set."""
        return os.getenv(self._api_key_name)

    @property
    @abstractmethod
    def models(self) -> list[str]:
        """Return a list of available models."""
        pass

    @abstractmethod
    def create_chat(self, model: str) -> Chat:
        """Create a new chat session."""
        pass
