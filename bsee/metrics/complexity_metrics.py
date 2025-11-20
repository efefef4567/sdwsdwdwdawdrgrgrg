"""
# DISABLED: Complexity metrics for binary analysis.
"""

# DISABLED: import zlib
# DISABLED: from typing import Dict, List


# DISABLED: class ComplexityMetrics:
    """Collection of complexity-based metrics."""

# DISABLED:     def __init__(self):
        """Initialize complexity metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all complexity metrics."""
# DISABLED:         return {
# DISABLED:             'kolmogorov_complexity_estimate': self.kolmogorov_complexity_estimate,
# DISABLED:             'lz_complexity': self.lz_complexity,
# DISABLED:             'lempel_ziv_complexity': self.lempel_ziv_complexity,
# DISABLED:             'algorithmic_complexity': self.algorithmic_complexity,
# DISABLED:             'compression_ratio_complexity': self.compression_ratio_complexity,
# DISABLED:             'entropy_rate': self.entropy_rate,
# DISABLED:             'predictive_complexity': self.predictive_complexity,
# DISABLED:             'normalised_compression_distance': self.normalised_compression_distance
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'kolmogorov_complexity_estimate': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Estimated Kolmogorov complexity',
# DISABLED:                 'range': [0, 'file_size'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'lz_complexity': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Lempel-Ziv complexity',
# DISABLED:                 'range': [0, 'file_size'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'lempel_ziv_complexity': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Lempel-Ziv complexity measure',
# DISABLED:                 'range': [0, 'file_size'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'algorithmic_complexity': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Algorithmic complexity estimate',
# DISABLED:                 'range': [0, 'file_size'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'compression_ratio_complexity': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Complexity based on compression ratio',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'entropy_rate': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Entropy rate of the sequence',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'predictive_complexity': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Complexity based on predictability',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'normalised_compression_distance': {
# DISABLED:                 'category': 'complexity',
# DISABLED:                 'description': 'Normalised compression distance',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def kolmogorov_complexity_estimate(self, binary_data: bytes) -> float:
        """Estimated Kolmogorov complexity using compression."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Use compression as an approximation of Kolmogorov complexity
# DISABLED:         compressed = zlib.compress(binary_data, level=9)
# DISABLED:         complexity = len(compressed)

        # Normalize by original size
# DISABLED:         normalized_complexity = complexity / len(binary_data)
# DISABLED:         return normalized_complexity

# DISABLED:     def lz_complexity(self, binary_data: bytes) -> float:
        """Lempel-Ziv complexity."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Simple LZ complexity implementation
# DISABLED:         n = len(binary_data)
# DISABLED:         complexity = 0
# DISABLED:         i = 0

# DISABLED:         while i < n:
            # Find longest prefix not seen before
# DISABLED:             max_length = 0
# DISABLED:             for j in range(1, n - i + 1):
# DISABLED:                 substring = binary_data[i:i + j]
# DISABLED:                 if substring in binary_data[:i]:
# DISABLED:                     max_length = j
# DISABLED:                 else:
# DISABLED:                     break

# DISABLED:             if max_length > 0:
# DISABLED:                 i += max_length
# DISABLED:             else:
# DISABLED:                 i += 1
# DISABLED:             complexity += 1

        # Normalize by n
# DISABLED:         return complexity / n if n > 0 else 0.0

# DISABLED:     def lempel_ziv_complexity(self, binary_data: bytes) -> float:
        """Lempel-Ziv complexity measure."""
# DISABLED:         return self.lz_complexity(binary_data)

# DISABLED:     def algorithmic_complexity(self, binary_data: bytes) -> float:
        """Algorithmic complexity estimate."""
        # Combine multiple complexity measures
# DISABLED:         kolmogorov = self.kolmogorov_complexity_estimate(binary_data)
# DISABLED:         lz = self.lz_complexity(binary_data)

        # Weighted average
# DISABLED:         complexity = (kolmogorov * 0.6 + lz * 0.4)
# DISABLED:         return complexity

# DISABLED:     def compression_ratio_complexity(self, binary_data: bytes) -> float:
        """Complexity based on compression ratio."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

# DISABLED:         compressed = zlib.compress(binary_data)
# DISABLED:         compression_ratio = len(compressed) / len(binary_data)

        # Higher compression ratio indicates lower complexity
# DISABLED:         complexity = compression_ratio
# DISABLED:         return complexity

# DISABLED:     def entropy_rate(self, binary_data: bytes) -> float:
        """Entropy rate of the sequence."""
# DISABLED:         if len(binary_data) < 2:
# DISABLED:             return 0.0

        # Calculate conditional entropy
# DISABLED:         from bsee.metrics.entropy_metrics import EntropyMetrics
# DISABLED:         entropy_metrics = EntropyMetrics()

# DISABLED:         conditional_entropy = entropy_metrics.conditional_entropy_order1(binary_data)
# DISABLED:         return conditional_entropy

# DISABLED:     def predictive_complexity(self, binary_data: bytes) -> float:
        """Complexity based on predictability."""
# DISABLED:         if len(binary_data) < 8:
# DISABLED:             return 1.0  # Maximum complexity for very small data

        # Use simple predictability test
# DISABLED:         correct_predictions = 0
# DISABLED:         total_predictions = 0

# DISABLED:         for i in range(1, len(binary_data)):
            # Predict next byte based on previous byte
# DISABLED:             predicted = binary_data[i - 1]
# DISABLED:             actual = binary_data[i]

# DISABLED:             if predicted == actual:
# DISABLED:                 correct_predictions += 1
# DISABLED:             total_predictions += 1

        # Predictability = correct / total
# DISABLED:         predictability = correct_predictions / total_predictions if total_predictions > 0 else 0.0

        # Complexity = 1 - predictability
# DISABLED:         complexity = 1.0 - predictability
# DISABLED:         return complexity

# DISABLED:     def normalised_compression_distance(self, binary_data: bytes) -> float:
        """Normalised compression distance."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Compress the data
# DISABLED:         c_x = len(zlib.compress(binary_data))
# DISABLED:         n = len(binary_data)

        # NCD = C(x) / |x|
# DISABLED:         ncd = c_x / n
# DISABLED:         return ncd