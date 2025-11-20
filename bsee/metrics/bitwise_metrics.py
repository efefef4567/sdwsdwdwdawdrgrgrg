"""
# DISABLED: Bitwise metrics for binary analysis.
"""

# DISABLED: import numpy as np
# DISABLED: from typing import Dict, List


# DISABLED: class BitwiseMetrics:
    """Collection of bitwise metrics."""

# DISABLED:     def __init__(self):
        """Initialize bitwise metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all bitwise metrics."""
# DISABLED:         return {
# DISABLED:             'bit_density_0': self.bit_density_0,
# DISABLED:             'bit_density_1': self.bit_density_1,
# DISABLED:             'bit_density_2': self.bit_density_2,
# DISABLED:             'bit_density_3': self.bit_density_3,
# DISABLED:             'bit_density_4': self.bit_density_4,
# DISABLED:             'bit_density_5': self.bit_density_5,
# DISABLED:             'bit_density_6': self.bit_density_6,
# DISABLED:             'bit_density_7': self.bit_density_7,
# DISABLED:             'bit_entropy': self.bit_entropy,
# DISABLED:             'bit_autocorrelation': self.bit_autocorrelation,
# DISABLED:             'bit_run_density': self.bit_run_density,
# DISABLED:             'alternating_bit_ratio': self.alternating_bit_ratio,
# DISABLED:             'bit_pattern_diversity': self.bit_pattern_diversity,
# DISABLED:             'most_significant_bit_bias': self.most_significant_bit_bias,
# DISABLED:             'least_significant_bit_bias': self.least_significant_bit_bias,
# DISABLED:             'bit_plane_entropy': self.bit_plane_entropy
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'bit_density_0': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 0 (MSB)',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_density_1': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 1',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_density_2': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 2',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_density_3': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 3',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_density_4': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 4',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_density_5': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 5',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_density_6': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 6',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_density_7': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit 7 (LSB)',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_entropy': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Entropy of bit distribution',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_autocorrelation': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Autocorrelation of bit sequence',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_run_density': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Density of bit runs',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'alternating_bit_ratio': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Ratio of alternating bits',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_pattern_diversity': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Diversity of bit patterns',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'most_significant_bit_bias': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Bias in most significant bits',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'least_significant_bit_bias': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Bias in least significant bits',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bit_plane_entropy': {
# DISABLED:                 'category': 'bitwise',
# DISABLED:                 'description': 'Average entropy across bit planes',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def _bytes_to_bits(self, binary_data: bytes) -> List[int]:
        """Convert bytes to list of bits."""
# DISABLED:         bits = []
# DISABLED:         for byte_val in binary_data:
# DISABLED:             for bit_pos in range(8):
# DISABLED:                 bit = (byte_val >> (7 - bit_pos)) & 1
# DISABLED:                 bits.append(bit)
# DISABLED:         return bits

# DISABLED:     def bit_density(self, binary_data: bytes, bit_position: int) -> float:
        """Calculate density of specific bit position."""
# DISABLED:         if not binary_data or bit_position < 0 or bit_position > 7:
# DISABLED:             return 0.0

# DISABLED:         bit_count = 0
# DISABLED:         for byte_val in binary_data:
# DISABLED:             bit = (byte_val >> (7 - bit_position)) & 1
# DISABLED:             bit_count += bit

# DISABLED:         return bit_count / len(binary_data)

# DISABLED:     def bit_density_0(self, binary_data: bytes) -> float:
        """Density of bit 0 (MSB)."""
# DISABLED:         return self.bit_density(binary_data, 0)

# DISABLED:     def bit_density_1(self, binary_data: bytes) -> float:
        """Density of bit 1."""
# DISABLED:         return self.bit_density(binary_data, 1)

# DISABLED:     def bit_density_2(self, binary_data: bytes) -> float:
        """Density of bit 2."""
# DISABLED:         return self.bit_density(binary_data, 2)

# DISABLED:     def bit_density_3(self, binary_data: bytes) -> float:
        """Density of bit 3."""
# DISABLED:         return self.bit_density(binary_data, 3)

# DISABLED:     def bit_density_4(self, binary_data: bytes) -> float:
        """Density of bit 4."""
# DISABLED:         return self.bit_density(binary_data, 4)

# DISABLED:     def bit_density_5(self, binary_data: bytes) -> float:
        """Density of bit 5."""
# DISABLED:         return self.bit_density(binary_data, 5)

# DISABLED:     def bit_density_6(self, binary_data: bytes) -> float:
        """Density of bit 6."""
# DISABLED:         return self.bit_density(binary_data, 6)

# DISABLED:     def bit_density_7(self, binary_data: bytes) -> float:
        """Density of bit 7 (LSB)."""
# DISABLED:         return self.bit_density(binary_data, 7)

# DISABLED:     def bit_entropy(self, binary_data: bytes) -> float:
        """Entropy of bit distribution."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

# DISABLED:         bits = self._bytes_to_bits(binary_data)
# DISABLED:         total_bits = len(bits)

# DISABLED:         if total_bits == 0:
# DISABLED:             return 0.0

        # Count bits
# DISABLED:         ones_count = sum(bits)
# DISABLED:         zeros_count = total_bits - ones_count

# DISABLED:         if ones_count == 0 or zeros_count == 0:
# DISABLED:             return 0.0

        # Calculate entropy
# DISABLED:         import math
# DISABLED:         p_ones = ones_count / total_bits
# DISABLED:         p_zeros = zeros_count / total_bits

# DISABLED:         entropy = -(p_ones * math.log2(p_ones) + p_zeros * math.log2(p_zeros))
# DISABLED:         return entropy

# DISABLED:     def bit_autocorrelation(self, binary_data: bytes) -> float:
        """Autocorrelation of bit sequence."""
# DISABLED:         if len(binary_data) < 2:
# DISABLED:             return 0.0

# DISABLED:         bits = self._bytes_to_bits(binary_data)
# DISABLED:         if len(bits) < 2:
# DISABLED:             return 0.0

        # Calculate autocorrelation at lag 1
# DISABLED:         n = len(bits) - 1
# DISABLED:         matches = sum(1 for i in range(n) if bits[i] == bits[i + 1])

        # Normalize to [-1, 1]
# DISABLED:         autocorr = (2 * matches - n) / n
# DISABLED:         return autocorr

# DISABLED:     def bit_run_density(self, binary_data: bytes) -> float:
        """Density of bit runs."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

# DISABLED:         bits = self._bytes_to_bits(binary_data)
# DISABLED:         if len(bits) < 2:
# DISABLED:             return 0.0

        # Count runs (sequences of consecutive identical bits)
# DISABLED:         runs = 1
# DISABLED:         for i in range(1, len(bits)):
# DISABLED:             if bits[i] != bits[i - 1]:
# DISABLED:                 runs += 1

        # Density = runs / total_bits
# DISABLED:         return runs / len(bits)

# DISABLED:     def alternating_bit_ratio(self, binary_data: bytes) -> float:
        """Ratio of alternating bits."""
# DISABLED:         if len(binary_data) < 2:
# DISABLED:             return 0.0

# DISABLED:         bits = self._bytes_to_bits(binary_data)
# DISABLED:         if len(bits) < 2:
# DISABLED:             return 0.0

        # Count alternating pairs (01 or 10)
# DISABLED:         alternating_pairs = 0
# DISABLED:         for i in range(len(bits) - 1):
# DISABLED:             if bits[i] != bits[i + 1]:
# DISABLED:                 alternating_pairs += 1

# DISABLED:         return alternating_pairs / (len(bits) - 1)

# DISABLED:     def bit_pattern_diversity(self, binary_data: bytes) -> float:
        """Diversity of bit patterns."""
# DISABLED:         if len(binary_data) < 4:
# DISABLED:             return 0.0

        # Count unique 4-bit patterns
# DISABLED:         patterns = set()
# DISABLED:         bits = self._bytes_to_bits(binary_data)

# DISABLED:         for i in range(len(bits) - 3):
# DISABLED:             pattern = tuple(bits[i:i+4])
# DISABLED:             patterns.add(pattern)

# DISABLED:         total_possible_patterns = min(16, len(bits) - 3)
# DISABLED:         diversity = len(patterns) / total_possible_patterns if total_possible_patterns > 0 else 0.0

# DISABLED:         return diversity

# DISABLED:     def most_significant_bit_bias(self, binary_data: bytes) -> float:
        """Bias in most significant bits."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

        # Check bits 0-3 (most significant 4 bits)
# DISABLED:         msb_densities = []
# DISABLED:         for bit_pos in range(4):
# DISABLED:             density = self.bit_density(binary_data, bit_pos)
# DISABLED:             msb_densities.append(density)

        # Calculate bias from uniform (0.5)
# DISABLED:         bias = sum(abs(d - 0.5) for d in msb_densities) / 4
# DISABLED:         return bias

# DISABLED:     def least_significant_bit_bias(self, binary_data: bytes) -> float:
        """Bias in least significant bits."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

        # Check bits 4-7 (least significant 4 bits)
# DISABLED:         lsb_densities = []
# DISABLED:         for bit_pos in range(4, 8):
# DISABLED:             density = self.bit_density(binary_data, bit_pos)
# DISABLED:             lsb_densities.append(density)

        # Calculate bias from uniform (0.5)
# DISABLED:         bias = sum(abs(d - 0.5) for d in lsb_densities) / 4
# DISABLED:         return bias

# DISABLED:     def bit_plane_entropy(self, binary_data: bytes) -> float:
        """Average entropy across bit planes."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

# DISABLED:         entropies = []
# DISABLED:         for bit_pos in range(8):
            # Extract bit plane
# DISABLED:             bit_plane = []
# DISABLED:             for byte_val in binary_data:
# DISABLED:                 bit = (byte_val >> (7 - bit_pos)) & 1
# DISABLED:                 bit_plane.append(bit)

            # Calculate entropy of this bit plane
# DISABLED:             if bit_plane:
# DISABLED:                 ones_count = sum(bit_plane)
# DISABLED:                 zeros_count = len(bit_plane) - ones_count

# DISABLED:                 if ones_count > 0 and zeros_count > 0:
# DISABLED:                     import math
# DISABLED:                     p_ones = ones_count / len(bit_plane)
# DISABLED:                     p_zeros = zeros_count / len(bit_plane)
# DISABLED:                     entropy = -(p_ones * math.log2(p_ones) + p_zeros * math.log2(p_zeros))
# DISABLED:                     entropies.append(entropy)
# DISABLED:                 else:
# DISABLED:                     entropies.append(0.0)
# DISABLED:             else:
# DISABLED:                 entropies.append(0.0)

# DISABLED:         return sum(entropies) / len(entropies) if entropies else 0.0