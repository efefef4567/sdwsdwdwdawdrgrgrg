"""
# DISABLED: Structure metrics for binary analysis.
"""

# DISABLED: import numpy as np
# DISABLED: from typing import Dict, List, Tuple


# DISABLED: class StructureMetrics:
    """Collection of structure-based metrics."""

# DISABLED:     def __init__(self):
        """Initialize structure metrics."""
# DISABLED:         self.metrics = self._create_metrics()

# DISABLED:     def _create_metrics(self) -> Dict[str, callable]:
        """Create all structure metrics."""
# DISABLED:         return {
# DISABLED:             'alignment_score': self.alignment_score,
# DISABLED:             'block_detection_score': self.block_detection_score,
# DISABLED:             'repeating_block_count': self.repeating_block_count,
# DISABLED:             'block_size_variance': self.block_size_variance,
# DISABLED:             'structure_regularity': self.structure_regularity,
# DISABLED:             'segmentation_score': self.segmentation_score,
# DISABLED:             'pattern_coherence': self.pattern_coherence,
# DISABLED:             'hierarchical_structure': self.hierarchical_structure,
# DISABLED:             'byte_alignment_index': self.byte_alignment_index,
# DISABLED:             'structural_entropy': self.structural_entropy
# DISABLED:         }

# DISABLED:     def get_metrics(self) -> Dict[str, callable]:
        """Get all metrics."""
# DISABLED:         return self.metrics

# DISABLED:     def get_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         metadata_map = {
# DISABLED:             'alignment_score': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Score based on byte alignment patterns',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'block_detection_score': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Score for detectable block structures',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'repeating_block_count': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Count of repeating blocks',
# DISABLED:                 'range': [0, 'file_size/block_size'],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'block_size_variance': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Variance of detected block sizes',
# DISABLED:                 'range': [0, 'file_size²'],
# DISABLED:                 'higher_better': False
# DISABLED:             },
# DISABLED:             'structure_regularity': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Regularity of structural patterns',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'segmentation_score': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Score for natural segmentation points',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'pattern_coherence': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Coherence of patterns across segments',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'hierarchical_structure': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Score for hierarchical structure',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'byte_alignment_index': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Index of byte alignment patterns',
# DISABLED:                 'range': [0, 1],
# DISABLED:                 'higher_better': True
# DISABLED:             },
# DISABLED:             'structural_entropy': {
# DISABLED:                 'category': 'structure',
# DISABLED:                 'description': 'Entropy of structural features',
# DISABLED:                 'range': [0, 'log2(n_structures)'],
# DISABLED:                 'higher_better': False
# DISABLED:             }
# DISABLED:         }
# DISABLED:         return metadata_map.get(metric_name, {})

# DISABLED:     def alignment_score(self, binary_data: bytes) -> float:
        """Score based on byte alignment patterns."""
# DISABLED:         if len(binary_data) < 16:
# DISABLED:             return 0.0

        # Check for alignment at common boundaries (4, 8, 16, 32 bytes)
# DISABLED:         alignment_scores = []

# DISABLED:         for alignment in [4, 8, 16, 32]:
# DISABLED:             if len(binary_data) >= alignment * 2:
                # Count aligned positions
# DISABLED:                 aligned_positions = 0
# DISABLED:                 total_positions = len(binary_data) // alignment

# DISABLED:                 for i in range(total_positions):
# DISABLED:                     pos = i * alignment
# DISABLED:                     if pos < len(binary_data):
                        # Check if this position shows alignment characteristics
# DISABLED:                         if self._is_aligned_position(binary_data, pos, alignment):
# DISABLED:                             aligned_positions += 1

# DISABLED:                 score = aligned_positions / total_positions if total_positions > 0 else 0.0
# DISABLED:                 alignment_scores.append(score)

# DISABLED:         return sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.0

# DISABLED:     def _is_aligned_position(self, binary_data: bytes, pos: int, alignment: int) -> bool:
        """Check if a position shows alignment characteristics."""
# DISABLED:         if pos + alignment > len(binary_data):
# DISABLED:             return False

        # Simple heuristic: check if the position starts a repeated pattern
# DISABLED:         if pos + alignment * 2 <= len(binary_data):
# DISABLED:             pattern1 = binary_data[pos:pos + alignment]
# DISABLED:             pattern2 = binary_data[pos + alignment:pos + alignment * 2]
# DISABLED:             similarity = sum(a == b for a, b in zip(pattern1, pattern2)) / alignment
# DISABLED:             return similarity > 0.8

# DISABLED:         return False

# DISABLED:     def block_detection_score(self, binary_data: bytes) -> float:
        """Score for detectable block structures."""
# DISABLED:         if len(binary_data) < 32:
# DISABLED:             return 0.0

        # Try different block sizes
# DISABLED:         block_sizes = [4, 8, 16, 32, 64, 128, 256]
# DISABLED:         block_scores = []

# DISABLED:         for block_size in block_sizes:
# DISABLED:             if len(binary_data) >= block_size * 2:
# DISABLED:                 score = self._detect_blocks_of_size(binary_data, block_size)
# DISABLED:                 block_scores.append(score)

# DISABLED:         return max(block_scores) if block_scores else 0.0

# DISABLED:     def _detect_blocks_of_size(self, binary_data: bytes, block_size: int) -> float:
        """Detect blocks of a specific size."""
        # Count unique blocks
# DISABLED:         blocks = set()
# DISABLED:         for i in range(0, len(binary_data) - block_size + 1, block_size):
# DISABLED:             block = binary_data[i:i + block_size]
# DISABLED:             blocks.add(block)

# DISABLED:         total_blocks = len(binary_data) // block_size
# DISABLED:         unique_blocks = len(blocks)

        # Score based on repetition (fewer unique blocks = more structure)
# DISABLED:         if total_blocks > 0:
# DISABLED:             repetition_score = 1.0 - (unique_blocks / total_blocks)
# DISABLED:             return repetition_score

# DISABLED:         return 0.0

# DISABLED:     def repeating_block_count(self, binary_data: bytes) -> float:
        """Count of repeating blocks."""
# DISABLED:         if len(binary_data) < 8:
# DISABLED:             return 0.0

        # Use default block size of 16 bytes
# DISABLED:         block_size = min(16, len(binary_data) // 4)
# DISABLED:         if block_size < 4:
# DISABLED:             return 0.0

# DISABLED:         block_counts = {}
# DISABLED:         for i in range(0, len(binary_data) - block_size + 1, block_size):
# DISABLED:             block = binary_data[i:i + block_size]
# DISABLED:             block_counts[block] = block_counts.get(block, 0) + 1

        # Count blocks that appear more than once
# DISABLED:         repeating_blocks = sum(1 for count in block_counts.values() if count > 1)
# DISABLED:         return float(repeating_blocks)

# DISABLED:     def block_size_variance(self, binary_data: bytes) -> float:
        """Variance of detected block sizes."""
# DISABLED:         if len(binary_data) < 16:
# DISABLED:             return 0.0

        # Detect multiple block sizes
# DISABLED:         detected_sizes = []
# DISABLED:         for block_size in [4, 8, 16, 32, 64]:
# DISABLED:             if len(binary_data) >= block_size * 3:
# DISABLED:                 score = self._detect_blocks_of_size(binary_data, block_size)
# DISABLED:                 if score > 0.3:  # Threshold for considering this size significant
# DISABLED:                     detected_sizes.append(block_size)

# DISABLED:         if len(detected_sizes) < 2:
# DISABLED:             return 0.0

        # Calculate variance
# DISABLED:         mean_size = sum(detected_sizes) / len(detected_sizes)
# DISABLED:         variance = sum((size - mean_size) ** 2 for size in detected_sizes) / len(detected_sizes)

# DISABLED:         return variance

# DISABLED:     def structure_regularity(self, binary_data: bytes) -> float:
        """Regularity of structural patterns."""
# DISABLED:         if len(binary_data) < 32:
# DISABLED:             return 0.0

        # Divide data into chunks and look for regular patterns
# DISABLED:         chunk_size = min(32, len(binary_data) // 8)
# DISABLED:         if chunk_size < 4:
# DISABLED:             return 0.0

# DISABLED:         similarities = []
# DISABLED:         chunks = []

        # Collect chunks
# DISABLED:         for i in range(0, len(binary_data), chunk_size):
# DISABLED:             chunk = binary_data[i:i + chunk_size]
# DISABLED:             if len(chunk) == chunk_size:
# DISABLED:                 chunks.append(chunk)

        # Compare consecutive chunks
# DISABLED:         for i in range(len(chunks) - 1):
# DISABLED:             similarity = sum(a == b for a, b in zip(chunks[i], chunks[i + 1])) / chunk_size
# DISABLED:             similarities.append(similarity)

# DISABLED:         return sum(similarities) / len(similarities) if similarities else 0.0

# DISABLED:     def segmentation_score(self, binary_data: bytes) -> float:
        """Score for natural segmentation points."""
# DISABLED:         if len(binary_data) < 64:
# DISABLED:             return 0.0

        # Look for natural break points based on byte distribution changes
# DISABLED:         window_size = min(32, len(binary_data) // 8)
# DISABLED:         if window_size < 8:
# DISABLED:             return 0.0

# DISABLED:         segment_scores = []
# DISABLED:         for i in range(window_size, len(binary_data) - window_size, window_size // 2):
            # Compare distributions before and after this point
# DISABLED:             before_window = binary_data[i - window_size:i]
# DISABLED:             after_window = binary_data[i:i + window_size]

            # Simple distribution similarity
# DISABLED:             before_counts = [0] * 256
# DISABLED:             after_counts = [0] * 256

# DISABLED:             for byte_val in before_window:
# DISABLED:                 before_counts[byte_val] += 1
# DISABLED:             for byte_val in after_window:
# DISABLED:                 after_counts[byte_val] += 1

            # Calculate similarity
# DISABLED:             similarity = sum(min(before_counts[j], after_counts[j]) for j in range(256))
# DISABLED:             total_before = sum(before_counts)
# DISABLED:             total_after = sum(after_counts)
# DISABLED:             total_min = min(total_before, total_after)

# DISABLED:             if total_min > 0:
# DISABLED:                 segment_score = 1.0 - (similarity / total_min)
# DISABLED:                 segment_scores.append(segment_score)

# DISABLED:         return sum(segment_scores) / len(segment_scores) if segment_scores else 0.0

# DISABLED:     def pattern_coherence(self, binary_data: bytes) -> float:
        """Coherence of patterns across segments."""
# DISABLED:         if len(binary_data) < 64:
# DISABLED:             return 0.0

        # Divide into segments and check for consistent patterns
# DISABLED:         num_segments = min(8, len(binary_data) // 16)
# DISABLED:         if num_segments < 2:
# DISABLED:             return 0.0

# DISABLED:         segment_size = len(binary_data) // num_segments
# DISABLED:         patterns = []

# DISABLED:         for i in range(num_segments):
# DISABLED:             start = i * segment_size
# DISABLED:             end = start + segment_size
# DISABLED:             segment = binary_data[start:end]

            # Extract simple pattern (first 8 bytes)
# DISABLED:             if len(segment) >= 8:
# DISABLED:                 pattern = segment[:8]
# DISABLED:                 patterns.append(pattern)

# DISABLED:         if len(patterns) < 2:
# DISABLED:             return 0.0

        # Calculate coherence based on pattern similarity
# DISABLED:         total_similarity = 0
# DISABLED:         comparisons = 0

# DISABLED:         for i in range(len(patterns)):
# DISABLED:             for j in range(i + 1, len(patterns)):
# DISABLED:                 similarity = sum(a == b for a, b in zip(patterns[i], patterns[j])) / len(patterns[i])
# DISABLED:                 total_similarity += similarity
# DISABLED:                 comparisons += 1

# DISABLED:         return total_similarity / comparisons if comparisons > 0 else 0.0

# DISABLED:     def hierarchical_structure(self, binary_data: bytes) -> float:
        """Score for hierarchical structure."""
# DISABLED:         if len(binary_data) < 64:
# DISABLED:             return 0.0

        # Look for structure at multiple scales
# DISABLED:         scale_scores = []

# DISABLED:         for scale in [8, 16, 32, 64]:
# DISABLED:             if len(binary_data) >= scale * 4:
# DISABLED:                 score = self._analyze_scale_structure(binary_data, scale)
# DISABLED:                 scale_scores.append(score)

# DISABLED:         return sum(scale_scores) / len(scale_scores) if scale_scores else 0.0

# DISABLED:     def _analyze_scale_structure(self, binary_data: bytes, scale: int) -> float:
        """Analyze structure at a specific scale."""
        # Count patterns at this scale
# DISABLED:         patterns = set()
# DISABLED:         for i in range(0, len(binary_data) - scale + 1, scale):
# DISABLED:             pattern = binary_data[i:i + scale]
# DISABLED:             patterns.add(pattern)

# DISABLED:         total_patterns = len(binary_data) // scale
# DISABLED:         unique_patterns = len(patterns)

# DISABLED:         if total_patterns == 0:
# DISABLED:             return 0.0

        # Structure score based on pattern repetition
# DISABLED:         structure_score = 1.0 - (unique_patterns / total_patterns)
# DISABLED:         return structure_score

# DISABLED:     def byte_alignment_index(self, binary_data: bytes) -> float:
        """Index of byte alignment patterns."""
        # Similar to alignment_score but focused on common alignments
# DISABLED:         common_alignments = [2, 4, 8, 16]  # Powers of 2

# DISABLED:         alignment_indices = []
# DISABLED:         for alignment in common_alignments:
# DISABLED:             if len(binary_data) >= alignment * 4:
                # Check for periodicity at this alignment
# DISABLED:                 periodic_score = self._check_periodicity_at_alignment(binary_data, alignment)
# DISABLED:                 alignment_indices.append(periodic_score)

# DISABLED:         return sum(alignment_indices) / len(alignment_indices) if alignment_indices else 0.0

# DISABLED:     def _check_periodicity_at_alignment(self, binary_data: bytes, alignment: int) -> float:
        """Check for periodicity at a specific alignment."""
# DISABLED:         if len(binary_data) < alignment * 2:
# DISABLED:             return 0.0

        # Compare bytes at alignment offsets
# DISABLED:         matches = 0
# DISABLED:         total_comparisons = 0

# DISABLED:         for i in range(len(binary_data) - alignment):
# DISABLED:             if binary_data[i] == binary_data[i + alignment]:
# DISABLED:                 matches += 1
# DISABLED:             total_comparisons += 1

# DISABLED:         return matches / total_comparisons if total_comparisons > 0 else 0.0

# DISABLED:     def structural_entropy(self, binary_data: bytes) -> float:
        """Entropy of structural features."""
# DISABLED:         if len(binary_data) < 32:
# DISABLED:             return 0.0

        # Extract structural features (byte changes, runs, etc.)
# DISABLED:         features = []

        # Add byte change positions
# DISABLED:         for i in range(1, len(binary_data)):
# DISABLED:             if binary_data[i] != binary_data[i - 1]:
# DISABLED:                 features.append(('change', i % 256))

        # Add run lengths
# DISABLED:         current_run = 1
# DISABLED:         for i in range(1, len(binary_data)):
# DISABLED:             if binary_data[i] == binary_data[i - 1]:
# DISABLED:                 current_run += 1
# DISABLED:             else:
# DISABLED:                 features.append(('run_length', min(current_run, 255)))
# DISABLED:                 current_run = 1

# DISABLED:         if current_run > 1:
# DISABLED:             features.append(('run_length', min(current_run, 255)))

# DISABLED:         if not features:
# DISABLED:             return 0.0

        # Calculate entropy of features
# DISABLED:         from collections import Counter
# DISABLED:         feature_counts = Counter(features)
# DISABLED:         total_features = len(features)

# DISABLED:         import math
# DISABLED:         entropy = 0.0
# DISABLED:         for count in feature_counts.values():
# DISABLED:             probability = count / total_features
# DISABLED:             entropy -= probability * math.log2(probability)

# DISABLED:         return entropy