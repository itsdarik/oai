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


class Message(ABC):
    """Abstract base class for chat messages."""

    def __init__(self, role: str, content: str):
        self.role: str = role
        self.content: str = content

    @abstractmethod
    def dict(self) -> dict:
        """Return the message as a dictionary."""
        pass

    @abstractmethod
    def from_user(self) -> bool:
        """Return True if the message is from the user, False otherwise."""
        pass
