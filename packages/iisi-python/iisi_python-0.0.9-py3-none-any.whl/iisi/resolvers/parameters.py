"""_summary_
"""
import json
import logging
from dataclasses import dataclass
from typing import Any, Dict

from .resolver import ParameterResolver

log = logging.getLogger(__name__)


@dataclass
class DefaultParameterResolver(ParameterResolver):
    """Handle JWT token claims."""

    def resolve(self, event: Dict[str, Any]):
        """_summary_

        Args:
            event (Dict[str, Any]): _description_

        Returns:
            _type_: _description_
        """
        return event.get("pathParameters", {}) | json.loads(event.get("body", "{}"))
