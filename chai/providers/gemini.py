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
from google.genai.types import Content, Part

from ..base.chat import Chat
from ..base.message import Message
from ..base.provider import Provider


class GeminiChat(Chat):
    """Gemini chat session."""

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(model)
        self._client: genai.Client = genai.Client(api_key=api_key)
        self._chat = self._client.chats.create(model=model)

    def send(self, message: str) -> Generator[str, None, None]:
        self._history.append(Message(role="user", content=message))

        full_content = ""

        for chunk in self._chat.send_message_stream(message):
            content = chunk.text
            if content:
                full_content += content
                yield content

        self._history.append(Message(role="assistant", content=full_content))

    def clear(self) -> None:
        super().clear()
        self._chat = self._client.chats.create(model=self._model)

    def load(self, history: list[Message]) -> None:
        super().load(history)
        chat_history = []
        for message in history:
            role = "model" if message.role == "assistant" else message.role
            chat_history.append(Content(parts=[Part(text=message.content)], role=role))
        self._chat = self._client.chats.create(model=self._model, history=chat_history)


class GeminiProvider(Provider):
    """Gemini provider."""

    def __init__(self) -> None:
        super().__init__("Gemini", "GEMINI_API_KEY")

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
