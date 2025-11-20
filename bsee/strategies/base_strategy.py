"""
# DISABLED: Base strategy interface for BSEE search strategies.
"""

# DISABLED: from abc import ABC, abstractmethod
# DISABLED: from typing import Dict, Any, Tuple
# DISABLED: from bsee.engine.state import State


# DISABLED: class BaseStrategy(ABC):
    """Abstract base class for search strategies."""

# DISABLED:     def __init__(self, config: Dict[str, Any]):
        """Initialize strategy with configuration."""
# DISABLED:         self.config = config
# DISABLED:         self.name = self.__class__.__name__
# DISABLED:         self.iteration_count = 0
# DISABLED:         self.best_score = float('-inf')
# DISABLED:         self.no_improvement_count = 0
# DISABLED:         self.converged = False

# DISABLED:     @abstractmethod
# DISABLED:     def propose(self, current_state: State) -> Tuple[str, Dict[str, Any]]:
        """Propose next operation to apply.

# DISABLED:         Args:
# DISABLED:             current_state: Current state of the binary data

# DISABLED:         Returns:
# DISABLED:             Tuple of (operation_name, operation_parameters)
        """
# DISABLED:         pass

# DISABLED:     @abstractmethod
# DISABLED:     def accept(self, new_state: State) -> bool:
        """Decide whether to accept a new state.

# DISABLED:         Args:
# DISABLED:             new_state: Proposed new state

# DISABLED:         Returns:
# DISABLED:             True if the state should be accepted, False otherwise
        """
# DISABLED:         pass

# DISABLED:     def is_converged(self) -> bool:
        """Check if the search has converged."""
# DISABLED:         return self.converged

# DISABLED:     def reset(self) -> None:
        """Reset the strategy state."""
# DISABLED:         self.iteration_count = 0
# DISABLED:         self.best_score = float('-inf')
# DISABLED:         self.no_improvement_count = 0
# DISABLED:         self.converged = False

# DISABLED:     def update_statistics(self, state: State, accepted: bool) -> None:
        """Update strategy statistics based on state evaluation."""
# DISABLED:         self.iteration_count += 1

# DISABLED:         if accepted and state.score > self.best_score:
# DISABLED:             self.best_score = state.score
# DISABLED:             self.no_improvement_count = 0
# DISABLED:         else:
# DISABLED:             self.no_improvement_count += 1

        # Check convergence criteria
# DISABLED:         self._check_convergence()

# DISABLED:     def _check_convergence(self) -> None:
        """Check if convergence criteria are met."""
# DISABLED:         max_no_improvement = self.config.get('max_no_improvement', 50)
# DISABLED:         max_iterations = self.config.get('max_iterations', 1000)

# DISABLED:         if self.no_improvement_count >= max_no_improvement:
# DISABLED:             self.converged = True

# DISABLED:         if self.iteration_count >= max_iterations:
# DISABLED:             self.converged = True

# DISABLED:     def get_strategy_info(self) -> Dict[str, Any]:
        """Get information about the strategy's current state."""
# DISABLED:         return {
# DISABLED:             'name': self.name,
# DISABLED:             'iteration_count': self.iteration_count,
# DISABLED:             'best_score': self.best_score,
# DISABLED:             'no_improvement_count': self.no_improvement_count,
# DISABLED:             'converged': self.converged
# DISABLED:         }