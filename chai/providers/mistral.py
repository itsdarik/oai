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

from mistralai import Mistral

from ..base.chat import Chat
from ..base.message import Message
from ..base.provider import Provider


class MistralChat(Chat):
    """Mistral chat session."""

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(model)
        self._client: Mistral = Mistral(api_key=api_key)

    def send(self, message: str) -> Generator[str, None, None]:
        self._history.append(Message(role="user", content=message))

        response = self._client.chat.stream(
            messages=[message.to_dict() for message in self._history],
            model=self._model,
        )

        full_content = ""

        for chunk in response:
            content = chunk.data.choices[0].delta.content
            if content:
                full_content += content
                yield content

        self._history.append(Message(role="assistant", content=full_content))


class MistralProvider(Provider):
    """Mistral provider."""

    def __init__(self) -> None:
        super().__init__("Mistral", "MISTRAL_API_KEY")

    @property
    def models(self) -> list[str]:
        if self.api_key is None:
            raise RuntimeError(f"{self.api_key_name} environment variable not set")
        try:
            with Mistral(api_key=self.api_key) as mistral:
                return sorted([model.id for model in mistral.models.list().data])
        except Exception as e:
            raise RuntimeError(f"Error getting models: {e}")

    def _create_chat_instance(self, model: str) -> MistralChat:
        return MistralChat(self.api_key, model)
