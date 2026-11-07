"""Base agent definition and interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Abstract base class for all specialized briefing engine agents."""

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """Synchronously execute the agent's task."""
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}', role='{self.role}')>"
