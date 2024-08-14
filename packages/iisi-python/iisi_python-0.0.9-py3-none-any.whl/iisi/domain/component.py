"""_summary_"""
from dataclasses import dataclass

from iisi.application import App


@dataclass(frozen=True)
class Component:
    """Represents a Iisi application use case implementation stack."""

    app: App
