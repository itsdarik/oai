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
