from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator


@dataclass(frozen=True)
class Message:
    role: str
    content: str

    def dict(self) -> dict[str, str]:
        return {"role": self.role, "content": self.content}


class Chat(ABC):
    """Abstract base class for LLM chat sessions."""

    @property
    @abstractmethod
    def model(self) -> str:
        """Return the model name."""
        pass

    @property
    @abstractmethod
    def history(self) -> list[Message]:
        """Return the chat history."""
        pass

    @abstractmethod
    def send(self, message: str) -> Generator[str, None, None]:
        """Send a message to the model and stream the response."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the chat history."""
        pass
