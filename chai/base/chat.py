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

from abc import ABC, abstractmethod
from typing import Generator

from .message import Message


class Chat(ABC):
    """Abstract base class for chat sessions."""

    def __init__(self, model: str) -> None:
        self._model: str = model
        self._history: list[Message] = []

    @property
    def model(self) -> str:
        return self._model

    @property
    def history(self) -> list[Message]:
        return self._history

    def clear(self) -> None:
        """Clear the chat history."""
        self._history.clear()

    def load(self, history: list[Message]) -> None:
        """Replace chat with a saved chat."""
        self.clear()
        self._history.extend(history)

    @abstractmethod
    def send(self, message: str) -> Generator[str, None, None]:
        """Send a message to the model and stream the response."""
        pass
