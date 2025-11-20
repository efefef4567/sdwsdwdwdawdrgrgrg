"""
Greedy hill climbing strategy for BSEE.
"""

import random
from typing import Dict, Any, Tuple, List


class GreedyStrategy:
    """Greedy hill climbing strategy that always accepts improvements."""

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize greedy strategy."""
        self.config = config or {}
        self.restart_threshold = self.config.get('restart_threshold', 10)
        self.random_restart_prob = self.config.get('random_restart_prob', 0.1)
        self.no_improvement_count = 0
        self.best_score = 0.0

    def propose(self, current_state) -> Tuple[str, Dict[str, Any]]:
        """Propose next operation using greedy selection."""
        # Check if we should restart
        if self.no_improvement_count >= self.restart_threshold:
            if random.random() < self.random_restart_prob:
                return self._propose_random_operation()

        # Greedy selection - return a good default operation
        return self._propose_best_known_operation(current_state)

    def accept(self, new_state) -> bool:
        """Accept state if it improves score."""
        # Greedy always accepts improvements
        if new_state.score > self.best_score:
            return True

        # Sometimes accept equal scores for exploration
        if new_state.score == self.best_score and random.random() < 0.1:
            return True

        return False

    def analyze(self, initial_state, max_iterations: int = 100):
        """Run strategy analysis on initial state."""
        current_state = initial_state
        best_state = initial_state
        self.best_score = getattr(initial_state, 'score', 0.0)
        self.no_improvement_count = 0

        for iteration in range(max_iterations):
            # Propose operation
            operation, params = self.propose(current_state)

            # For now, just return the current state as result
            # In a full implementation, this would apply operations
            if hasattr(current_state, 'copy'):
                new_state = current_state.copy()
            else:
                new_state = current_state

            # Accept or reject
            if self.accept(new_state):
                current_state = new_state
                if hasattr(new_state, 'score'):
                    self.no_improvement_count = 0
                    if new_state.score > self.best_score:
                        self.best_score = new_state.score
                        best_state = new_state
            else:
                self.no_improvement_count += 1

        return {
            'best_state': best_state,
            'best_score': self.best_score,
            'iterations': max_iterations
        }

    def _propose_random_operation(self) -> Tuple[str, Dict[str, Any]]:
        """Propose a random operation."""
        operations = [
            ('xor_constant', {'constant': random.randint(1, 255)}),
            ('rotate_left', {'shift': random.randint(1, 7)}),
            ('rotate_right', {'shift': random.randint(1, 7)}),
            ('not_bytes', {}),
            ('swap_nibbles', {})
        ]

        return random.choice(operations)

    def _propose_best_known_operation(self, current_state) -> Tuple[str, Dict[str, Any]]:
        """Propose operation based on heuristics."""
        # Simple heuristic: try different operations based on current score
        if self.best_score < 10:
            # Low score - try basic transformations
            return self._propose_basic_operation()
        else:
            # Higher score - try compression-oriented operations
            return self._propose_compression_operation()

    def _propose_basic_operation(self) -> Tuple[str, Dict[str, Any]]:
        """Propose basic transformation operations."""
        basic_ops = [
            ('xor_constant', {'constant': random.randint(1, 255)}),
            ('rotate_left', {'shift': random.randint(1, 7)}),
            ('rotate_right', {'shift': random.randint(1, 7)}),
            ('not_bytes', {}),
            ('swap_nibbles', {})
        ]
        return random.choice(basic_ops)

    def _propose_compression_operation(self) -> Tuple[str, Dict[str, Any]]:
        """Propose compression-oriented operations."""
        compression_ops = [
            ('move_to_front', {}),
            ('xor_range', {'offset': random.randint(0, 100), 'length': random.randint(10, 50)}),
            ('shuffle_bytes', {'seed': random.randint(0, 10000)})
        ]
        return random.choice(compression_ops)