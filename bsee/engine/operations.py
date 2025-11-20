"""
Operations module for BSEE
Contains binary operation definitions.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Operation(ABC):
    """Base class for binary operations"""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}

    @abstractmethod
    def apply(self, state):
        """Apply the operation to a binary state"""
        pass

    def __str__(self):
        return f"Operation({self.name})"