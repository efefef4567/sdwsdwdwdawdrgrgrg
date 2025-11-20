"""
# DISABLED: Performance Profiler Implementation
# DISABLED: Detailed performance profiling for batch jobs with function-level timing.
"""

# DISABLED: import time
# DISABLED: import threading
# DISABLED: import tracemalloc
# DISABLED: import cProfile
# DISABLED: import pstats
# DISABLED: import io
# DISABLED: from typing import Dict, List, Any, Optional, Callable
# DISABLED: from dataclasses import dataclass, asdict
# DISABLED: from contextlib import contextmanager
# DISABLED: from collections import defaultdict, deque
# DISABLED: import functools
# DISABLED: import inspect

# DISABLED: from ...utils.logger import get_logger

# DISABLED: logger = get_logger(__name__)


# DISABLED: @dataclass
# DISABLED: class FunctionProfile:
    """Profile data for a single function"""
# DISABLED:     function_name: str
# DISABLED:     call_count: int
# DISABLED:     total_time: float
# DISABLED:     average_time: float
# DISABLED:     max_time: float
# DISABLED:     min_time: float
# DISABLED:     memory_usage_mb: float
# DISABLED:     thread_id: int


# DISABLED: @dataclass
# DISABLED: class JobProfile:
    """Complete profile for a job execution"""
# DISABLED:     job_id: str
# DISABLED:     start_time: float
# DISABLED:     end_time: Optional[float]
# DISABLED:     functions: Dict[str, FunctionProfile]
# DISABLED:     memory_snapshots: List[Dict[str, Any]]
# DISABLED:     thread_activity: Dict[int, List[str]]
# DISABLED:     performance_events: List[Dict[str, Any]]


# DISABLED: class PerformanceProfiler:
    """Detailed performance profiling for batch jobs"""

# DISABLED:     def __init__(self, max_functions: int = 1000):
        """
# DISABLED:         Initialize performance profiler

# DISABLED:         Args:
# DISABLED:             max_functions: Maximum number of functions to track
        """
# DISABLED:         self.max_functions = max_functions
# DISABLED:         self.active_profiles: Dict[str, JobProfile] = {}
# DISABLED:         self.completed_profiles: Dict[str, JobProfile] = {}
# DISABLED:         self.profile_lock = threading.Lock()

        # Performance tracking
# DISABLED:         self.function_times: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
# DISABLED:         self.memory_tracker = MemoryTracker()
# DISABLED:         self.thread_tracker = ThreadTracker()

        # Profiling state
# DISABLED:         self.cprofiler: Optional[cProfile.Profile] = None
# DISABLED:         self.tracing_enabled = False

# DISABLED:     def start_job_profiling(self, job_id: str) -> str:
        """
# DISABLED:         Start profiling a job

# DISABLED:         Args:
# DISABLED:             job_id: ID of job to profile

# DISABLED:         Returns:
# DISABLED:             Profile session ID
        """
# DISABLED:         with self.profile_lock:
# DISABLED:             profile_id = f"{job_id}_{int(time.time())}"

# DISABLED:             self.active_profiles[profile_id] = JobProfile(
# DISABLED:                 job_id=job_id,
# DISABLED:                 start_time=time.time(),
# DISABLED:                 end_time=None,
# DISABLED:                 functions={},
# DISABLED:                 memory_snapshots=[],
# DISABLED:                 thread_activity={},
# DISABLED:                 performance_events=[]
# DISABLED:             )

            # Start memory tracking
# DISABLED:             self.memory_tracker.start_tracking()

            # Start thread tracking
# DISABLED:             self.thread_tracker.start_tracking()

            # Enable function tracing
# DISABLED:             self._enable_function_tracing()

# DISABLED:             logger.info(f"Started profiling job: {job_id}")
# DISABLED:             return profile_id

# DISABLED:     def end_job_profiling(self, profile_id: str) -> Optional[JobProfile]:
        """
# DISABLED:         End profiling for a job

# DISABLED:         Args:
# DISABLED:             profile_id: Profile session ID

# DISABLED:         Returns:
# DISABLED:             Completed job profile
        """
# DISABLED:         with self.profile_lock:
# DISABLED:             if profile_id not in self.active_profiles:
# DISABLED:                 logger.warning(f"Profile not found: {profile_id}")
# DISABLED:                 return None

# DISABLED:             profile = self.active_profiles.pop(profile_id)
# DISABLED:             profile.end_time = time.time()

            # Stop tracking
# DISABLED:             self.memory_tracker.stop_tracking()
# DISABLED:             self.thread_tracker.stop_tracking()
# DISABLED:             self._disable_function_tracing()

            # Get final memory snapshot
# DISABLED:             final_memory = self.memory_tracker.get_current_snapshot()
# DISABLED:             if final_memory:
# DISABLED:                 profile.memory_snapshots.append(final_memory)

            # Move to completed profiles
# DISABLED:             self.completed_profiles[profile_id] = profile

# DISABLED:             logger.info(f"Completed profiling job: {profile.job_id}")
# DISABLED:             return profile

# DISABLED:     def get_job_profile(self, job_id: str) -> Optional[JobProfile]:
        """Get profile for a specific job"""
# DISABLED:         with self.profile_lock:
            # Check active profiles
# DISABLED:             for profile in self.active_profiles.values():
# DISABLED:                 if profile.job_id == job_id:
# DISABLED:                     return profile

            # Check completed profiles
# DISABLED:             for profile in self.completed_profiles.values():
# DISABLED:                 if profile.job_id == job_id:
# DISABLED:                     return profile

# DISABLED:         return None

# DISABLED:     @contextmanager
# DISABLED:     def profile_function(self, job_id: str, function_name: str):
        """Context manager for profiling a function"""
# DISABLED:         start_time = time.time()
# DISABLED:         start_memory = self.memory_tracker.get_current_usage()

# DISABLED:         try:
# DISABLED:             yield
# DISABLED:         finally:
# DISABLED:             end_time = time.time()
# DISABLED:             end_memory = self.memory_tracker.get_current_usage()
# DISABLED:             execution_time = end_time - start_time
# DISABLED:             memory_delta = (end_memory or 0) - (start_memory or 0)

# DISABLED:             self._record_function_execution(job_id, function_name, execution_time, memory_delta)

# DISABLED:     def _record_function_execution(self, job_id: str, function_name: str, execution_time: float, memory_delta: float):
        """Record execution of a function"""
# DISABLED:         with self.profile_lock:
            # Find the profile
# DISABLED:             profile = None
# DISABLED:             for p in self.active_profiles.values():
# DISABLED:                 if p.job_id == job_id:
# DISABLED:                     profile = p
# DISABLED:                     break

# DISABLED:             if not profile:
# DISABLED:                 return

            # Update or create function profile
# DISABLED:             if function_name in profile.functions:
# DISABLED:                 func_profile = profile.functions[function_name]
# DISABLED:                 func_profile.call_count += 1
# DISABLED:                 func_profile.total_time += execution_time
# DISABLED:                 func_profile.average_time = func_profile.total_time / func_profile.call_count
# DISABLED:                 func_profile.max_time = max(func_profile.max_time, execution_time)
# DISABLED:                 func_profile.min_time = min(func_profile.min_time, execution_time)
# DISABLED:                 func_profile.memory_usage_mb += memory_delta
# DISABLED:             else:
# DISABLED:                 func_profile = FunctionProfile(
# DISABLED:                     function_name=function_name,
# DISABLED:                     call_count=1,
# DISABLED:                     total_time=execution_time,
# DISABLED:                     average_time=execution_time,
# DISABLED:                     max_time=execution_time,
# DISABLED:                     min_time=execution_time,
# DISABLED:                     memory_usage_mb=memory_delta,
# DISABLED:                     thread_id=threading.get_ident()
# DISABLED:                 )
# DISABLED:                 profile.functions[function_name] = func_profile

            # Store in function times history
# DISABLED:             self.function_times[function_name].append(execution_time)

            # Add performance event
# DISABLED:             profile.performance_events.append({
# DISABLED:                 'timestamp': time.time(),
# DISABLED:                 'event_type': 'function_execution',
# DISABLED:                 'function_name': function_name,
# DISABLED:                 'execution_time': execution_time,
# DISABLED:                 'memory_delta': memory_delta,
# DISABLED:                 'thread_id': threading.get_ident()
# DISABLED:             })

# DISABLED:     def _enable_function_tracing(self):
        """Enable automatic function tracing"""
# DISABLED:         if self.tracing_enabled:
# DISABLED:             return

        # Note: This is a simplified version. A full implementation would use
        # sys.settrace() or decorator-based tracing for comprehensive coverage
# DISABLED:         self.tracing_enabled = True

# DISABLED:     def _disable_function_tracing(self):
        """Disable function tracing"""
# DISABLED:         self.tracing_enabled = False

# DISABLED:     def record_memory_snapshot(self, job_id: str):
        """Record a memory snapshot for a job"""
# DISABLED:         snapshot = self.memory_tracker.get_current_snapshot()
# DISABLED:         if snapshot:
# DISABLED:             with self.profile_lock:
# DISABLED:                 for profile in self.active_profiles.values():
# DISABLED:                     if profile.job_id == job_id:
# DISABLED:                         snapshot['timestamp'] = time.time()
# DISABLED:                         profile.memory_snapshots.append(snapshot)
# DISABLED:                         break

# DISABLED:     def record_thread_activity(self, job_id: str, activity: str):
        """Record thread activity for a job"""
# DISABLED:         thread_id = threading.get_ident()

# DISABLED:         with self.profile_lock:
# DISABLED:             for profile in self.active_profiles.values():
# DISABLED:                 if profile.job_id == job_id:
# DISABLED:                     if thread_id not in profile.thread_activity:
# DISABLED:                         profile.thread_activity[thread_id] = []
# DISABLED:                     profile.thread_activity[thread_id].append({
# DISABLED:                         'timestamp': time.time(),
# DISABLED:                         'activity': activity
# DISABLED:                     })
# DISABLED:                     break

# DISABLED:     def analyze_performance_bottlenecks(self, profile: JobProfile) -> Dict[str, Any]:
        """Analyze performance bottlenecks in a job profile"""
# DISABLED:         if not profile.functions:
# DISABLED:             return {'bottlenecks': [], 'recommendations': []}

        # Sort functions by total time
# DISABLED:         sorted_functions = sorted(
# DISABLED:             profile.functions.values(),
# DISABLED:             key=lambda f: f.total_time,
# DISABLED:             reverse=True
# DISABLED:         )

        # Identify bottlenecks (top 20% of time-consuming functions)
# DISABLED:         total_time = sum(f.total_time for f in profile.functions.values())
# DISABLED:         bottlenecks = []
# DISABLED:         cumulative_time = 0

# DISABLED:         for func in sorted_functions:
# DISABLED:             cumulative_time += func.total_time
# DISABLED:             percentage = (func.total_time / total_time * 100) if total_time > 0 else 0

# DISABLED:             if cumulative_time <= total_time * 0.8 or percentage > 5:  # Top 80% or >5% individually
# DISABLED:                 bottlenecks.append({
# DISABLED:                     'function_name': func.function_name,
# DISABLED:                     'total_time': func.total_time,
# DISABLED:                     'percentage': percentage,
# DISABLED:                     'call_count': func.call_count,
# DISABLED:                     'average_time': func.average_time,
# DISABLED:                     'memory_usage': func.memory_usage_mb
# DISABLED:                 })

        # Generate recommendations
# DISABLED:         recommendations = []
# DISABLED:         for bottleneck in bottlenecks:
# DISABLED:             if bottleneck['average_time'] > 1.0:  # Slow average time
# DISABLED:                 recommendations.append(f"Optimize {bottleneck['function_name']} - average execution time: {bottleneck['average_time']:.3f}s")

# DISABLED:             if bottleneck['call_count'] > 1000:  # High call count
# DISABLED:                 recommendations.append(f"Consider caching or optimizing {bottleneck['function_name']} - called {bottleneck['call_count']} times")

# DISABLED:             if bottleneck['memory_usage'] > 100:  # High memory usage
# DISABLED:                 recommendations.append(f"Review memory usage in {bottleneck['function_name']} - {bottleneck['memory_usage']:.1f}MB")

# DISABLED:         return {
# DISABLED:             'bottlenecks': bottlenecks,
# DISABLED:             'recommendations': recommendations,
# DISABLED:             'total_execution_time': total_time,
# DISABLED:             'total_functions': len(profile.functions)
# DISABLED:         }

# DISABLED:     def compare_performance(self, profile1: JobProfile, profile2: JobProfile) -> Dict[str, Any]:
        """Compare performance between two job profiles"""
# DISABLED:         comparison = {
# DISABLED:             'job1_id': profile1.job_id,
# DISABLED:             'job2_id': profile2.job_id,
# DISABLED:             'execution_time_comparison': {},
# DISABLED:             'function_comparison': {},
# DISABLED:             'memory_comparison': {},
# DISABLED:             'overall_improvement': 0.0
# DISABLED:         }

        # Compare execution times
# DISABLED:         if profile1.end_time and profile2.end_time:
# DISABLED:             time1 = profile1.end_time - profile1.start_time
# DISABLED:             time2 = profile2.end_time - profile2.start_time

# DISABLED:             comparison['execution_time_comparison'] = {
# DISABLED:                 'job1_time': time1,
# DISABLED:                 'job2_time': time2,
# DISABLED:                 'difference': time2 - time1,
# DISABLED:                 'percentage_change': ((time2 - time1) / time1 * 100) if time1 > 0 else 0
# DISABLED:             }

        # Compare common functions
# DISABLED:         common_functions = set(profile1.functions.keys()) & set(profile2.functions.keys())
# DISABLED:         for func_name in common_functions:
# DISABLED:             func1 = profile1.functions[func_name]
# DISABLED:             func2 = profile2.functions[func_name]

# DISABLED:             comparison['function_comparison'][func_name] = {
# DISABLED:                 'job1_avg_time': func1.average_time,
# DISABLED:                 'job2_avg_time': func2.average_time,
# DISABLED:                 'job1_call_count': func1.call_count,
# DISABLED:                 'job2_call_count': func2.call_count,
# DISABLED:                 'time_improvement': ((func1.average_time - func2.average_time) / func1.average_time * 100) if func1.average_time > 0 else 0
# DISABLED:             }

        # Compare memory usage
# DISABLED:         if profile1.memory_snapshots and profile2.memory_snapshots:
# DISABLED:             mem1 = max(s.get('current_mb', 0) for s in profile1.memory_snapshots)
# DISABLED:             mem2 = max(s.get('current_mb', 0) for s in profile2.memory_snapshots)

# DISABLED:             comparison['memory_comparison'] = {
# DISABLED:                 'job1_peak_memory': mem1,
# DISABLED:                 'job2_peak_memory': mem2,
# DISABLED:                 'memory_difference': mem2 - mem1,
# DISABLED:                 'memory_percentage_change': ((mem2 - mem1) / mem1 * 100) if mem1 > 0 else 0
# DISABLED:             }

# DISABLED:         return comparison

# DISABLED:     def generate_performance_report(self, profile: JobProfile) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
# DISABLED:         execution_time = (profile.end_time - profile.start_time) if profile.end_time else 0

# DISABLED:         report = {
# DISABLED:             'job_id': profile.job_id,
# DISABLED:             'execution_time': execution_time,
# DISABLED:             'start_time': profile.start_time,
# DISABLED:             'end_time': profile.end_time,
# DISABLED:             'functions_profiled': len(profile.functions),
# DISABLED:             'memory_snapshots': len(profile.memory_snapshots),
# DISABLED:             'active_threads': len(profile.thread_activity),
# DISABLED:             'performance_events': len(profile.performance_events)
# DISABLED:         }

        # Function analysis
# DISABLED:         if profile.functions:
# DISABLED:             sorted_functions = sorted(
# DISABLED:                 profile.functions.values(),
# DISABLED:                 key=lambda f: f.total_time,
# DISABLED:                 reverse=True
# DISABLED:             )

# DISABLED:             report['top_functions'] = [
# DISABLED:                 {
# DISABLED:                     'name': func.function_name,
# DISABLED:                     'total_time': func.total_time,
# DISABLED:                     'percentage': (func.total_time / execution_time * 100) if execution_time > 0 else 0,
# DISABLED:                     'call_count': func.call_count,
# DISABLED:                     'average_time': func.average_time
# DISABLED:                 }
# DISABLED:                 for func in sorted_functions[:10]
# DISABLED:             ]

# DISABLED:             report['function_statistics'] = {
# DISABLED:                 'total_functions': len(profile.functions),
# DISABLED:                 'total_calls': sum(f.call_count for f in profile.functions.values()),
# DISABLED:                 'average_function_time': sum(f.total_time for f in profile.functions.values()) / len(profile.functions)
# DISABLED:             }

        # Memory analysis
# DISABLED:         if profile.memory_snapshots:
# DISABLED:             memory_values = [s.get('current_mb', 0) for s in profile.memory_snapshots]
# DISABLED:             report['memory_analysis'] = {
# DISABLED:                 'peak_memory_mb': max(memory_values) if memory_values else 0,
# DISABLED:                 'average_memory_mb': sum(memory_values) / len(memory_values) if memory_values else 0,
# DISABLED:                 'memory_snapshots_count': len(profile.memory_snapshots)
# DISABLED:             }

        # Thread analysis
# DISABLED:         if profile.thread_activity:
# DISABLED:             thread_activities = []
# DISABLED:             for thread_id, activities in profile.thread_activity.items():
# DISABLED:                 thread_activities.append({
# DISABLED:                     'thread_id': thread_id,
# DISABLED:                     'activity_count': len(activities),
# DISABLED:                     'activities': activities[:5]  # First 5 activities
# DISABLED:                 })

# DISABLED:             report['thread_analysis'] = thread_activities

        # Bottleneck analysis
# DISABLED:         report['bottleneck_analysis'] = self.analyze_performance_bottlenecks(profile)

# DISABLED:         return report

# DISABLED:     def export_profile_data(self, profile_id: str, filename: str, format: str = "json") -> bool:
        """Export profile data to file"""
# DISABLED:         with self.profile_lock:
# DISABLED:             profile = self.completed_profiles.get(profile_id)
# DISABLED:             if not profile:
# DISABLED:                 logger.error(f"Profile not found: {profile_id}")
# DISABLED:                 return False

# DISABLED:         try:
# DISABLED:             if format.lower() == "json":
# DISABLED:                 import json
# DISABLED:                 report = self.generate_performance_report(profile)
# DISABLED:                 with open(filename, 'w') as f:
# DISABLED:                     json.dump(report, f, indent=2, default=str)
# DISABLED:             else:
                # CSV format for function data
# DISABLED:                 import csv
# DISABLED:                 with open(filename, 'w', newline='') as f:
# DISABLED:                     writer = csv.writer(f)
# DISABLED:                     writer.writerow(['function_name', 'call_count', 'total_time', 'average_time', 'max_time', 'min_time', 'memory_usage_mb'])
# DISABLED:                     for func in profile.functions.values():
# DISABLED:                         writer.writerow([
# DISABLED:                             func.function_name,
# DISABLED:                             func.call_count,
# DISABLED:                             func.total_time,
# DISABLED:                             func.average_time,
# DISABLED:                             func.max_time,
# DISABLED:                             func.min_time,
# DISABLED:                             func.memory_usage_mb
# DISABLED:                         ])

# DISABLED:             logger.info(f"Profile data exported to {filename}")
# DISABLED:             return True

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Failed to export profile data: {e}")
# DISABLED:             return False

# DISABLED:     def cleanup_old_profiles(self, max_age_hours: int = 24):
        """Clean up old profile data"""
# DISABLED:         cutoff_time = time.time() - (max_age_hours * 3600)

# DISABLED:         with self.profile_lock:
# DISABLED:             old_profiles = [
# DISABLED:                 profile_id for profile_id, profile in self.completed_profiles.items()
# DISABLED:                 if profile.start_time < cutoff_time
# DISABLED:             ]

# DISABLED:             for profile_id in old_profiles:
# DISABLED:                 del self.completed_profiles[profile_id]

# DISABLED:             logger.info(f"Cleaned up {len(old_profiles)} old profiles")

# DISABLED:     def get_system_performance_summary(self) -> Dict[str, Any]:
        """Get summary of system performance across all profiles"""
# DISABLED:         with self.profile_lock:
# DISABLED:             all_profiles = list(self.active_profiles.values()) + list(self.completed_profiles.values())

# DISABLED:         if not all_profiles:
# DISABLED:             return {'message': 'No performance data available'}

        # Calculate statistics
# DISABLED:         execution_times = []
# DISABLED:         memory_peaks = []
# DISABLED:         function_counts = []

# DISABLED:         for profile in all_profiles:
# DISABLED:             if profile.end_time:
# DISABLED:                 execution_times.append(profile.end_time - profile.start_time)

# DISABLED:             if profile.memory_snapshots:
# DISABLED:                 memory_values = [s.get('current_mb', 0) for s in profile.memory_snapshots]
# DISABLED:                 memory_peaks.append(max(memory_values))

# DISABLED:             function_counts.append(len(profile.functions))

# DISABLED:         summary = {
# DISABLED:             'total_profiles': len(all_profiles),
# DISABLED:             'active_profiles': len(self.active_profiles),
# DISABLED:             'completed_profiles': len(self.completed_profiles)
# DISABLED:         }

# DISABLED:         if execution_times:
# DISABLED:             summary['execution_time_stats'] = {
# DISABLED:                 'average': sum(execution_times) / len(execution_times),
# DISABLED:                 'min': min(execution_times),
# DISABLED:                 'max': max(execution_times)
# DISABLED:             }

# DISABLED:         if memory_peaks:
# DISABLED:             summary['memory_peak_stats'] = {
# DISABLED:                 'average': sum(memory_peaks) / len(memory_peaks),
# DISABLED:                 'min': min(memory_peaks),
# DISABLED:                 'max': max(memory_peaks)
# DISABLED:             }

# DISABLED:         if function_counts:
# DISABLED:             summary['function_count_stats'] = {
# DISABLED:                 'average': sum(function_counts) / len(function_counts),
# DISABLED:                 'min': min(function_counts),
# DISABLED:                 'max': max(function_counts)
# DISABLED:             }

# DISABLED:         return summary


# DISABLED: class MemoryTracker:
    """Track memory usage for profiling"""

# DISABLED:     def __init__(self):
# DISABLED:         self.tracking = False
# DISABLED:         self.snapshots = []

# DISABLED:     def start_tracking(self):
        """Start memory tracking"""
# DISABLED:         if not self.tracking:
# DISABLED:             tracemalloc.start()
# DISABLED:             self.tracking = True

# DISABLED:     def stop_tracking(self):
        """Stop memory tracking"""
# DISABLED:         if self.tracking:
# DISABLED:             tracemalloc.stop()
# DISABLED:             self.tracking = False

# DISABLED:     def get_current_usage(self) -> Optional[float]:
        """Get current memory usage in MB"""
# DISABLED:         if self.tracing:
# DISABLED:             current, peak = tracemalloc.get_traced_memory()
# DISABLED:             return current / 1024 / 1024
# DISABLED:         return None

# DISABLED:     def get_current_snapshot(self) -> Optional[Dict[str, Any]]:
        """Get current memory snapshot"""
# DISABLED:         if self.tracking:
# DISABLED:             current, peak = tracemalloc.get_traced_memory()
# DISABLED:             return {
# DISABLED:                 'current_mb': current / 1024 / 1024,
# DISABLED:                 'peak_mb': peak / 1024 / 1024
# DISABLED:             }
# DISABLED:         return None


# DISABLED: class ThreadTracker:
    """Track thread activity for profiling"""

# DISABLED:     def __init__(self):
# DISABLED:         self.tracking = False
# DISABLED:         self.thread_activities = defaultdict(list)

# DISABLED:     def start_tracking(self):
        """Start thread tracking"""
# DISABLED:         self.tracking = True

# DISABLED:     def stop_tracking(self):
        """Stop thread tracking"""
# DISABLED:         self.tracking = False

# DISABLED:     def record_activity(self, thread_id: int, activity: str):
        """Record thread activity"""
# DISABLED:         if self.tracking:
# DISABLED:             self.thread_activities[thread_id].append({
# DISABLED:                 'timestamp': time.time(),
# DISABLED:                 'activity': activity
# DISABLED:             })


# DISABLED: def profile_function(job_id: str, name: Optional[str] = None):
    """Decorator for profiling functions"""
# DISABLED:     def decorator(func: Callable) -> Callable:
# DISABLED:         func_name = name or f"{func.__module__}.{func.__name__}"

# DISABLED:         @functools.wraps(func)
# DISABLED:         def wrapper(*args, **kwargs):
            # Get profiler instance
            # This would need to be injected or accessed via a singleton
# DISABLED:             profiler = getattr(wrapper, '_profiler', None)
# DISABLED:             if not profiler:
# DISABLED:                 return func(*args, **kwargs)

# DISABLED:             with profiler.profile_function(job_id, func_name):
# DISABLED:                 return func(*args, **kwargs)

# DISABLED:         return wrapper
# DISABLED:     return decorator