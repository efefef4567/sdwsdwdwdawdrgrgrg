"""
# DISABLED: Pattern metrics for binary analysis.
"""

# DISABLED: import numpy as np
# DISABLED: from typing import Dict, List


# DISABLED: class PatternMetrics:
    """Collection of pattern-based metrics."""

# DISABLED:     def __init__(self):
        """Initialize pattern metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all pattern metrics."""
# DISABLED:         return {
# DISABLED:             'autocorrelation_avg': self.autocorrelation_avg,
# DISABLED:             'autocorrelation_lag1': self.autocorrelation_lag1,
# DISABLED:             'autocorrelation_lag2': self.autocorrelation_lag2,
# DISABLED:             'autocorrelation_lag4': self.autocorrelation_lag4,
# DISABLED:             'autocorrelation_lag8': self.autocorrelation_lag8,
# DISABLED:             'autocorrelation_lag16': self.autocorrelation_lag16,
# DISABLED:             'autocorrelation_lag32': self.autocorrelation_lag32,
# DISABLED:             'autocorrelation_lag64': self.autocorrelation_lag64,
# DISABLED:             'autocorrelation_lag128': self.autocorrelation_lag128,
# DISABLED:             'periodicity_score': self.periodicity_score,
# DISABLED:             'dominant_frequency': self.dominant_frequency,
# DISABLED:             'frequency_spectrum_entropy': self.frequency_spectrum_entropy,
# DISABLED:             'pattern_richness': self.pattern_richness,
# DISABLED:             'repetition_factor': self.repetition_factor,
# DISABLED:             'self_similarity': self.self_similarity,
# DISABLED:             'fractal_dimension': self.fractal_dimension,
# DISABLED:             'long_range_correlation': self.long_range_correlation
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'autocorrelation_avg': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Average autocorrelation across lags',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag1': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 1',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag2': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 2',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag4': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 4',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag8': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 8',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag16': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 16',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag32': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 32',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag64': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 64',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'autocorrelation_lag128': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Autocorrelation at lag 128',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'periodicity_score': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Overall periodicity score',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'dominant_frequency': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Dominant frequency in signal',
# DISABLED:                 'range': [0, 'nyquist'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'frequency_spectrum_entropy': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Entropy of frequency spectrum',
# DISABLED:                 'range': [0, 'log2(fft_size)'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'pattern_richness': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Richness of patterns in data',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'repetition_factor': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Factor of pattern repetition',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'self_similarity': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Self-similarity measure',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'fractal_dimension': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Fractal dimension of data',
# DISABLED:                 'range': [1, 2],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'long_range_correlation': {
# DISABLED:                 'category': 'pattern',
# DISABLED:                 'description': 'Long-range correlation coefficient',
# DISABLED:                 'range': [-1, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def autocorrelation_lag(self, binary_data: bytes, lag: int) -> float:
        """Calculate autocorrelation at specific lag."""
# DISABLED:         if len(binary_data) <= lag:
# DISABLED:             return 0.0

        # Convert bytes to values
# DISABLED:         data = np.array(list(binary_data), dtype=float)

        # Calculate mean
# DISABLED:         mean = np.mean(data)

        # Calculate autocorrelation
# DISABLED:         if lag == 0:
# DISABLED:             return 1.0

# DISABLED:         n = len(data) - lag
# DISABLED:         if n <= 0:
# DISABLED:             return 0.0

# DISABLED:         numerator = np.sum((data[:n] - mean) * (data[lag:] - mean))
# DISABLED:         denominator = np.sum((data - mean) ** 2)

# DISABLED:         if denominator == 0:
# DISABLED:             return 0.0

# DISABLED:         return numerator / denominator

# DISABLED:     def autocorrelation_avg(self, binary_data: bytes) -> float:
        """Calculate average autocorrelation across multiple lags."""
# DISABLED:         if len(binary_data) < 2:
# DISABLED:             return 0.0

# DISABLED:         lags = [1, 2, 4, 8, 16, 32, 64, 128]
# DISABLED:         correlations = []

# DISABLED:         for lag in lags:
# DISABLED:             if lag < len(binary_data):
# DISABLED:                 corr = self.autocorrelation_lag(binary_data, lag)
# DISABLED:                 correlations.append(abs(corr))

# DISABLED:         return np.mean(correlations) if correlations else 0.0

# DISABLED:     def autocorrelation_lag1(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 1."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 1)

# DISABLED:     def autocorrelation_lag2(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 2."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 2)

# DISABLED:     def autocorrelation_lag4(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 4."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 4)

# DISABLED:     def autocorrelation_lag8(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 8."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 8)

# DISABLED:     def autocorrelation_lag16(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 16."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 16)

# DISABLED:     def autocorrelation_lag32(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 32."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 32)

# DISABLED:     def autocorrelation_lag64(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 64."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 64)

# DISABLED:     def autocorrelation_lag128(self, binary_data: bytes) -> float:
        """Autocorrelation at lag 128."""
# DISABLED:         return self.autocorrelation_lag(binary_data, 128)

# DISABLED:     def periodicity_score(self, binary_data: bytes) -> float:
        """Calculate overall periodicity score."""
# DISABLED:         if len(binary_data) < 16:
# DISABLED:             return 0.0

        # Calculate autocorrelation for multiple lags
# DISABLED:         correlations = []
# DISABLED:         for lag in range(1, min(64, len(binary_data) // 4)):
# DISABLED:             corr = abs(self.autocorrelation_lag(binary_data, lag))
# DISABLED:             correlations.append(corr)

        # Periodicity score based on peak correlations
# DISABLED:         if not correlations:
# DISABLED:             return 0.0

# DISABLED:         max_corr = max(correlations)
# DISABLED:         mean_corr = np.mean(correlations)

        # Score based on how much peak exceeds mean
# DISABLED:         periodicity = max(0, (max_corr - mean_corr) / (1 - mean_corr + 0.001))
# DISABLED:         return min(1.0, periodicity)

# DISABLED:     def dominant_frequency(self, binary_data: bytes) -> float:
        """Find dominant frequency in signal."""
# DISABLED:         if len(binary_data) < 8:
# DISABLED:             return 0.0

# DISABLED:         try:
            # Convert bytes to signal
# DISABLED:             signal = np.array(list(binary_data), dtype=float)

            # Apply FFT
# DISABLED:             fft = np.fft.fft(signal)
# DISABLED:             freqs = np.fft.fftfreq(len(signal))

            # Find dominant frequency (excluding DC component)
# DISABLED:             magnitude = np.abs(fft[1:len(fft)//2])
# DISABLED:             if len(magnitude) == 0:
# DISABLED:                 return 0.0

# DISABLED:             dominant_idx = np.argmax(magnitude)
# DISABLED:             dominant_freq = abs(freqs[dominant_idx + 1])

# DISABLED:             return dominant_freq
# DISABLED:         except Exception:
# DISABLED:             return 0.0

# DISABLED:     def frequency_spectrum_entropy(self, binary_data: bytes) -> float:
        """Calculate entropy of frequency spectrum."""
# DISABLED:         if len(binary_data) < 8:
# DISABLED:             return 0.0

# DISABLED:         try:
            # Convert bytes to signal
# DISABLED:             signal = np.array(list(binary_data), dtype=float)

            # Apply FFT
# DISABLED:             fft = np.fft.fft(signal)
# DISABLED:             magnitude = np.abs(fft[:len(fft)//2])

            # Normalize
# DISABLED:             if np.sum(magnitude) == 0:
# DISABLED:                 return 0.0

# DISABLED:             magnitude = magnitude / np.sum(magnitude)

            # Calculate entropy
# DISABLED:             entropy = -np.sum(magnitude * np.log2(magnitude + 1e-10))
# DISABLED:             return entropy
# DISABLED:         except Exception:
# DISABLED:             return 0.0

# DISABLED:     def pattern_richness(self, binary_data: bytes) -> float:
        """Calculate richness of patterns in data."""
# DISABLED:         if len(binary_data) < 4:
# DISABLED:             return 0.0

        # Count unique patterns of different lengths
# DISABLED:         pattern_lengths = [2, 4, 8]
# DISABLED:         total_patterns = 0
# DISABLED:         unique_patterns = 0

# DISABLED:         for length in pattern_lengths:
# DISABLED:             if len(binary_data) >= length:
# DISABLED:                 patterns = set()
# DISABLED:                 for i in range(len(binary_data) - length + 1):
# DISABLED:                     pattern = binary_data[i:i+length]
# DISABLED:                     patterns.add(pattern)

# DISABLED:                 total_patterns += len(binary_data) - length + 1
# DISABLED:                 unique_patterns += len(patterns)

# DISABLED:         if total_patterns == 0:
# DISABLED:             return 0.0

# DISABLED:         richness = unique_patterns / total_patterns
# DISABLED:         return richness

# DISABLED:     def repetition_factor(self, binary_data: bytes) -> float:
        """Calculate factor of pattern repetition."""
# DISABLED:         return 1.0 - self.pattern_richness(binary_data)

# DISABLED:     def self_similarity(self, binary_data: bytes) -> float:
        """Calculate self-similarity measure."""
# DISABLED:         if len(binary_data) < 16:
# DISABLED:             return 0.0

        # Compare different parts of the data
# DISABLED:         mid_point = len(binary_data) // 2
# DISABLED:         first_half = binary_data[:mid_point]
# DISABLED:         second_half = binary_data[mid_point:2*mid_point]

# DISABLED:         if len(first_half) != len(second_half):
# DISABLED:             min_len = min(len(first_half), len(second_half))
# DISABLED:             first_half = first_half[:min_len]
# DISABLED:             second_half = second_half[:min_len]

        # Calculate similarity
# DISABLED:         matches = sum(1 for a, b in zip(first_half, second_half) if a == b)
# DISABLED:         similarity = matches / len(first_half) if first_half else 0.0

# DISABLED:         return similarity

# DISABLED:     def fractal_dimension(self, binary_data: bytes) -> float:
        """Estimate fractal dimension of data."""
# DISABLED:         if len(binary_data) < 8:
# DISABLED:             return 1.0

# DISABLED:         try:
            # Convert bytes to signal
# DISABLED:             signal = np.array(list(binary_data), dtype=float)

            # Simple box-counting method
# DISABLED:             scales = [2, 4, 8, 16]
# DISABLED:             counts = []

# DISABLED:             for scale in scales:
# DISABLED:                 if scale < len(signal):
                    # Divide signal into boxes of size scale
# DISABLED:                     num_boxes = len(signal) // scale
# DISABLED:                     if num_boxes > 0:
# DISABLED:                         counts.append(num_boxes)

# DISABLED:             if len(counts) < 2:
# DISABLED:                 return 1.0

            # Estimate dimension from log-log plot
# DISABLED:             log_scales = np.log(scales[:len(counts)])
# DISABLED:             log_counts = np.log(counts)

            # Linear regression to estimate slope (negative fractal dimension)
# DISABLED:             if len(log_scales) >= 2:
# DISABLED:                 slope = np.polyfit(log_scales, log_counts, 1)[0]
# DISABLED:                 dimension = max(1.0, min(2.0, -slope))
# DISABLED:                 return dimension

# DISABLED:             return 1.0
# DISABLED:         except Exception:
# DISABLED:             return 1.0

# DISABLED:     def long_range_correlation(self, binary_data: bytes) -> float:
        """Calculate long-range correlation coefficient."""
# DISABLED:         if len(binary_data) < 32:
# DISABLED:             return 0.0

        # Calculate correlations at long lags
# DISABLED:         long_lags = [len(binary_data)//8, len(binary_data)//4, len(binary_data)//2]
# DISABLED:         correlations = []

# DISABLED:         for lag in long_lags:
# DISABLED:             if lag > 0 and lag < len(binary_data):
# DISABLED:                 corr = self.autocorrelation_lag(binary_data, lag)
# DISABLED:                 correlations.append(corr)

# DISABLED:         return np.mean(correlations) if correlations else 0.0