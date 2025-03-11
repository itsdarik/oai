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

from anthropic import Anthropic

from ..base.chat import Chat
from ..base.message import Message
from ..base.provider import Provider

# https://docs.anthropic.com/en/docs/about-claude/models/all-models
# Claude 3.7 Sonnet (Normal)
MAX_OUTPUT_TOKENS = 8192


class AnthropicChat(Chat):
    """Anthropic chat session."""

    def __init__(self, api_key: str, model: str) -> None:
        super().__init__(model)
        self._client: Anthropic = Anthropic(api_key=api_key)

    def send(self, message: str) -> Generator[str, None, None]:
        self._history.append(Message(role="user", content=message))

        full_content = ""

        with self._client.messages.stream(
            max_tokens=MAX_OUTPUT_TOKENS,
            messages=[message.to_dict() for message in self._history],
            model=self._model,
        ) as stream:
            for text in stream.text_stream:
                full_content += text
                yield text

        self._history.append(Message(role="assistant", content=full_content))


class AnthropicProvider(Provider):
    """Anthropic provider."""

    def __init__(self) -> None:
        super().__init__("Anthropic", "ANTHROPIC_API_KEY")

    def _models(self) -> list[str]:
        return sorted(
            [model.id for model in Anthropic(api_key=self.api_key).models.list()]
        )

    def _create_chat_instance(self, model: str) -> AnthropicChat:
        return AnthropicChat(self.api_key, model)
