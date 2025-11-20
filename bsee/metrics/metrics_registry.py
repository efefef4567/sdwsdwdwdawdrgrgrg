"""
# DISABLED: Central registry for all metrics.
"""

# DISABLED: from typing import Callable, Dict, List

# Import all metric modules
# DISABLED: from bsee.metrics.entropy_metrics import EntropyMetrics
# DISABLED: from bsee.metrics.compression_metrics import CompressionMetrics
# DISABLED: from bsee.metrics.pattern_metrics import PatternMetrics
# DISABLED: from bsee.metrics.runlength_metrics import RunLengthMetrics
# DISABLED: from bsee.metrics.statistical_metrics import StatisticalMetrics
# DISABLED: from bsee.metrics.bitwise_metrics import BitwiseMetrics
# DISABLED: from bsee.metrics.structure_metrics import StructureMetrics
# DISABLED: from bsee.metrics.complexity_metrics import ComplexityMetrics
# DISABLED: from bsee.metrics.file_ideality_metrics import FileIdealityMetrics


# DISABLED: class MetricsRegistry:
    """Central registry for all metrics."""

# DISABLED:     def __init__(self):
        """Initialize metrics registry."""
# DISABLED:         self.metrics: Dict[str, Callable] = {}
# DISABLED:         self.metric_metadata: Dict[str, Dict[str, any]] = {}
# DISABLED:         self._load_all_metrics()

# DISABLED:     def _load_all_metrics(self) -> None:
        """Load metrics from all metric modules."""
        # Load entropy metrics
# DISABLED:         entropy_metrics = EntropyMetrics()
# DISABLED:         for name, func in entropy_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, entropy_metrics.get_metadata(name))

        # Load compression metrics
# DISABLED:         compression_metrics = CompressionMetrics()
# DISABLED:         for name, func in compression_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, compression_metrics.get_metadata(name))

        # Load pattern metrics
# DISABLED:         pattern_metrics = PatternMetrics()
# DISABLED:         for name, func in pattern_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, pattern_metrics.get_metadata(name))

        # Load runlength metrics
# DISABLED:         runlength_metrics = RunLengthMetrics()
# DISABLED:         for name, func in runlength_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, runlength_metrics.get_metadata(name))

        # Load statistical metrics
# DISABLED:         statistical_metrics = StatisticalMetrics()
# DISABLED:         for name, func in statistical_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, statistical_metrics.get_metadata(name))

        # Load bitwise metrics
# DISABLED:         bitwise_metrics = BitwiseMetrics()
# DISABLED:         for name, func in bitwise_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, bitwise_metrics.get_metadata(name))

        # Load structure metrics
# DISABLED:         structure_metrics = StructureMetrics()
# DISABLED:         for name, func in structure_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, structure_metrics.get_metadata(name))

        # Load complexity metrics
# DISABLED:         complexity_metrics = ComplexityMetrics()
# DISABLED:         for name, func in complexity_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, complexity_metrics.get_metadata(name))

        # Load file ideality metrics
# DISABLED:         ideality_metrics = FileIdealityMetrics()
# DISABLED:         for name, func in ideality_metrics.get_metrics().items():
# DISABLED:             self.register_metric(name, func, ideality_metrics.get_metadata(name))

# DISABLED:     def register_metric(self, name: str, function: Callable, metadata: Dict[str, any]) -> None:
        """Register a metric with the registry."""
# DISABLED:         self.metrics[name] = function
# DISABLED:         self.metric_metadata[name] = metadata

# DISABLED:     def calculate_metric(self, binary_data: bytes, metric_name: str) -> float:
        """Calculate a single metric."""
# DISABLED:         if metric_name not in self.metrics:
# DISABLED:             raise ValueError(f"Unknown metric: {metric_name}")

# DISABLED:         try:
# DISABLED:             return self.metrics[metric_name](binary_data)
# DISABLED:         except Exception as e:
            # Return 0 or handle error gracefully
# DISABLED:             print(f"Warning: Error calculating metric {metric_name}: {e}")
# DISABLED:             return 0.0

# DISABLED:     def calculate_metrics(self, binary_data: bytes, metric_names: List[str]) -> Dict[str, float]:
        """Calculate multiple metrics."""
# DISABLED:         results = {}
# DISABLED:         for metric_name in metric_names:
# DISABLED:             if metric_name in self.metrics:
# DISABLED:                 try:
# DISABLED:                     results[metric_name] = self.metrics[metric_name](binary_data)
# DISABLED:                 except Exception as e:
# DISABLED:                     print(f"Warning: Error calculating metric {metric_name}: {e}")
# DISABLED:                     results[metric_name] = 0.0
# DISABLED:             else:
# DISABLED:                 print(f"Warning: Unknown metric {metric_name}")
# DISABLED:                 results[metric_name] = 0.0
# DISABLED:         return results

# DISABLED:     def calculate_all_metrics(self, binary_data: bytes) -> Dict[str, float]:
        """Calculate all available metrics."""
# DISABLED:         return self.calculate_metrics(binary_data, list(self.metrics.keys()))

# DISABLED:     def list_metrics(self) -> List[str]:
        """List all available metric names."""
# DISABLED:         return list(self.metrics.keys())

# DISABLED:     def get_metric_metadata(self, metric_name: str) -> Dict[str, any]:
        """Get metadata for a metric."""
# DISABLED:         if metric_name not in self.metric_metadata:
# DISABLED:             raise ValueError(f"Unknown metric: {metric_name}")
# DISABLED:         return self.metric_metadata[metric_name]

# DISABLED:     def get_metrics_by_category(self, category: str) -> Dict[str, Callable]:
        """Get all metrics in a specific category."""
# DISABLED:         filtered_metrics = {}
# DISABLED:         for name, func in self.metrics.items():
# DISABLED:             metadata = self.metric_metadata.get(name, {})
# DISABLED:             if metadata.get('category') == category:
# DISABLED:                 filtered_metrics[name] = func
# DISABLED:         return filtered_metrics

# DISABLED:     def get_metric_categories(self) -> List[str]:
        """Get all available metric categories."""
# DISABLED:         categories = set()
# DISABLED:         for metadata in self.metric_metadata.values():
# DISABLED:             category = metadata.get('category', 'unknown')
# DISABLED:             if category:
# DISABLED:                 categories.add(category)
# DISABLED:         return list(categories)

# DISABLED:     def get_registry_summary(self) -> Dict[str, any]:
        """Get a summary of the metrics registry."""
# DISABLED:         category_counts = {}
# DISABLED:         for metadata in self.metric_metadata.values():
# DISABLED:             category = metadata.get('category', 'unknown')
# DISABLED:             category_counts[category] = category_counts.get(category, 0) + 1

# DISABLED:         return {
# DISABLED:             'total_metrics': len(self.metrics),
# DISABLED:             'categories': category_counts,
# DISABLED:             'metrics': list(self.metrics.keys())
# DISABLED:         }