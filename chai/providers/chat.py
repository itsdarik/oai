from abc import ABC, abstractmethod
from typing import Generator


class Message(ABC):
    """Abstract base class for chat messages."""

    def __init__(self, role: str, content: str):
        self.role: str = role
        self.content: str = content

    @abstractmethod
    def dict(self) -> dict[str, str]:
        """Return the message as a dictionary."""
        pass

    @abstractmethod
    def from_user(self) -> bool:
        """Return True if the message is from the user, False otherwise."""
        pass


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

    def clear(self) -> None:
        """Clear the chat history."""
        self.history.clear()
