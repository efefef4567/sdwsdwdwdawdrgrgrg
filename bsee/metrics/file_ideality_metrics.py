"""
# DISABLED: File Ideality metrics for binary analysis.
"""

# DISABLED: import numpy as np
# DISABLED: from typing import Dict, List, Tuple


# DISABLED: class FileIdealityMetrics:
    """Collection of File Ideality metrics."""

# DISABLED:     def __init__(self):
        """Initialize File Ideality metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all File Ideality metrics."""
# DISABLED:         return {
# DISABLED:             'file_ideality_score': self.file_ideality_score,
# DISABLED:             'bits_in_window_8': self.bits_in_window_8,
# DISABLED:             'bits_in_window_16': self.bits_in_window_16,
# DISABLED:             'bits_in_window_32': self.bits_in_window_32,
# DISABLED:             'bits_in_window_64': self.bits_in_window_64,
# DISABLED:             'bits_in_window_128': self.bits_in_window_128,
# DISABLED:             'bits_in_window_256': self.bits_in_window_256,
# DISABLED:             'bits_in_window_512': self.bits_in_window_512,
# DISABLED:             'bits_in_window_1024': self.bits_in_window_1024,
# DISABLED:             'bits_in_window_2048': self.bits_in_window_2048,
# DISABLED:             'average_ideal_window_size': self.average_ideal_window_size,
# DISABLED:             'ideality_efficiency': self.ideality_efficiency,
# DISABLED:             'predictability_score': self.predictability_score
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'file_ideality_score': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Overall File Ideality score (0-1)',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_8': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 8-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_16': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 16-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_32': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 32-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_64': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 64-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_128': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 128-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_256': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 256-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_512': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 512-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_1024': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 1024-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'bits_in_window_2048': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Number of bits predictable with 2048-bit context',
# DISABLED:                 'range': [0, 'total_bits'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'average_ideal_window_size': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Average ideal window size for predictable bits',
# DISABLED:                 'range': [0, 'max_window'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'ideality_efficiency': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Efficiency of File Ideality distribution',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'predictability_score': {
# DISABLED:                 'category': 'file_ideality',
# DISABLED:                 'description': 'Overall predictability score',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def file_ideality_score(self, binary_data: bytes) -> float:
        """Calculate overall File Ideality score."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Window sizes to test
# DISABLED:         window_sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

        # Convert bytes to bits
# DISABLED:         total_bits = len(binary_data) * 8
# DISABLED:         classified_bits = 0

        # Analyze each bit position
# DISABLED:         for bit_pos in range(total_bits):
# DISABLED:             ideal_windows = []

            # Test each window size
# DISABLED:             for window_size in window_sizes:
# DISABLED:                 if self._is_bit_predictable(binary_data, bit_pos, window_size):
# DISABLED:                     ideal_windows.append(window_size)

            # Assign to largest ideal window (exclusive assignment rule)
# DISABLED:             if ideal_windows:
# DISABLED:                 classified_bits += 1

        # Calculate ideality score
# DISABLED:         file_ideality_score = classified_bits / total_bits
# DISABLED:         return file_ideality_score

# DISABLED:     def _is_bit_predictable(self, binary_data: bytes, bit_position: int, window_size: int) -> bool:
        """Check if a bit is predictable from its context window."""
# DISABLED:         if window_size <= 0 or window_size > bit_position:
# DISABLED:             return False

        # Get the bit value
# DISABLED:         byte_pos = bit_position // 8
# DISABLED:         bit_in_byte = bit_position % 8
# DISABLED:         bit_value = (binary_data[byte_pos] >> (7 - bit_in_byte)) & 1

        # Extract context window
# DISABLED:         context = self._extract_context(binary_data, bit_position, window_size)

        # Find similar contexts and check predictability
# DISABLED:         threshold = 0.8  # 80% predictability threshold
# DISABLED:         predictability = self._calculate_predictability(bit_value, context, binary_data)
# DISABLED:         return predictability >= threshold

# DISABLED:     def _extract_context(self, binary_data: bytes, bit_position: int, window_size: int) -> str:
        """Extract context window around a bit position."""
        # Get window_size bits before the current bit
# DISABLED:         start_bit = max(0, bit_position - window_size)
# DISABLED:         context_bits = []

# DISABLED:         for bit_pos in range(start_bit, bit_position):
# DISABLED:             byte_pos = bit_pos // 8
# DISABLED:             bit_in_byte = bit_pos % 8
# DISABLED:             bit_value = (binary_data[byte_pos] >> (7 - bit_in_byte)) & 1
# DISABLED:             context_bits.append(str(bit_value))

# DISABLED:         return ''.join(context_bits)

# DISABLED:     def _calculate_predictability(self, bit_value: int, context: str, binary_data: bytes) -> float:
        """Calculate predictability of a bit given its context."""
# DISABLED:         if len(context) == 0:
# DISABLED:             return 0.0

        # Find all occurrences of this context in the binary data
# DISABLED:         matches = 0
# DISABLED:         correct_predictions = 0

        # Convert binary data to bit string for easier searching
# DISABLED:         bit_string = ''.join(
# DISABLED:             str((byte_val >> (7 - bit_pos)) & 1)
# DISABLED:             for byte_val in binary_data
# DISABLED:             for bit_pos in range(8)
# DISABLED:         )

        # Search for context pattern
# DISABLED:         context_len = len(context)
# DISABLED:         for i in range(len(bit_string) - context_len):
# DISABLED:             if bit_string[i:i + context_len] == context:
# DISABLED:                 matches += 1
                # Check if next bit matches our target bit value
# DISABLED:                 next_bit_pos = i + context_len
# DISABLED:                 if next_bit_pos < len(bit_string):
# DISABLED:                     actual_next_bit = int(bit_string[next_bit_pos])
# DISABLED:                     if actual_next_bit == bit_value:
# DISABLED:                         correct_predictions += 1

        # Calculate predictability
# DISABLED:         if matches == 0:
# DISABLED:             return 0.0

# DISABLED:         return correct_predictions / matches

# DISABLED:     def bits_in_window(self, binary_data: bytes, window_size: int) -> int:
        """Count bits predictable with specified window size."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0

# DISABLED:         total_bits = len(binary_data) * 8
# DISABLED:         predictable_bits = 0

# DISABLED:         for bit_pos in range(total_bits):
# DISABLED:             if self._is_bit_predictable(binary_data, bit_pos, window_size):
# DISABLED:                 predictable_bits += 1

# DISABLED:         return predictable_bits

# DISABLED:     def bits_in_window_8(self, binary_data: bytes) -> int:
        """Number of bits predictable with 8-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 8)

# DISABLED:     def bits_in_window_16(self, binary_data: bytes) -> int:
        """Number of bits predictable with 16-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 16)

# DISABLED:     def bits_in_window_32(self, binary_data: bytes) -> int:
        """Number of bits predictable with 32-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 32)

# DISABLED:     def bits_in_window_64(self, binary_data: bytes) -> int:
        """Number of bits predictable with 64-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 64)

# DISABLED:     def bits_in_window_128(self, binary_data: bytes) -> int:
        """Number of bits predictable with 128-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 128)

# DISABLED:     def bits_in_window_256(self, binary_data: bytes) -> int:
        """Number of bits predictable with 256-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 256)

# DISABLED:     def bits_in_window_512(self, binary_data: bytes) -> int:
        """Number of bits predictable with 512-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 512)

# DISABLED:     def bits_in_window_1024(self, binary_data: bytes) -> int:
        """Number of bits predictable with 1024-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 1024)

# DISABLED:     def bits_in_window_2048(self, binary_data: bytes) -> int:
        """Number of bits predictable with 2048-bit context."""
# DISABLED:         return self.bits_in_window(binary_data, 2048)

# DISABLED:     def average_ideal_window_size(self, binary_data: bytes) -> float:
        """Calculate average ideal window size for predictable bits."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

# DISABLED:         window_sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
# DISABLED:         total_bits = len(binary_data) * 8
# DISABLED:         total_window_size = 0
# DISABLED:         classified_bits = 0

# DISABLED:         for bit_pos in range(total_bits):
# DISABLED:             ideal_windows = []

# DISABLED:             for window_size in window_sizes:
# DISABLED:                 if self._is_bit_predictable(binary_data, bit_pos, window_size):
# DISABLED:                     ideal_windows.append(window_size)

# DISABLED:             if ideal_windows:
                # Assign to largest ideal window
# DISABLED:                 largest_window = max(ideal_windows)
# DISABLED:                 total_window_size += largest_window
# DISABLED:                 classified_bits += 1

# DISABLED:         return total_window_size / classified_bits if classified_bits > 0 else 0.0

# DISABLED:     def ideality_efficiency(self, binary_data: bytes) -> float:
        """Calculate efficiency of File Ideality distribution."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Calculate distribution of bits across window sizes
# DISABLED:         window_counts = {}
# DISABLED:         total_classified = 0

# DISABLED:         window_sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
# DISABLED:         total_bits = len(binary_data) * 8

# DISABLED:         for bit_pos in range(total_bits):
# DISABLED:             ideal_windows = []

# DISABLED:             for window_size in window_sizes:
# DISABLED:                 if self._is_bit_predictable(binary_data, bit_pos, window_size):
# DISABLED:                     ideal_windows.append(window_size)

# DISABLED:             if ideal_windows:
                # Assign to largest ideal window
# DISABLED:                 largest_window = max(ideal_windows)
# DISABLED:                 window_counts[largest_window] = window_counts.get(largest_window, 0) + 1
# DISABLED:                 total_classified += 1

# DISABLED:         if total_classified == 0:
# DISABLED:             return 0.0

        # Calculate entropy of window size distribution
# DISABLED:         import math
# DISABLED:         entropy = 0.0
# DISABLED:         for count in window_counts.values():
# DISABLED:             if count > 0:
# DISABLED:                 probability = count / total_classified
# DISABLED:                 entropy -= probability * math.log2(probability)

        # Maximum possible entropy with 10 window sizes
# DISABLED:         max_entropy = math.log2(len(window_sizes))

        # Efficiency = actual entropy / max entropy
# DISABLED:         efficiency = entropy / max_entropy if max_entropy > 0 else 0.0

        # Combine with overall ideality score
# DISABLED:         overall_score = self.file_ideality_score(binary_data)
# DISABLED:         return (efficiency + overall_score) / 2

# DISABLED:     def predictability_score(self, binary_data: bytes) -> float:
        """Calculate overall predictability score."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Calculate predictability for different window sizes
# DISABLED:         window_sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
# DISABLED:         predictability_scores = []

# DISABLED:         for window_size in window_sizes:
# DISABLED:             predictable_bits = self.bits_in_window(binary_data, window_size)
# DISABLED:             total_bits = len(binary_data) * 8
# DISABLED:             if total_bits > 0:
# DISABLED:                 score = predictable_bits / total_bits
# DISABLED:                 predictability_scores.append(score)

        # Return average predictability across all window sizes
# DISABLED:         return sum(predictability_scores) / len(predictability_scores) if predictability_scores else 0.0