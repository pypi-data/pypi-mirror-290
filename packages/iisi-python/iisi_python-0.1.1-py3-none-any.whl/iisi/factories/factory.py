"""
Event handler module.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class IisiFactory(ABC):
    """
    Application event handler
    """

    @abstractmethod
    def __call__(self) -> Any:
        """_summary_"""
        raise NotImplementedError(f"{type(self).__name__} not implemented.")


class TableFactory(IisiFactory):
    """_summary_"""
