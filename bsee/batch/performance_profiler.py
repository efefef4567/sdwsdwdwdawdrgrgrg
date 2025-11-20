"""
Performance Profiler Implementation
Detailed performance profiling for batch jobs with function-level timing.
"""

import time
import threading
import tracemalloc
import cProfile
import pstats
import io
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from contextlib import contextmanager
from collections import defaultdict, deque
import functools
import inspect

from ...utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class FunctionProfile:
    """Profile data for a single function"""
    function_name: str
    call_count: int
    total_time: float
    average_time: float
    max_time: float
    min_time: float
    memory_usage_mb: float
    thread_id: int


@dataclass
class JobProfile:
    """Complete profile for a job execution"""
    job_id: str
    start_time: float
    end_time: Optional[float]
    functions: Dict[str, FunctionProfile]
    memory_snapshots: List[Dict[str, Any]]
    thread_activity: Dict[int, List[str]]
    performance_events: List[Dict[str, Any]]


class PerformanceProfiler:
    """Detailed performance profiling for batch jobs"""

    def __init__(self, max_functions: int = 1000):
        """
        Initialize performance profiler

        Args:
            max_functions: Maximum number of functions to track
        """
        self.max_functions = max_functions
        self.active_profiles: Dict[str, JobProfile] = {}
        self.completed_profiles: Dict[str, JobProfile] = {}
        self.profile_lock = threading.Lock()

        # Performance tracking
        self.function_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.memory_tracker = MemoryTracker()
        self.thread_tracker = ThreadTracker()

        # Profiling state
        self.cprofiler: Optional[cProfile.Profile] = None
        self.tracing_enabled = False

    def start_job_profiling(self, job_id: str) -> str:
        """
        Start profiling a job

        Args:
            job_id: ID of job to profile

        Returns:
            Profile session ID
        """
        with self.profile_lock:
            profile_id = f"{job_id}_{int(time.time())}"

            self.active_profiles[profile_id] = JobProfile(
                job_id=job_id,
                start_time=time.time(),
                end_time=None,
                functions={},
                memory_snapshots=[],
                thread_activity={},
                performance_events=[]
            )

            # Start memory tracking
            self.memory_tracker.start_tracking()

            # Start thread tracking
            self.thread_tracker.start_tracking()

            # Enable function tracing
            self._enable_function_tracing()

            logger.info(f"Started profiling job: {job_id}")
            return profile_id

    def end_job_profiling(self, profile_id: str) -> Optional[JobProfile]:
        """
        End profiling for a job

        Args:
            profile_id: Profile session ID

        Returns:
            Completed job profile
        """
        with self.profile_lock:
            if profile_id not in self.active_profiles:
                logger.warning(f"Profile not found: {profile_id}")
                return None

            profile = self.active_profiles.pop(profile_id)
            profile.end_time = time.time()

            # Stop tracking
            self.memory_tracker.stop_tracking()
            self.thread_tracker.stop_tracking()
            self._disable_function_tracing()

            # Get final memory snapshot
            final_memory = self.memory_tracker.get_current_snapshot()
            if final_memory:
                profile.memory_snapshots.append(final_memory)

            # Move to completed profiles
            self.completed_profiles[profile_id] = profile

            logger.info(f"Completed profiling job: {profile.job_id}")
            return profile

    def get_job_profile(self, job_id: str) -> Optional[JobProfile]:
        """Get profile for a specific job"""
        with self.profile_lock:
            # Check active profiles
            for profile in self.active_profiles.values():
                if profile.job_id == job_id:
                    return profile

            # Check completed profiles
            for profile in self.completed_profiles.values():
                if profile.job_id == job_id:
                    return profile

        return None

    @contextmanager
    def profile_function(self, job_id: str, function_name: str):
        """Context manager for profiling a function"""
        start_time = time.time()
        start_memory = self.memory_tracker.get_current_usage()

        try:
            yield
        finally:
            end_time = time.time()
            end_memory = self.memory_tracker.get_current_usage()
            execution_time = end_time - start_time
            memory_delta = (end_memory or 0) - (start_memory or 0)

            self._record_function_execution(job_id, function_name, execution_time, memory_delta)

    def _record_function_execution(self, job_id: str, function_name: str, execution_time: float, memory_delta: float):
        """Record execution of a function"""
        with self.profile_lock:
            # Find the profile
            profile = None
            for p in self.active_profiles.values():
                if p.job_id == job_id:
                    profile = p
                    break

            if not profile:
                return

            # Update or create function profile
            if function_name in profile.functions:
                func_profile = profile.functions[function_name]
                func_profile.call_count += 1
                func_profile.total_time += execution_time
                func_profile.average_time = func_profile.total_time / func_profile.call_count
                func_profile.max_time = max(func_profile.max_time, execution_time)
                func_profile.min_time = min(func_profile.min_time, execution_time)
                func_profile.memory_usage_mb += memory_delta
            else:
                func_profile = FunctionProfile(
                    function_name=function_name,
                    call_count=1,
                    total_time=execution_time,
                    average_time=execution_time,
                    max_time=execution_time,
                    min_time=execution_time,
                    memory_usage_mb=memory_delta,
                    thread_id=threading.get_ident()
                )
                profile.functions[function_name] = func_profile

            # Store in function times history
            self.function_times[function_name].append(execution_time)

            # Add performance event
            profile.performance_events.append({
                'timestamp': time.time(),
                'event_type': 'function_execution',
                'function_name': function_name,
                'execution_time': execution_time,
                'memory_delta': memory_delta,
                'thread_id': threading.get_ident()
            })

    def _enable_function_tracing(self):
        """Enable automatic function tracing"""
        if self.tracing_enabled:
            return

        # Note: This is a simplified version. A full implementation would use
        # sys.settrace() or decorator-based tracing for comprehensive coverage
        self.tracing_enabled = True

    def _disable_function_tracing(self):
        """Disable function tracing"""
        self.tracing_enabled = False

    def record_memory_snapshot(self, job_id: str):
        """Record a memory snapshot for a job"""
        snapshot = self.memory_tracker.get_current_snapshot()
        if snapshot:
            with self.profile_lock:
                for profile in self.active_profiles.values():
                    if profile.job_id == job_id:
                        snapshot['timestamp'] = time.time()
                        profile.memory_snapshots.append(snapshot)
                        break

    def record_thread_activity(self, job_id: str, activity: str):
        """Record thread activity for a job"""
        thread_id = threading.get_ident()

        with self.profile_lock:
            for profile in self.active_profiles.values():
                if profile.job_id == job_id:
                    if thread_id not in profile.thread_activity:
                        profile.thread_activity[thread_id] = []
                    profile.thread_activity[thread_id].append({
                        'timestamp': time.time(),
                        'activity': activity
                    })
                    break

    def analyze_performance_bottlenecks(self, profile: JobProfile) -> Dict[str, Any]:
        """Analyze performance bottlenecks in a job profile"""
        if not profile.functions:
            return {'bottlenecks': [], 'recommendations': []}

        # Sort functions by total time
        sorted_functions = sorted(
            profile.functions.values(),
            key=lambda f: f.total_time,
            reverse=True
        )

        # Identify bottlenecks (top 20% of time-consuming functions)
        total_time = sum(f.total_time for f in profile.functions.values())
        bottlenecks = []
        cumulative_time = 0

        for func in sorted_functions:
            cumulative_time += func.total_time
            percentage = (func.total_time / total_time * 100) if total_time > 0 else 0

            if cumulative_time <= total_time * 0.8 or percentage > 5:  # Top 80% or >5% individually
                bottlenecks.append({
                    'function_name': func.function_name,
                    'total_time': func.total_time,
                    'percentage': percentage,
                    'call_count': func.call_count,
                    'average_time': func.average_time,
                    'memory_usage': func.memory_usage_mb
                })

        # Generate recommendations
        recommendations = []
        for bottleneck in bottlenecks:
            if bottleneck['average_time'] > 1.0:  # Slow average time
                recommendations.append(f"Optimize {bottleneck['function_name']} - average execution time: {bottleneck['average_time']:.3f}s")

            if bottleneck['call_count'] > 1000:  # High call count
                recommendations.append(f"Consider caching or optimizing {bottleneck['function_name']} - called {bottleneck['call_count']} times")

            if bottleneck['memory_usage'] > 100:  # High memory usage
                recommendations.append(f"Review memory usage in {bottleneck['function_name']} - {bottleneck['memory_usage']:.1f}MB")

        return {
            'bottlenecks': bottlenecks,
            'recommendations': recommendations,
            'total_execution_time': total_time,
            'total_functions': len(profile.functions)
        }

    def compare_performance(self, profile1: JobProfile, profile2: JobProfile) -> Dict[str, Any]:
        """Compare performance between two job profiles"""
        comparison = {
            'job1_id': profile1.job_id,
            'job2_id': profile2.job_id,
            'execution_time_comparison': {},
            'function_comparison': {},
            'memory_comparison': {},
            'overall_improvement': 0.0
        }

        # Compare execution times
        if profile1.end_time and profile2.end_time:
            time1 = profile1.end_time - profile1.start_time
            time2 = profile2.end_time - profile2.start_time

            comparison['execution_time_comparison'] = {
                'job1_time': time1,
                'job2_time': time2,
                'difference': time2 - time1,
                'percentage_change': ((time2 - time1) / time1 * 100) if time1 > 0 else 0
            }

        # Compare common functions
        common_functions = set(profile1.functions.keys()) & set(profile2.functions.keys())
        for func_name in common_functions:
            func1 = profile1.functions[func_name]
            func2 = profile2.functions[func_name]

            comparison['function_comparison'][func_name] = {
                'job1_avg_time': func1.average_time,
                'job2_avg_time': func2.average_time,
                'job1_call_count': func1.call_count,
                'job2_call_count': func2.call_count,
                'time_improvement': ((func1.average_time - func2.average_time) / func1.average_time * 100) if func1.average_time > 0 else 0
            }

        # Compare memory usage
        if profile1.memory_snapshots and profile2.memory_snapshots:
            mem1 = max(s.get('current_mb', 0) for s in profile1.memory_snapshots)
            mem2 = max(s.get('current_mb', 0) for s in profile2.memory_snapshots)

            comparison['memory_comparison'] = {
                'job1_peak_memory': mem1,
                'job2_peak_memory': mem2,
                'memory_difference': mem2 - mem1,
                'memory_percentage_change': ((mem2 - mem1) / mem1 * 100) if mem1 > 0 else 0
            }

        return comparison

    def generate_performance_report(self, profile: JobProfile) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        execution_time = (profile.end_time - profile.start_time) if profile.end_time else 0

        report = {
            'job_id': profile.job_id,
            'execution_time': execution_time,
            'start_time': profile.start_time,
            'end_time': profile.end_time,
            'functions_profiled': len(profile.functions),
            'memory_snapshots': len(profile.memory_snapshots),
            'active_threads': len(profile.thread_activity),
            'performance_events': len(profile.performance_events)
        }

        # Function analysis
        if profile.functions:
            sorted_functions = sorted(
                profile.functions.values(),
                key=lambda f: f.total_time,
                reverse=True
            )

            report['top_functions'] = [
                {
                    'name': func.function_name,
                    'total_time': func.total_time,
                    'percentage': (func.total_time / execution_time * 100) if execution_time > 0 else 0,
                    'call_count': func.call_count,
                    'average_time': func.average_time
                }
                for func in sorted_functions[:10]
            ]

            report['function_statistics'] = {
                'total_functions': len(profile.functions),
                'total_calls': sum(f.call_count for f in profile.functions.values()),
                'average_function_time': sum(f.total_time for f in profile.functions.values()) / len(profile.functions)
            }

        # Memory analysis
        if profile.memory_snapshots:
            memory_values = [s.get('current_mb', 0) for s in profile.memory_snapshots]
            report['memory_analysis'] = {
                'peak_memory_mb': max(memory_values) if memory_values else 0,
                'average_memory_mb': sum(memory_values) / len(memory_values) if memory_values else 0,
                'memory_snapshots_count': len(profile.memory_snapshots)
            }

        # Thread analysis
        if profile.thread_activity:
            thread_activities = []
            for thread_id, activities in profile.thread_activity.items():
                thread_activities.append({
                    'thread_id': thread_id,
                    'activity_count': len(activities),
                    'activities': activities[:5]  # First 5 activities
                })

            report['thread_analysis'] = thread_activities

        # Bottleneck analysis
        report['bottleneck_analysis'] = self.analyze_performance_bottlenecks(profile)

        return report

    def export_profile_data(self, profile_id: str, filename: str, format: str = "json") -> bool:
        """Export profile data to file"""
        with self.profile_lock:
            profile = self.completed_profiles.get(profile_id)
            if not profile:
                logger.error(f"Profile not found: {profile_id}")
                return False

        try:
            if format.lower() == "json":
                import json
                report = self.generate_performance_report(profile)
                with open(filename, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
            else:
                # CSV format for function data
                import csv
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['function_name', 'call_count', 'total_time', 'average_time', 'max_time', 'min_time', 'memory_usage_mb'])
                    for func in profile.functions.values():
                        writer.writerow([
                            func.function_name,
                            func.call_count,
                            func.total_time,
                            func.average_time,
                            func.max_time,
                            func.min_time,
                            func.memory_usage_mb
                        ])

            logger.info(f"Profile data exported to {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to export profile data: {e}")
            return False

    def cleanup_old_profiles(self, max_age_hours: int = 24):
        """Clean up old profile data"""
        cutoff_time = time.time() - (max_age_hours * 3600)

        with self.profile_lock:
            old_profiles = [
                profile_id for profile_id, profile in self.completed_profiles.items()
                if profile.start_time < cutoff_time
            ]

            for profile_id in old_profiles:
                del self.completed_profiles[profile_id]

            logger.info(f"Cleaned up {len(old_profiles)} old profiles")

    def get_system_performance_summary(self) -> Dict[str, Any]:
        """Get summary of system performance across all profiles"""
        with self.profile_lock:
            all_profiles = list(self.active_profiles.values()) + list(self.completed_profiles.values())

        if not all_profiles:
            return {'message': 'No performance data available'}

        # Calculate statistics
        execution_times = []
        memory_peaks = []
        function_counts = []

        for profile in all_profiles:
            if profile.end_time:
                execution_times.append(profile.end_time - profile.start_time)

            if profile.memory_snapshots:
                memory_values = [s.get('current_mb', 0) for s in profile.memory_snapshots]
                memory_peaks.append(max(memory_values))

            function_counts.append(len(profile.functions))

        summary = {
            'total_profiles': len(all_profiles),
            'active_profiles': len(self.active_profiles),
            'completed_profiles': len(self.completed_profiles)
        }

        if execution_times:
            summary['execution_time_stats'] = {
                'average': sum(execution_times) / len(execution_times),
                'min': min(execution_times),
                'max': max(execution_times)
            }

        if memory_peaks:
            summary['memory_peak_stats'] = {
                'average': sum(memory_peaks) / len(memory_peaks),
                'min': min(memory_peaks),
                'max': max(memory_peaks)
            }

        if function_counts:
            summary['function_count_stats'] = {
                'average': sum(function_counts) / len(function_counts),
                'min': min(function_counts),
                'max': max(function_counts)
            }

        return summary


class MemoryTracker:
    """Track memory usage for profiling"""

    def __init__(self):
        self.tracking = False
        self.snapshots = []

    def start_tracking(self):
        """Start memory tracking"""
        if not self.tracking:
            tracemalloc.start()
            self.tracking = True

    def stop_tracking(self):
        """Stop memory tracking"""
        if self.tracking:
            tracemalloc.stop()
            self.tracking = False

    def get_current_usage(self) -> Optional[float]:
        """Get current memory usage in MB"""
        if self.tracing:
            current, peak = tracemalloc.get_traced_memory()
            return current / 1024 / 1024
        return None

    def get_current_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get current memory snapshot"""
        if self.tracking:
            current, peak = tracemalloc.get_traced_memory()
            return {
                'current_mb': current / 1024 / 1024,
                'peak_mb': peak / 1024 / 1024
            }
        return None


class ThreadTracker:
    """Track thread activity for profiling"""

    def __init__(self):
        self.tracking = False
        self.thread_activities = defaultdict(list)

    def start_tracking(self):
        """Start thread tracking"""
        self.tracking = True

    def stop_tracking(self):
        """Stop thread tracking"""
        self.tracking = False

    def record_activity(self, thread_id: int, activity: str):
        """Record thread activity"""
        if self.tracking:
            self.thread_activities[thread_id].append({
                'timestamp': time.time(),
                'activity': activity
            })


def profile_function(job_id: str, name: Optional[str] = None):
    """Decorator for profiling functions"""
    def decorator(func: Callable) -> Callable:
        func_name = name or f"{func.__module__}.{func.__name__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get profiler instance
            # This would need to be injected or accessed via a singleton
            profiler = getattr(wrapper, '_profiler', None)
            if not profiler:
                return func(*args, **kwargs)

            with profiler.profile_function(job_id, func_name):
                return func(*args, **kwargs)

        return wrapper
    return decorator