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

from typing import Generator

from google import genai
from google.genai.types import Content

from .chat import Chat, Message
from .provider import Provider


class GeminiMessage(Message):
    """Gemini chat message."""

    def dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}

    def from_user(self) -> bool:
        return self.role == "user"


class GeminiChat(Chat):
    """Gemini chat session."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client: genai.Client = genai.Client(api_key=api_key)
        self._history: list[Content] = []
        self._chat = self._client.chats.create(model=model, history=self._history)
        self._model: str = model

    @property
    def model(self) -> str:
        return self._model

    @property
    def history(self) -> list[Message]:
        return self._history

    def send(self, message: str) -> Generator[str, None, None]:
        response = self._chat.send_message_stream(message)

        full_content = ""

        for chunk in response:
            chunk_content = chunk.text
            full_content += chunk_content
            yield chunk_content

    def create_message(self, message_data: dict[str, str]) -> GeminiMessage:
        return GeminiMessage(role=message_data["role"], content=message_data["content"])


class GeminiProvider(Provider):
    """Gemini provider."""

    @property
    def name(self) -> str:
        return "Gemini"

    @property
    def api_key_name(self) -> str:
        return "GEMINI_API_KEY"

    @property
    def models(self) -> list[str]:
        if self.api_key is None:
            raise RuntimeError(f"{self.api_key_name} environment variable not set")
        try:
            return sorted(
                [
                    model.name.removeprefix("models/")
                    for model in genai.Client(api_key=self.api_key).models.list()
                ]
            )
        except Exception as e:
            raise RuntimeError(f"Error getting models: {e}")

    def create_chat(self, model: str) -> GeminiChat:
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")
        if self.api_key is None:
            raise RuntimeError(f"{self.api_key_name} environment variable not set")
        return GeminiChat(self.api_key, model)
