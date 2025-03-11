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

from openai import OpenAI

from ..base.chat import Chat, Message
from ..base.provider import Provider

XAI_URL = "https://api.x.ai/v1"


class XAIMessage(Message):
    """XAI chat message."""

    def dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}

    def from_user(self) -> bool:
        return self.role == "user"


class XAIChat(Chat):
    """XAI chat session."""

    def __init__(self, api_key: str, model: str) -> None:
        self._client: OpenAI = OpenAI(api_key=api_key, base_url=XAI_URL)
        self._model: str = model
        self._history: list[XAIMessage] = []

    @property
    def model(self) -> str:
        return self._model

    @property
    def history(self) -> list[XAIMessage]:
        return self._history

    def send(self, message: str) -> Generator[str, None, None]:
        self._history.append(XAIMessage(role="user", content=message))

        response = self._client.chat.completions.create(
            messages=[message.dict() for message in self._history],
            model=self._model,
            stream=True,
        )

        full_content = ""

        for chunk in response:
            if chunk.choices[0].delta.content:
                chunk_content = chunk.choices[0].delta.content
                full_content += chunk_content
                yield chunk_content

        self._history.append(XAIMessage(role="assistant", content=full_content))

    def create_message(self, message_data: dict[str, str]) -> XAIMessage:
        return XAIMessage(role=message_data["role"], content=message_data["content"])


class XAIProvider(Provider):
    """XAI provider."""

    @property
    def name(self) -> str:
        return "xAI"

    @property
    def api_key_name(self) -> str:
        return "XAI_API_KEY"

    @property
    def models(self) -> list[str]:
        if self.api_key is None:
            raise RuntimeError(f"{self.api_key_name} environment variable not set")
        try:
            return sorted(
                [
                    model.id
                    for model in OpenAI(
                        api_key=self.api_key, base_url=XAI_URL
                    ).models.list()
                ]
            )
        except Exception as e:
            raise RuntimeError(f"Error getting models: {e}")

    def create_chat(self, model: str) -> XAIChat:
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")
        if self.api_key is None:
            raise RuntimeError(f"{self.api_key_name} environment variable not set")
        return XAIChat(self.api_key, model)
