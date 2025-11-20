"""
# DISABLED: Compression metrics for binary analysis.
"""

# DISABLED: import zlib
# DISABLED: import lzma
# DISABLED: from typing import Dict, List


# DISABLED: class CompressionMetrics:
    """Collection of compression-based metrics."""

# DISABLED:     def __init__(self):
        """Initialize compression metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all compression metrics."""
# DISABLED:         return {
# DISABLED:             'lz77_ratio': self.lz77_ratio,
# DISABLED:             'lzma_ratio': self.lzma_ratio,
# DISABLED:             'zlib_ratio': self.zlib_ratio,
# DISABLED:             'gzip_ratio': self.gzip_ratio,
# DISABLED:             'bz2_ratio': self.bz2_ratio,
# DISABLED:             'compression_efficiency': self.compression_efficiency,
# DISABLED:             'redundancy_score': self.redundancy_score,
# DISABLED:             'compressibility_index': self.compressibility_index,
# DISABLED:             'entropy_compression_gap': self.entropy_compression_gap,
# DISABLED:             'dictionary_size_estimate': self.dictionary_size_estimate,
# DISABLED:             'pattern_repetition_score': self.pattern_repetition_score,
# DISABLED:             'block_compressibility_variance': self.block_compressibility_variance,
# DISABLED:             'adaptive_compressibility': self.adaptive_compressibility,
# DISABLED:             'compression_complexity': self.compression_complexity,
# DISABLED:             'optimal_compression_ratio': self.optimal_compression_ratio
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'lz77_ratio': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'LZ77 compression ratio',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'lzma_ratio': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'LZMA compression ratio',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'zlib_ratio': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Zlib compression ratio',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'gzip_ratio': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Gzip compression ratio',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'bz2_ratio': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Bzip2 compression ratio',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'compression_efficiency': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Overall compression efficiency',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'redundancy_score': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Redundancy score based on compressibility',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'compressibility_index': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Overall compressibility index',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'entropy_compression_gap': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Gap between theoretical entropy and actual compression',
# DISABLED:                 'range': [0, 8],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'dictionary_size_estimate': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Estimated dictionary size for compression',
# DISABLED:                 'range': [0, 'file_size'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'pattern_repetition_score': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Score based on pattern repetition',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'block_compressibility_variance': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Variance of compressibility across blocks',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'adaptive_compressibility': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Adaptive compressibility score',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'compression_complexity': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Complexity of compression patterns',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'optimal_compression_ratio': {
# DISABLED:                 'category': 'compression',
# DISABLED:                 'description': 'Estimated optimal compression ratio',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': False
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def lz77_ratio(self, binary_data: bytes) -> float:
        """Calculate LZ77 compression ratio."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

# DISABLED:         try:
# DISABLED:             compressed = zlib.compress(binary_data, level=6)
# DISABLED:             ratio = len(compressed) / len(binary_data)
# DISABLED:             return ratio
# DISABLED:         except Exception:
# DISABLED:             return 1.0

# DISABLED:     def lzma_ratio(self, binary_data: bytes) -> float:
        """Calculate LZMA compression ratio."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

# DISABLED:         try:
# DISABLED:             compressed = lzma.compress(binary_data)
# DISABLED:             ratio = len(compressed) / len(binary_data)
# DISABLED:             return ratio
# DISABLED:         except Exception:
# DISABLED:             return 1.0

# DISABLED:     def zlib_ratio(self, binary_data: bytes) -> float:
        """Calculate Zlib compression ratio."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

# DISABLED:         try:
# DISABLED:             compressed = zlib.compress(binary_data)
# DISABLED:             ratio = len(compressed) / len(binary_data)
# DISABLED:             return ratio
# DISABLED:         except Exception:
# DISABLED:             return 1.0

# DISABLED:     def gzip_ratio(self, binary_data: bytes) -> float:
        """Calculate Gzip compression ratio."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

# DISABLED:         try:
# DISABLED:             import gzip
# DISABLED:             compressed = gzip.compress(binary_data)
# DISABLED:             ratio = len(compressed) / len(binary_data)
# DISABLED:             return ratio
# DISABLED:         except Exception:
# DISABLED:             return 1.0

# DISABLED:     def bz2_ratio(self, binary_data: bytes) -> float:
        """Calculate Bzip2 compression ratio."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

# DISABLED:         try:
# DISABLED:             import bz2
# DISABLED:             compressed = bz2.compress(binary_data)
# DISABLED:             ratio = len(compressed) / len(binary_data)
# DISABLED:             return ratio
# DISABLED:         except Exception:
# DISABLED:             return 1.0

# DISABLED:     def compression_efficiency(self, binary_data: bytes) -> float:
        """Calculate overall compression efficiency."""
# DISABLED:         ratios = [
# DISABLED:             self.lz77_ratio(binary_data),
# DISABLED:             self.lzma_ratio(binary_data),
# DISABLED:             self.zlib_ratio(binary_data),
# DISABLED:             self.gzip_ratio(binary_data),
# DISABLED:             self.bz2_ratio(binary_data)
# DISABLED:         ]

        # Average compression ratio (lower is better, so invert for efficiency)
# DISABLED:         avg_ratio = sum(ratios) / len(ratios)
# DISABLED:         efficiency = max(0, 1 - avg_ratio)  # Higher efficiency means better compression
# DISABLED:         return efficiency

# DISABLED:     def redundancy_score(self, binary_data: bytes) -> float:
        """Calculate redundancy score based on compressibility."""
        # Use best compression ratio to estimate redundancy
# DISABLED:         best_ratio = min(
# DISABLED:             self.lz77_ratio(binary_data),
# DISABLED:             self.lzma_ratio(binary_data),
# DISABLED:             self.zlib_ratio(binary_data)
# DISABLED:         )

        # Redundancy = 1 - compression ratio
# DISABLED:         redundancy = max(0, 1 - best_ratio)
# DISABLED:         return redundancy

# DISABLED:     def compressibility_index(self, binary_data: bytes) -> float:
        """Calculate overall compressibility index."""
        # Combine multiple compression metrics
# DISABLED:         lz77_score = 1 - self.lz77_ratio(binary_data)
# DISABLED:         lzma_score = 1 - self.lzma_ratio(binary_data)
# DISABLED:         zlib_score = 1 - self.zlib_ratio(binary_data)

        # Weighted average
# DISABLED:         index = (lz77_score * 0.3 + lzma_score * 0.4 + zlib_score * 0.3)
# DISABLED:         return max(0, min(1, index))

# DISABLED:     def entropy_compression_gap(self, binary_data: bytes) -> float:
        """Calculate gap between theoretical entropy and actual compression."""
# DISABLED:         from bsee.metrics.entropy_metrics import EntropyMetrics
# DISABLED:         entropy_metrics = EntropyMetrics()

# DISABLED:         theoretical_entropy = entropy_metrics.shannon_entropy_global(binary_data)
# DISABLED:         actual_compression = self.lzma_ratio(binary_data) * 8  # Convert to bits

# DISABLED:         gap = max(0, actual_compression - theoretical_entropy)
# DISABLED:         return gap

# DISABLED:     def dictionary_size_estimate(self, binary_data: bytes) -> float:
        """Estimate dictionary size for compression."""
# DISABLED:         if len(binary_data) == 0:
# DISABLED:             return 0.0

        # Simple heuristic: count unique byte sequences of different lengths
# DISABLED:         unique_2grams = len(set(binary_data[i:i+2] for i in range(len(binary_data)-1)))
# DISABLED:         unique_4grams = len(set(binary_data[i:i+4] for i in range(len(binary_data)-3)))
# DISABLED:         unique_8grams = len(set(binary_data[i:i+8] for i in range(len(binary_data)-7)))

        # Weighted estimate
# DISABLED:         dict_size = (unique_2grams * 2 + unique_4grams * 4 + unique_8grams * 8) / 3
# DISABLED:         return min(dict_size, len(binary_data) / 2)  # Cap at half file size

# DISABLED:     def pattern_repetition_score(self, binary_data: bytes) -> float:
        """Calculate score based on pattern repetition."""
# DISABLED:         if len(binary_data) < 16:
# DISABLED:             return 0.0

        # Look for repeated patterns
# DISABLED:         pattern_counts = {}
# DISABLED:         for length in [2, 4, 8]:
# DISABLED:             for i in range(len(binary_data) - length):
# DISABLED:                 pattern = binary_data[i:i+length]
# DISABLED:                 pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        # Calculate repetition score
# DISABLED:         total_patterns = sum(pattern_counts.values())
# DISABLED:         unique_patterns = len(pattern_counts)
# DISABLED:         repetition_ratio = (total_patterns - unique_patterns) / total_patterns if total_patterns > 0 else 0

# DISABLED:         return repetition_ratio

# DISABLED:     def block_compressibility_variance(self, binary_data: bytes) -> float:
        """Calculate variance of compressibility across blocks."""
# DISABLED:         if len(binary_data) < 1024:
# DISABLED:             return 0.0

# DISABLED:         block_size = min(1024, len(binary_data) // 10)
# DISABLED:         ratios = []

# DISABLED:         for i in range(0, len(binary_data), block_size):
# DISABLED:             block = binary_data[i:i+block_size]
# DISABLED:             if len(block) >= 64:  # Minimum block size for meaningful compression
# DISABLED:                 ratio = self.lz77_ratio(block)
# DISABLED:                 ratios.append(ratio)

# DISABLED:         if len(ratios) < 2:
# DISABLED:             return 0.0

        # Calculate variance
# DISABLED:         mean_ratio = sum(ratios) / len(ratios)
# DISABLED:         variance = sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios)
# DISABLED:         return variance

# DISABLED:     def adaptive_compressibility(self, binary_data: bytes) -> float:
        """Calculate adaptive compressibility score."""
# DISABLED:         if len(binary_data) < 512:
# DISABLED:             return self.compressibility_index(binary_data)

        # Test compressibility with different block sizes
# DISABLED:         block_sizes = [256, 512, 1024, 2048]
# DISABLED:         scores = []

# DISABLED:         for block_size in block_sizes:
# DISABLED:             if len(binary_data) >= block_size * 2:
# DISABLED:                 block = binary_data[:block_size]
# DISABLED:                 score = 1 - self.lz77_ratio(block)
# DISABLED:                 scores.append(score)

# DISABLED:         return sum(scores) / len(scores) if scores else 0.0

# DISABLED:     def compression_complexity(self, binary_data: bytes) -> float:
        """Calculate complexity of compression patterns."""
# DISABLED:         if len(binary_data) < 256:
# DISABLED:             return 0.0

        # Analyze compression ratio consistency
# DISABLED:         ratios = []
# DISABLED:         chunk_size = min(512, len(binary_data) // 8)

# DISABLED:         for i in range(0, len(binary_data), chunk_size):
# DISABLED:             chunk = binary_data[i:i+chunk_size]
# DISABLED:             if len(chunk) >= 64:
# DISABLED:                 ratio = self.lz77_ratio(chunk)
# DISABLED:                 ratios.append(ratio)

# DISABLED:         if len(ratios) < 2:
# DISABLED:             return 0.0

        # Complex data has inconsistent compression ratios
# DISABLED:         mean_ratio = sum(ratios) / len(ratios)
# DISABLED:         variance = sum((r - mean_ratio) ** 2 for r in ratios) / len(ratios)

        # Normalize to [0,1]
# DISABLED:         complexity = min(1.0, variance / (mean_ratio ** 2 + 0.01))
# DISABLED:         return complexity

# DISABLED:     def optimal_compression_ratio(self, binary_data: bytes) -> float:
        """Estimate optimal compression ratio."""
        # Use the best of available compression methods
# DISABLED:         ratios = [
# DISABLED:             self.lz77_ratio(binary_data),
# DISABLED:             self.lzma_ratio(binary_data),
# DISABLED:             self.zlib_ratio(binary_data),
# DISABLED:             self.gzip_ratio(binary_data),
# DISABLED:             self.bz2_ratio(binary_data)
# DISABLED:         ]

        # Account for potential improvements with better algorithms
# DISABLED:         best_ratio = min(ratios)
# DISABLED:         optimal_ratio = best_ratio * 0.9  # Assume 10% potential improvement

# DISABLED:         return max(0.1, optimal_ratio)  # Minimum 10% compression