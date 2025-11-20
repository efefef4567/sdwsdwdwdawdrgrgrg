"""
Strategies module for BSEE
Contains search strategy implementations.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List


class Strategy(ABC):
    """Base class for search strategies"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.name = self.__class__.__name__

    @abstractmethod
    def analyze(self, initial_state, max_iterations: int = 100):
        """Run strategy analysis on initial state"""
        pass

    def __str__(self):
        return f"Strategy({self.name})"