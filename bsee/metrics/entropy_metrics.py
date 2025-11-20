"""
# DISABLED: Entropy metrics for binary analysis.
"""

# DISABLED: import math
# DISABLED: from typing import Dict, List


# DISABLED: class EntropyMetrics:
    """Collection of entropy-based metrics."""

# DISABLED:     def __init__(self):
        """Initialize entropy metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all entropy metrics."""
# DISABLED:         return {
# DISABLED:             'shannon_entropy_global': self.shannon_entropy_global,
# DISABLED:             'entropy_global': self.shannon_entropy_global,  # Alias for backward compatibility
# DISABLED:             'shannon_entropy_windowed_8': self.shannon_entropy_windowed_8,
# DISABLED:             'shannon_entropy_windowed_16': self.shannon_entropy_windowed_16,
# DISABLED:             'shannon_entropy_windowed_32': self.shannon_entropy_windowed_32,
# DISABLED:             'shannon_entropy_windowed_64': self.shannon_entropy_windowed_64,
# DISABLED:             'shannon_entropy_windowed_128': self.shannon_entropy_windowed_128,
# DISABLED:             'shannon_entropy_windowed_256': self.shannon_entropy_windowed_256,
# DISABLED:             'conditional_entropy_order1': self.conditional_entropy_order1,
# DISABLED:             'conditional_entropy_order2': self.conditional_entropy_order2,
# DISABLED:             'entropy_variance': self.entropy_variance,
# DISABLED:             'entropy_gradient': self.entropy_gradient,
# DISABLED:             'relative_entropy': self.relative_entropy,
# DISABLED:             'entropy_efficiency': self.entropy_efficiency
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'shannon_entropy_global': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Shannon entropy of entire binary',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'entropy_global': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Shannon entropy of entire binary (alias)',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'shannon_entropy_windowed_8': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Average Shannon entropy in 8-byte windows',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'shannon_entropy_windowed_16': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Average Shannon entropy in 16-byte windows',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'shannon_entropy_windowed_32': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Average Shannon entropy in 32-byte windows',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'shannon_entropy_windowed_64': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Average Shannon entropy in 64-byte windows',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'shannon_entropy_windowed_128': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Average Shannon entropy in 128-byte windows',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'shannon_entropy_windowed_256': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Average Shannon entropy in 256-byte windows',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'conditional_entropy_order1': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'First-order conditional entropy',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'conditional_entropy_order2': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Second-order conditional entropy',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'entropy_variance': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Variance of entropy across windows',
# DISABLED:                 'range': [0, 16],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'entropy_gradient': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Average entropy gradient magnitude',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'relative_entropy': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Entropy relative to maximum possible',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'entropy_efficiency': {
# DISABLED:                 'category': 'entropy',
# DISABLED:                 'description': 'Efficiency of entropy distribution',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def shannon_entropy_global(self, binary_data: bytes) -> float:
        """Calculate Shannon entropy of entire binary."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Count frequency of each byte value
# DISABLED:         frequency = [0] * 256
# DISABLED:         for byte_val in binary_data:
# DISABLED:             frequency[byte_val] += 1

        # Calculate entropy
# DISABLED:         entropy = 0.0
# DISABLED:         total = len(binary_data)

# DISABLED:         for count in frequency:
# DISABLED:             if count > 0:
# DISABLED:                 probability = count / total
# DISABLED:                 entropy -= probability * math.log2(probability)

# DISABLED:         return entropy

# DISABLED:     def shannon_entropy_windowed(self, binary_data: bytes, window_size: int) -> float:
        """Calculate average Shannon entropy in sliding windows."""
# DISABLED:         if len(binary_data) < window_size or window_size == 0:
# DISABLED:             return self.shannon_entropy_global(binary_data)

# DISABLED:         entropies = []
# DISABLED:         for i in range(0, len(binary_data) - window_size + 1, window_size // 2):
# DISABLED:             window = binary_data[i:i + window_size]
# DISABLED:             entropy = self.shannon_entropy_global(window)
# DISABLED:             entropies.append(entropy)

# DISABLED:         return sum(entropies) / len(entropies) if entropies else 0.0

# DISABLED:     def shannon_entropy_windowed_8(self, binary_data: bytes) -> float:
        """Average Shannon entropy in 8-byte windows."""
# DISABLED:         return self.shannon_entropy_windowed(binary_data, 8)

# DISABLED:     def shannon_entropy_windowed_16(self, binary_data: bytes) -> float:
        """Average Shannon entropy in 16-byte windows."""
# DISABLED:         return self.shannon_entropy_windowed(binary_data, 16)

# DISABLED:     def shannon_entropy_windowed_32(self, binary_data: bytes) -> float:
        """Average Shannon entropy in 32-byte windows."""
# DISABLED:         return self.shannon_entropy_windowed(binary_data, 32)

# DISABLED:     def shannon_entropy_windowed_64(self, binary_data: bytes) -> float:
        """Average Shannon entropy in 64-byte windows."""
# DISABLED:         return self.shannon_entropy_windowed(binary_data, 64)

# DISABLED:     def shannon_entropy_windowed_128(self, binary_data: bytes) -> float:
        """Average Shannon entropy in 128-byte windows."""
# DISABLED:         return self.shannon_entropy_windowed(binary_data, 128)

# DISABLED:     def shannon_entropy_windowed_256(self, binary_data: bytes) -> float:
        """Average Shannon entropy in 256-byte windows."""
# DISABLED:         return self.shannon_entropy_windowed(binary_data, 256)

# DISABLED:     def conditional_entropy_order1(self, binary_data: bytes) -> float:
        """Calculate first-order conditional entropy H(X|X-1)."""
# DISABLED:         if len(binary_data) < 2:
# DISABLED:             return 0.0

        # Count transitions from byte to byte
# DISABLED:         transitions = [[0] * 256 for _ in range(256)]
# DISABLED:         for i in range(1, len(binary_data)):
# DISABLED:             prev_byte = binary_data[i - 1]
# DISABLED:             curr_byte = binary_data[i]
# DISABLED:             transitions[prev_byte][curr_byte] += 1

        # Calculate conditional entropy
# DISABLED:         conditional_entropy = 0.0
# DISABLED:         total_transitions = len(binary_data) - 1

# DISABLED:         for prev_byte in range(256):
# DISABLED:             row_transitions = sum(transitions[prev_byte])
# DISABLED:             if row_transitions > 0:
# DISABLED:                 row_entropy = 0.0
# DISABLED:                 for curr_byte in range(256):
# DISABLED:                     if transitions[prev_byte][curr_byte] > 0:
# DISABLED:                         probability = transitions[prev_byte][curr_byte] / row_transitions
# DISABLED:                         row_entropy -= probability * math.log2(probability)
# DISABLED:                 conditional_entropy += (row_transitions / total_transitions) * row_entropy

# DISABLED:         return conditional_entropy

# DISABLED:     def conditional_entropy_order2(self, binary_data: bytes) -> float:
        """Calculate second-order conditional entropy H(X|X-1,X-2)."""
# DISABLED:         if len(binary_data) < 3:
# DISABLED:             return 0.0

        # Count transitions from byte pairs to byte
# DISABLED:         transitions = {}
# DISABLED:         for i in range(2, len(binary_data)):
# DISABLED:             prev_pair = (binary_data[i - 2], binary_data[i - 1])
# DISABLED:             curr_byte = binary_data[i]
# DISABLED:             if prev_pair not in transitions:
# DISABLED:                 transitions[prev_pair] = [0] * 256
# DISABLED:             transitions[prev_pair][curr_byte] += 1

        # Calculate conditional entropy
# DISABLED:         conditional_entropy = 0.0
# DISABLED:         total_transitions = len(binary_data) - 2

# DISABLED:         for prev_pair, counts in transitions.items():
# DISABLED:             row_transitions = sum(counts)
# DISABLED:             if row_transitions > 0:
# DISABLED:                 row_entropy = 0.0
# DISABLED:                 for curr_byte in range(256):
# DISABLED:                     if counts[curr_byte] > 0:
# DISABLED:                         probability = counts[curr_byte] / row_transitions
# DISABLED:                         row_entropy -= probability * math.log2(probability)
# DISABLED:                 conditional_entropy += (row_transitions / total_transitions) * row_entropy

# DISABLED:         return conditional_entropy

# DISABLED:     def entropy_variance(self, binary_data: bytes) -> float:
        """Calculate variance of entropy across windows."""
# DISABLED:         window_size = min(256, max(16, len(binary_data) // 100))
# DISABLED:         if len(binary_data) < window_size * 2:
# DISABLED:             return 0.0

# DISABLED:         entropies = []
# DISABLED:         for i in range(0, len(binary_data) - window_size + 1, window_size // 2):
# DISABLED:             window = binary_data[i:i + window_size]
# DISABLED:             entropy = self.shannon_entropy_global(window)
# DISABLED:             entropies.append(entropy)

# DISABLED:         if len(entropies) < 2:
# DISABLED:             return 0.0

# DISABLED:         mean_entropy = sum(entropies) / len(entropies)
# DISABLED:         variance = sum((e - mean_entropy) ** 2 for e in entropies) / len(entropies)
# DISABLED:         return variance

# DISABLED:     def entropy_gradient(self, binary_data: bytes) -> float:
        """Calculate average entropy gradient magnitude."""
# DISABLED:         window_size = min(256, max(16, len(binary_data) // 100))
# DISABLED:         if len(binary_data) < window_size * 3:
# DISABLED:             return 0.0

# DISABLED:         entropies = []
# DISABLED:         for i in range(0, len(binary_data) - window_size + 1, window_size // 2):
# DISABLED:             window = binary_data[i:i + window_size]
# DISABLED:             entropy = self.shannon_entropy_global(window)
# DISABLED:             entropies.append(entropy)

# DISABLED:         if len(entropies) < 3:
# DISABLED:             return 0.0

        # Calculate gradients
# DISABLED:         gradients = []
# DISABLED:         for i in range(1, len(entropies)):
# DISABLED:             gradient = abs(entropies[i] - entropies[i - 1])
# DISABLED:             gradients.append(gradient)

# DISABLED:         return sum(gradients) / len(gradients) if gradients else 0.0

# DISABLED:     def relative_entropy(self, binary_data: bytes) -> float:
        """Calculate entropy relative to maximum possible (8 bits/byte)."""
# DISABLED:         max_entropy = 8.0
# DISABLED:         actual_entropy = self.shannon_entropy_global(binary_data)
# DISABLED:         return actual_entropy / max_entropy

# DISABLED:     def entropy_efficiency(self, binary_data: bytes) -> float:
        """Calculate efficiency of entropy distribution."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Calculate byte frequency distribution
# DISABLED:         frequency = [0] * 256
# DISABLED:         for byte_val in binary_data:
# DISABLED:             frequency[byte_val] += 1

        # Count non-zero frequencies
# DISABLED:         unique_bytes = sum(1 for count in frequency if count > 0)
# DISABLED:         max_possible_unique = min(256, len(binary_data))

# DISABLED:         if max_possible_unique == 0:
# DISABLED:             return 0.0

        # Efficiency = actual unique / max possible unique
# DISABLED:         efficiency = unique_bytes / max_possible_unique

        # Combine with relative entropy for a more nuanced measure
# DISABLED:         relative_entropy = self.relative_entropy(binary_data)
# DISABLED:         return (efficiency + relative_entropy) / 2