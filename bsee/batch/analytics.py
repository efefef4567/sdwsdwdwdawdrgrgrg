"""
Analytics Implementation
Performance analytics and metrics collection for batch jobs.
"""

import time
import threading
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import statistics
from pathlib import Path

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class PerformanceMetric:
    """Individual performance metric data point"""
    timestamp: float
    metric_name: str
    value: float
    job_id: str
    stage: str


@dataclass
class ResourceSnapshot:
    """Snapshot of resource usage at a point in time"""
    timestamp: float
    cpu_percent: float
    memory_mb: float
    disk_io_mb: float
    network_io_mb: float
    active_threads: int


@dataclass
class JobPerformanceData:
    """Performance data for a specific job"""
    job_id: str
    start_time: float
    end_time: Optional[float]
    metrics: List[PerformanceMetric]
    resources: List[ResourceSnapshot]
    stages_completed: List[str]
    errors: List[str]


class AnalyticsCollector:
    """Collects and analyzes performance data for batch jobs"""

    def __init__(self, max_data_points: int = 10000):
        """
        Initialize analytics collector

        Args:
            max_data_points: Maximum number of data points to keep in memory
        """
        self.max_data_points = max_data_points
        self.job_data: Dict[str, JobPerformanceData] = {}
        self.system_metrics: deque = deque(maxlen=max_data_points)
        self.collection_lock = threading.Lock()

        # Collection thread
        self.collection_thread: Optional[threading.Thread] = None
        self.collecting = False
        self.collection_interval = 1.0  # seconds

    def start_collection(self):
        """Start metrics collection"""
        if self.collecting:
            return

        self.collecting = True
        self.collection_thread = threading.Thread(target=self._collection_loop, daemon=True)
        self.collection_thread.start()
        logger.info("Analytics collection started")

    def stop_collection(self):
        """Stop metrics collection"""
        self.collecting = False
        if self.collection_thread and self.collection_thread.is_alive():
            self.collection_thread.join(timeout=5)
        logger.info("Analytics collection stopped")

    def _collection_loop(self):
        """Main collection loop"""
        while self.collecting:
            try:
                self._collect_system_metrics()
                time.sleep(self.collection_interval)
            except Exception as e:
                logger.error(f"Error in analytics collection: {e}")
                time.sleep(self.collection_interval)

    def _collect_system_metrics(self):
        """Collect system-wide metrics"""
        try:
            import psutil

            # Get system metrics
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk_io = psutil.disk_io_counters()
            net_io = psutil.net_io_counters()

            snapshot = ResourceSnapshot(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_mb=memory.used / 1024 / 1024,
                disk_io_mb=(disk_io.read_bytes + disk_io.write_bytes) / 1024 / 1024 if disk_io else 0,
                network_io_mb=(net_io.bytes_sent + net_io.bytes_recv) / 1024 / 1024 if net_io else 0,
                active_threads=len(threading.enumerate())
            )

            with self.collection_lock:
                self.system_metrics.append(snapshot)

        except ImportError:
            logger.warning("psutil not available for system metrics collection")
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")

    def start_job_tracking(self, job_id: str):
        """Start tracking performance for a job"""
        with self.collection_lock:
            self.job_data[job_id] = JobPerformanceData(
                job_id=job_id,
                start_time=time.time(),
                end_time=None,
                metrics=[],
                resources=[],
                stages_completed=[],
                errors=[]
            )
        logger.info(f"Started tracking job: {job_id}")

    def end_job_tracking(self, job_id: str, success: bool = True):
        """End tracking for a job"""
        with self.collection_lock:
            if job_id in self.job_data:
                self.job_data[job_id].end_time = time.time()
                if not success:
                    self.job_data[job_id].errors.append("Job failed or was cancelled")
        logger.info(f"Ended tracking job: {job_id}")

    def record_metric(self, job_id: str, metric_name: str, value: float, stage: str = "unknown"):
        """Record a performance metric for a job"""
        with self.collection_lock:
            if job_id in self.job_data:
                metric = PerformanceMetric(
                    timestamp=time.time(),
                    metric_name=metric_name,
                    value=value,
                    job_id=job_id,
                    stage=stage
                )
                self.job_data[job_id].metrics.append(metric)

    def record_resource_usage(self, job_id: str, cpu_percent: float, memory_mb: float, active_threads: int):
        """Record resource usage for a job"""
        with self.collection_lock:
            if job_id in self.job_data:
                snapshot = ResourceSnapshot(
                    timestamp=time.time(),
                    cpu_percent=cpu_percent,
                    memory_mb=memory_mb,
                    disk_io_mb=0,  # Job-level disk tracking not implemented
                    network_io_mb=0,  # Job-level network tracking not implemented
                    active_threads=active_threads
                )
                self.job_data[job_id].resources.append(snapshot)

    def record_stage_completion(self, job_id: str, stage: str):
        """Record completion of a job stage"""
        with self.collection_lock:
            if job_id in self.job_data:
                self.job_data[job_id].stages_completed.append(stage)

    def record_error(self, job_id: str, error_message: str):
        """Record an error for a job"""
        with self.collection_lock:
            if job_id in self.job_data:
                self.job_data[job_id].errors.append(error_message)

    def get_job_analytics(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get analytics summary for a specific job"""
        with self.collection_lock:
            if job_id not in self.job_data:
                return None

            job_data = self.job_data[job_id]
            return self._analyze_job_performance(job_data)

    def get_system_analytics(self, time_window: float = 300) -> Dict[str, Any]:
        """
        Get system analytics summary

        Args:
            time_window: Time window in seconds to analyze
        """
        with self.collection_lock:
            cutoff_time = time.time() - time_window
            recent_metrics = [m for m in self.system_metrics if m.timestamp >= cutoff_time]

            if not recent_metrics:
                return {}

            return {
                'time_window': time_window,
                'data_points': len(recent_metrics),
                'cpu_stats': self._calculate_metric_stats([m.cpu_percent for m in recent_metrics]),
                'memory_stats': self._calculate_metric_stats([m.memory_mb for m in recent_metrics]),
                'thread_stats': self._calculate_metric_stats([m.active_threads for m in recent_metrics]),
                'trend_data': self._calculate_trends(recent_metrics)
            }

    def get_batch_analytics(self) -> Dict[str, Any]:
        """Get analytics summary for all batch jobs"""
        with self.collection_lock:
            if not self.job_data:
                return {}

            completed_jobs = [j for j in self.job_data.values() if j.end_time is not None]
            running_jobs = [j for j in self.job_data.values() if j.end_time is None]

            return {
                'total_jobs': len(self.job_data),
                'completed_jobs': len(completed_jobs),
                'running_jobs': len(running_jobs),
                'success_rate': self._calculate_success_rate(completed_jobs),
                'average_execution_time': self._calculate_average_execution_time(completed_jobs),
                'resource_efficiency': self._calculate_resource_efficiency(completed_jobs),
                'common_errors': self._get_common_errors(completed_jobs),
                'performance_distribution': self._get_performance_distribution(completed_jobs)
            }

    def _analyze_job_performance(self, job_data: JobPerformanceData) -> Dict[str, Any]:
        """Analyze performance data for a single job"""
        analysis = {
            'job_id': job_data.job_id,
            'start_time': job_data.start_time,
            'end_time': job_data.end_time,
            'execution_time': None,
            'stages_completed': job_data.stages_completed,
            'error_count': len(job_data.errors),
            'errors': job_data.errors,
            'metric_analysis': {},
            'resource_analysis': {}
        }

        if job_data.end_time:
            analysis['execution_time'] = job_data.end_time - job_data.start_time

        # Analyze metrics
        if job_data.metrics:
            metrics_by_name = defaultdict(list)
            for metric in job_data.metrics:
                metrics_by_name[metric.metric_name].append(metric.value)

            for metric_name, values in metrics_by_name.items():
                analysis['metric_analysis'][metric_name] = self._calculate_metric_stats(values)

        # Analyze resources
        if job_data.resources:
            cpu_values = [r.cpu_percent for r in job_data.resources]
            memory_values = [r.memory_mb for r in job_data.resources]
            thread_values = [r.active_threads for r in job_data.resources]

            analysis['resource_analysis'] = {
                'cpu': self._calculate_metric_stats(cpu_values),
                'memory': self._calculate_metric_stats(memory_values),
                'threads': self._calculate_metric_stats(thread_values)
            }

        return analysis

    def _calculate_metric_stats(self, values: List[float]) -> Dict[str, float]:
        """Calculate statistical measures for a list of values"""
        if not values:
            return {}

        return {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'min': min(values),
            'max': max(values),
            'std_dev': statistics.stdev(values) if len(values) > 1 else 0,
            'sum': sum(values)
        }

    def _calculate_trends(self, metrics: List[ResourceSnapshot]) -> Dict[str, float]:
        """Calculate trend information from metrics"""
        if len(metrics) < 2:
            return {}

        # Calculate simple linear trend for CPU and memory
        cpu_values = [m.cpu_percent for m in metrics]
        memory_values = [m.memory_mb for m in metrics]

        return {
            'cpu_trend': self._calculate_linear_trend(cpu_values),
            'memory_trend': self._calculate_linear_trend(memory_values)
        }

    def _calculate_linear_trend(self, values: List[float]) -> float:
        """Calculate simple linear trend (slope)"""
        if len(values) < 2:
            return 0

        n = len(values)
        x = list(range(n))
        sum_x = sum(x)
        sum_y = sum(values)
        sum_xy = sum(x[i] * values[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))

        # Calculate slope
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope

    def _calculate_success_rate(self, completed_jobs: List[JobPerformanceData]) -> float:
        """Calculate success rate for completed jobs"""
        if not completed_jobs:
            return 0

        successful_jobs = sum(1 for job in completed_jobs if not job.errors)
        return (successful_jobs / len(completed_jobs)) * 100

    def _calculate_average_execution_time(self, completed_jobs: List[JobPerformanceData]) -> float:
        """Calculate average execution time for completed jobs"""
        completed_with_time = [j for j in completed_jobs if j.end_time is not None]

        if not completed_with_time:
            return 0

        execution_times = [j.end_time - j.start_time for j in completed_with_time]
        return statistics.mean(execution_times)

    def _calculate_resource_efficiency(self, completed_jobs: List[JobPerformanceData]) -> Dict[str, float]:
        """Calculate resource efficiency metrics"""
        if not completed_jobs:
            return {}

        all_cpu_values = []
        all_memory_values = []

        for job in completed_jobs:
            if job.resources:
                all_cpu_values.extend([r.cpu_percent for r in job.resources])
                all_memory_values.extend([r.memory_mb for r in job.resources])

        efficiency = {}
        if all_cpu_values:
            efficiency['avg_cpu_utilization'] = statistics.mean(all_cpu_values)
        if all_memory_values:
            efficiency['avg_memory_usage'] = statistics.mean(all_memory_values)

        return efficiency

    def _get_common_errors(self, completed_jobs: List[JobPerformanceData]) -> List[Dict[str, Any]]:
        """Get most common errors from completed jobs"""
        error_counts = defaultdict(int)
        error_messages = {}

        for job in completed_jobs:
            for error in job.errors:
                error_counts[error] += 1
                if error not in error_messages:
                    error_messages[error] = []

        # Sort by frequency
        sorted_errors = sorted(error_counts.items(), key=lambda x: x[1], reverse=True)

        return [
            {'error': error, 'count': count}
            for error, count in sorted_errors[:5]  # Top 5 errors
        ]

    def _get_performance_distribution(self, completed_jobs: List[JobPerformanceData]) -> Dict[str, Any]:
        """Get distribution of performance metrics"""
        execution_times = []

        for job in completed_jobs:
            if job.end_time is not None:
                execution_times.append(job.end_time - job.start_time)

        if not execution_times:
            return {}

        return {
            'min_time': min(execution_times),
            'max_time': max(execution_times),
            'mean_time': statistics.mean(execution_times),
            'median_time': statistics.median(execution_times),
            'std_dev_time': statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            'percentiles': {
                '25th': statistics.quantiles(execution_times, n=4)[0] if len(execution_times) >= 4 else 0,
                '50th': statistics.median(execution_times),
                '75th': statistics.quantiles(execution_times, n=4)[2] if len(execution_times) >= 4 else 0,
                '90th': statistics.quantiles(execution_times, n=10)[8] if len(execution_times) >= 10 else 0
            }
        }

    def export_analytics(self, filename: str, format: str = "json") -> bool:
        """
        Export analytics data to file

        Args:
            filename: Output filename
            format: Export format ("json" or "csv")

        Returns:
            bool: True if successful
        """
        try:
            with self.collection_lock:
                data = {
                    'export_timestamp': time.time(),
                    'system_analytics': self.get_system_analytics(),
                    'batch_analytics': self.get_batch_analytics(),
                    'job_analytics': {
                        job_id: self._analyze_job_performance(job_data)
                        for job_id, job_data in self.job_data.items()
                    }
                }

            if format.lower() == "json":
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2, default=str)
            else:
                # CSV format (simplified)
                import csv
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['job_id', 'execution_time', 'error_count', 'stages_completed'])
                    for job_id, job_data in self.job_data.items():
                        execution_time = (job_data.end_time - job_data.start_time) if job_data.end_time else 0
                        writer.writerow([
                            job_id,
                            execution_time,
                            len(job_data.errors),
                            len(job_data.stages_completed)
                        ])

            logger.info(f"Analytics exported to {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to export analytics: {e}")
            return False

    def cleanup_old_data(self, max_age_days: int = 30):
        """Clean up old analytics data"""
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)

        with self.collection_lock:
            # Clean up old job data
            old_jobs = [
                job_id for job_id, job_data in self.job_data.items()
                if job_data.start_time < cutoff_time
            ]

            for job_id in old_jobs:
                del self.job_data[job_id]

            logger.info(f"Cleaned up {len(old_jobs)} old job records")

        # Clean up old system metrics (handled by deque maxlen)
        logger.info("Analytics cleanup completed")