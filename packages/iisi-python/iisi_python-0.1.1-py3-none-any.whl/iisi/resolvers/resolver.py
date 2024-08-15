"""
Event handler module.
"""
from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Resolver(ABC):
    """
    Application resolver
    """

    def resolve(self, event: Dict[str, Any]) -> Any:
        """_summary_

        Args:
            event (Dict[str, Any]): _description_

        Returns:
            Dict: _description_
        """
        raise NotImplementedError(f"{type(self).__name__} not implemented.")


@dataclass
class PrincipalResolver(Resolver):
    """Principal resolver"""


@dataclass
class ParameterResolver(Resolver):
    """Application parameter resolver"""


@dataclass
class UsecaseResolver(Resolver):
    """Usecase resolver."""


@dataclass
class UsecaseStackResolver(Resolver):
    """Usecase stack resolver."""
