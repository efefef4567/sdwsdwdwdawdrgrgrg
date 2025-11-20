"""
# DISABLED: Statistical metrics for binary analysis.
"""

# DISABLED: import math
# DISABLED: import numpy as np
# DISABLED: from typing import Dict, List, Any, Callable
# DISABLED: from collections import Counter
# DISABLED: from scipy import stats


# DISABLED: class StatisticalMetrics:
    """Collection of statistical metrics."""

# DISABLED:     def __init__(self):
        """Initialize statistical metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, Callable]:
        """Create all statistical metrics."""
# DISABLED:         return {
# DISABLED:             'chi_square_uniformity': self.chi_square_uniformity,
# DISABLED:             'chi_square_p_value': self.chi_square_p_value,
# DISABLED:             'mean_byte_value': self.mean_byte_value,
# DISABLED:             'median_byte_value': self.median_byte_value,
# DISABLED:             'std_deviation': self.std_deviation,
# DISABLED:             'skewness': self.skewness,
# DISABLED:             'kurtosis': self.kurtosis,
# DISABLED:             'byte_range': self.byte_range,
# DISABLED:             'interquartile_range': self.interquartile_range,
# DISABLED:             'coefficient_of_variation': self.coefficient_of_variation,
# DISABLED:             'kl_divergence_uniform': self.kl_divergence_uniform,
# DISABLED:             'js_divergence_uniform': self.js_divergence_uniform,
# DISABLED:             'moment1': self.moment1,
# DISABLED:             'moment2': self.moment2,
# DISABLED:             'moment3': self.moment3,
# DISABLED:             'moment4': self.moment4
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, Callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, Any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'chi_square_uniformity': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Chi-square test for uniformity',
# DISABLED:                 'range': [0, 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'chi_square_p_value': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'P-value from chi-square test',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'mean_byte_value': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Mean of byte values',
# DISABLED:                 'range': [0, 255],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'median_byte_value': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Median of byte values',
# DISABLED:                 'range': [0, 255],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'std_deviation': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Standard deviation of byte values',
# DISABLED:                 'range': [0, 255],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'skewness': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Skewness of byte distribution',
# DISABLED:                 'range': ['-inf', 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'kurtosis': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Kurtosis of byte distribution',
# DISABLED:                 'range': ['-inf', 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'byte_range': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Range of byte values',
# DISABLED:                 'range': [0, 255],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'interquartile_range': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Interquartile range',
# DISABLED:                 'range': [0, 255],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'coefficient_of_variation': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Coefficient of variation',
# DISABLED:                 'range': [0, 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'kl_divergence_uniform': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'KL divergence from uniform distribution',
# DISABLED:                 'range': [0, 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'js_divergence_uniform': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Jensen-Shannon divergence from uniform',
# DISABLED:                 'range': [0, 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'moment1': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'First central moment',
# DISABLED:                 'range': ['-inf', 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'moment2': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Second central moment (variance)',
# DISABLED:                 'range': [0, 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'moment3': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Third central moment',
# DISABLED:                 'range': ['-inf', 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'moment4': {
# DISABLED:                 'category': 'statistical',
# DISABLED:                 'description': 'Fourth central moment',
# DISABLED:                 'range': [0, 'inf'],
# DISABLED:                 'higher_better': False
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def chi_square_uniformity(self, binary_data: bytes) -> float:
        """Chi-square test for uniformity."""
# DISABLED:         if len(binary_data) < 10:
# DISABLED:             return 0.0

        # Count byte frequencies
# DISABLED:         counts = Counter(binary_data)
# DISABLED:         expected_count = len(binary_data) / 256.0

        # Calculate chi-square statistic
# DISABLED:         chi_square = 0.0
# DISABLED:         for byte_val in range(256):
# DISABLED:             observed = counts.get(byte_val, 0)
# DISABLED:             expected = expected_count
# DISABLED:             if expected > 0:
# DISABLED:                 chi_square += ((observed - expected) ** 2) / expected

# DISABLED:         return chi_square

# DISABLED:     def chi_square_p_value(self, binary_data: bytes) -> float:
        """P-value from chi-square test."""
# DISABLED:         chi_square = self.chi_square_uniformity(binary_data)

# DISABLED:         try:
            # Degrees of freedom = 256 - 1 = 255
# DISABLED:             p_value = 1.0 - stats.chi2.cdf(chi_square, 255)
# DISABLED:             return p_value
# DISABLED:         except Exception:
# DISABLED:             return 0.5  # Default value if calculation fails

# DISABLED:     def mean_byte_value(self, binary_data: bytes) -> float:
        """Mean of byte values."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0
# DISABLED:         return sum(binary_data) / len(binary_data)

# DISABLED:     def median_byte_value(self, binary_data: bytes) -> float:
        """Median of byte values."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

# DISABLED:         sorted_bytes = sorted(binary_data)
# DISABLED:         n = len(sorted_bytes)

# DISABLED:         if n % 2 == 0:
# DISABLED:             return (sorted_bytes[n//2 - 1] + sorted_bytes[n//2]) / 2.0
# DISABLED:         else:
# DISABLED:             return float(sorted_bytes[n//2])

# DISABLED:     def std_deviation(self, binary_data: bytes) -> float:
        """Standard deviation of byte values."""
# DISABLED:         if len(binary_data) < 2:
# DISABLED:             return 0.0

# DISABLED:         mean = self.mean_byte_value(binary_data)
# DISABLED:         variance = sum((byte_val - mean) ** 2 for byte_val in binary_data) / len(binary_data)
# DISABLED:         return math.sqrt(variance)

# DISABLED:     def skewness(self, binary_data: bytes) -> float:
        """Skewness of byte distribution."""
# DISABLED:         if len(binary_data) < 3:
# DISABLED:             return 0.0

# DISABLED:         mean = self.mean_byte_value(binary_data)
# DISABLED:         std_dev = self.std_deviation(binary_data)

# DISABLED:         if std_dev == 0:
# DISABLED:             return 0.0

        # Calculate third standardized moment
# DISABLED:         third_moment = sum((byte_val - mean) ** 3 for byte_val in binary_data) / len(binary_data)
# DISABLED:         skewness = third_moment / (std_dev ** 3)

# DISABLED:         return skewness

# DISABLED:     def kurtosis(self, binary_data: bytes) -> float:
        """Kurtosis of byte distribution."""
# DISABLED:         if len(binary_data) < 4:
# DISABLED:             return 0.0

# DISABLED:         mean = self.mean_byte_value(binary_data)
# DISABLED:         std_dev = self.std_deviation(binary_data)

# DISABLED:         if std_dev == 0:
# DISABLED:             return 0.0

        # Calculate fourth standardized moment
# DISABLED:         fourth_moment = sum((byte_val - mean) ** 4 for byte_val in binary_data) / len(binary_data)
# DISABLED:         kurtosis = (fourth_moment / (std_dev ** 4)) - 3  # Excess kurtosis

# DISABLED:         return kurtosis

# DISABLED:     def byte_range(self, binary_data: bytes) -> float:
        """Range of byte values."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

# DISABLED:         min_byte = min(binary_data)
# DISABLED:         max_byte = max(binary_data)
# DISABLED:         return float(max_byte - min_byte)

# DISABLED:     def interquartile_range(self, binary_data: bytes) -> float:
        """Interquartile range."""
# DISABLED:         if len(binary_data) < 4:
# DISABLED:             return 0.0

# DISABLED:         sorted_bytes = sorted(binary_data)
# DISABLED:         n = len(sorted_bytes)

        # Calculate quartiles
# DISABLED:         q1_index = n // 4
# DISABLED:         q3_index = 3 * n // 4

# DISABLED:         q1 = sorted_bytes[q1_index]
# DISABLED:         q3 = sorted_bytes[q3_index]

# DISABLED:         return float(q3 - q1)

# DISABLED:     def coefficient_of_variation(self, binary_data: bytes) -> float:
        """Coefficient of variation."""
# DISABLED:         mean = self.mean_byte_value(binary_data)
# DISABLED:         std_dev = self.std_deviation(binary_data)

# DISABLED:         if mean == 0:
# DISABLED:             return 0.0 if std_dev == 0 else float('inf')

# DISABLED:         return std_dev / mean

# DISABLED:     def kl_divergence_uniform(self, binary_data: bytes) -> float:
        """KL divergence from uniform distribution."""
# DISABLED:         if len(binary_data) < 10:
# DISABLED:             return 0.0

        # Calculate empirical distribution
# DISABLED:         counts = Counter(binary_data)
# DISABLED:         total = len(binary_data)

        # Calculate KL divergence
# DISABLED:         kl_divergence = 0.0
# DISABLED:         uniform_prob = 1.0 / 256.0

# DISABLED:         for byte_val in range(256):
# DISABLED:             empirical_prob = counts.get(byte_val, 0) / total
# DISABLED:             if empirical_prob > 0:
# DISABLED:                 kl_divergence += empirical_prob * math.log2(empirical_prob / uniform_prob)

# DISABLED:         return kl_divergence

# DISABLED:     def js_divergence_uniform(self, binary_data: bytes) -> float:
        """Jensen-Shannon divergence from uniform."""
# DISABLED:         if len(binary_data) < 10:
# DISABLED:             return 0.0

        # Calculate empirical distribution
# DISABLED:         counts = Counter(binary_data)
# DISABLED:         total = len(binary_data)

        # Calculate JS divergence
# DISABLED:         js_divergence = 0.0
# DISABLED:         uniform_prob = 1.0 / 256.0

# DISABLED:         for byte_val in range(256):
# DISABLED:             empirical_prob = counts.get(byte_val, 0) / total
# DISABLED:             mixed_prob = (empirical_prob + uniform_prob) / 2.0

# DISABLED:             if mixed_prob > 0:
# DISABLED:                 if empirical_prob > 0:
# DISABLED:                     js_divergence += empirical_prob * math.log2(empirical_prob / mixed_prob)
# DISABLED:                 js_divergence += uniform_prob * math.log2(uniform_prob / mixed_prob)

# DISABLED:         return js_divergence / 2.0

# DISABLED:     def moment(self, binary_data: bytes, order: int) -> float:
        """Calculate nth central moment."""
# DISABLED:         if len(binary_data) < order + 1:
# DISABLED:             return 0.0

# DISABLED:         mean = self.mean_byte_value(binary_data)
# DISABLED:         moment = sum((byte_val - mean) ** order for byte_val in binary_data) / len(binary_data)
# DISABLED:         return moment

# DISABLED:     def moment1(self, binary_data: bytes) -> float:
        """First central moment (should be 0)."""
# DISABLED:         return self.moment(binary_data, 1)

# DISABLED:     def moment2(self, binary_data: bytes) -> float:
        """Second central moment (variance)."""
# DISABLED:         return self.moment(binary_data, 2)

# DISABLED:     def moment3(self, binary_data: bytes) -> float:
        """Third central moment."""
# DISABLED:         return self.moment(binary_data, 3)

# DISABLED:     def moment4(self, binary_data: bytes) -> float:
        """Fourth central moment."""
# DISABLED:         return self.moment(binary_data, 4)