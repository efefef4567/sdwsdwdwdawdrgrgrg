"""
# DISABLED: Run-length metrics for binary analysis.
"""

# DISABLED: from typing import Dict, List


# DISABLED: class RunLengthMetrics:
    """Collection of run-length based metrics."""

# DISABLED:     def __init__(self):
        """Initialize run-length metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all run-length metrics."""
# DISABLED:         return {
# DISABLED:             'run_count_total': self.run_count_total,
# DISABLED:             'average_run_length': self.average_run_length,
# DISABLED:             'max_run_length': self.max_run_length,
# DISABLED:             'run_length_variance': self.run_length_variance,
# DISABLED:             'run_length_entropy': self.run_length_entropy,
# DISABLED:             'homogeneity_index': self.homogeneity_index,
# DISABLED:             'run_efficiency': self.run_efficiency,
# DISABLED:             'compression_potential': self.compression_potential
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'run_count_total': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Total number of runs',
# DISABLED:                 'range': [0, 'file_size'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'average_run_length': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Average length of runs',
# DISABLED:                 'range': [1, 'file_size'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'max_run_length': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Maximum run length',
# DISABLED:                 'range': [1, 'file_size'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'run_length_variance': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Variance of run lengths',
# DISABLED:                 'range': [0, 'file_size²'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'run_length_entropy': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Entropy of run length distribution',
# DISABLED:                 'range': [0, 'log2(max_run_length)'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'homogeneity_index': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Index of data homogeneity',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'run_efficiency': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Efficiency of run structure',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'compression_potential': {
# DISABLED:                 'category': 'runlength',
# DISABLED:                 'description': 'Potential for run-length compression',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def _analyze_runs(self, binary_data: bytes) -> List[int]:
        """Analyze runs in binary data."""
# DISABLED:         if not binary_data:
# DISABLED:             return []

# DISABLED:         runs = []
# DISABLED:         current_value = binary_data[0]
# DISABLED:         current_length = 1

# DISABLED:         for i in range(1, len(binary_data)):
# DISABLED:             if binary_data[i] == current_value:
# DISABLED:                 current_length += 1
# DISABLED:             else:
# DISABLED:                 runs.append(current_length)
# DISABLED:                 current_value = binary_data[i]
# DISABLED:                 current_length = 1

# DISABLED:         runs.append(current_length)  # Add last run
# DISABLED:         return runs

# DISABLED:     def run_count_total(self, binary_data: bytes) -> float:
        """Total number of runs."""
# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         return float(len(runs))

# DISABLED:     def average_run_length(self, binary_data: bytes) -> float:
        """Average length of runs."""
# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         if not runs:
# DISABLED:             return 0.0
# DISABLED:         return sum(runs) / len(runs)

# DISABLED:     def max_run_length(self, binary_data: bytes) -> float:
        """Maximum run length."""
# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         return float(max(runs)) if runs else 0.0

# DISABLED:     def run_length_variance(self, binary_data: bytes) -> float:
        """Variance of run lengths."""
# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         if len(runs) < 2:
# DISABLED:             return 0.0

# DISABLED:         mean_length = sum(runs) / len(runs)
# DISABLED:         variance = sum((length - mean_length) ** 2 for length in runs) / len(runs)
# DISABLED:         return variance

# DISABLED:     def run_length_entropy(self, binary_data: bytes) -> float:
        """Entropy of run length distribution."""
# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         if not runs:
# DISABLED:             return 0.0

        # Count frequency of each run length
# DISABLED:         from collections import Counter
# DISABLED:         run_counts = Counter(runs)
# DISABLED:         total_runs = len(runs)

        # Calculate entropy
# DISABLED:         import math
# DISABLED:         entropy = 0.0
# DISABLED:         for count in run_counts.values():
# DISABLED:             probability = count / total_runs
# DISABLED:             entropy -= probability * math.log2(probability)

# DISABLED:         return entropy

# DISABLED:     def homogeneity_index(self, binary_data: bytes) -> float:
        """Index of data homogeneity."""
# DISABLED:         if not binary_data:
# DISABLED:             return 0.0

# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         total_bytes = len(binary_data)
# DISABLED:         max_possible_runs = total_bytes  # Alternating bytes
# DISABLED:         actual_runs = len(runs)

        # Homogeneity = 1 - (actual_runs / max_possible_runs)
# DISABLED:         homogeneity = 1.0 - (actual_runs / max_possible_runs)
# DISABLED:         return max(0.0, homogeneity)

# DISABLED:     def run_efficiency(self, binary_data: bytes) -> float:
        """Efficiency of run structure."""
# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         if not runs:
# DISABLED:             return 0.0

        # Efficiency based on average run length relative to maximum
# DISABLED:         max_run = max(runs)
# DISABLED:         avg_run = sum(runs) / len(runs)

# DISABLED:         efficiency = avg_run / max_run if max_run > 0 else 0.0
# DISABLED:         return efficiency

# DISABLED:     def compression_potential(self, binary_data: bytes) -> float:
        """Potential for run-length compression."""
# DISABLED:         runs = self._analyze_runs(binary_data)
# DISABLED:         if not runs:
# DISABLED:             return 0.0

        # Estimate compression ratio if run-length encoded
        # Each run needs: count byte + value byte = 2 bytes minimum
# DISABLED:         compressed_size = len(runs) * 2  # Simplified
# DISABLED:         original_size = len(binary_data)

# DISABLED:         compression_ratio = compressed_size / original_size if original_size > 0 else 1.0
# DISABLED:         potential = max(0.0, 1.0 - compression_ratio)

# DISABLED:         return potential