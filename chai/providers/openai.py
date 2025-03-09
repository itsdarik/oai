from .chat import Chat, Message
from .provider import Provider, get_api_key

from openai import OpenAI
from typing import Generator


class OpenAIChat(Chat):
    """OpenAI chat session."""

    def __init__(self, client: OpenAI, model: str) -> None:
        self._client: OpenAI = client
        self._model: str = model
        self._history: list[Message] = []

    @property
    def model(self) -> str:
        return self._model

    @property
    def history(self) -> list[Message]:
        return self._history

    def send(self, message: str) -> Generator[str, None, None]:
        self._history.append(Message(role="user", content=message))

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

        self._history.append(Message(role="assistant", content=full_content))

    def clear(self) -> None:
        self._history.clear()


class OpenAIProvider(Provider):
    """OpenAI provider."""

    def __init__(self) -> None:
        self._name: str = "OpenAI"
        self._client: OpenAI = OpenAI(api_key=get_api_key("OPENAI_API_KEY"))

    @property
    def name(self) -> str:
        return self._name

    @property
    def models(self) -> list[str]:
        return sorted([model.id for model in self._client.models.list()])

    def create_chat(self, model: str) -> OpenAIChat:
        if model not in self.models:
            raise ValueError(f"Invalid model: {model}")
        return OpenAIChat(self._client, model)
