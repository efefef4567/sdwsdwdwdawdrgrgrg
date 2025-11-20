"""
Job Manager Implementation
Central job management and orchestration for BSEE batch processing.
"""

import os
import time
import threading
from typing import Dict, List, Optional, Callable, Set
from collections import defaultdict, deque
import queue
import json
from pathlib import Path

from .job import Job, JobStatus, JobPriority
from .folder_monitor import FolderMonitor
from .job_validator import JobValidator
from bsee.processing.parallel_processor import ParallelProcessor
from bsee.utils.logger import get_logger

logger = get_logger(__name__)


class JobManager:
    """Central job management and orchestration system"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern implementation"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize job manager"""
        if hasattr(self, '_initialized'):
            return

        self._initialized = True
        self.jobs: Dict[str, Job] = {}
        self.job_queue = queue.PriorityQueue()
        self.running_jobs: Dict[str, Job] = {}
        self.max_concurrent_jobs = 4
        self.auto_start = False
        self.execution_lock = threading.Lock()

        # Threading
        self.worker_threads: List[threading.Thread] = []
        self.shutdown_event = threading.Event()
        self.manager_thread: Optional[threading.Thread] = None

        # Event callbacks
        self.job_callbacks: List[Callable] = []

        # Components
        self.parallel_processor = ParallelProcessor()
        self.folder_monitor: Optional[FolderMonitor] = None
        self.job_validator = JobValidator()

        # Configuration
        self.batch_jobs_dir = Path.cwd() / 'batch_jobs'
        self.batch_jobs_dir.mkdir(exist_ok=True)

        # Start the manager thread
        self._start_manager_thread()

    def _start_manager_thread(self):
        """Start the background job manager thread"""
        if self.manager_thread is None or not self.manager_thread.is_alive():
            self.shutdown_event.clear()
            self.manager_thread = threading.Thread(target=self._manager_loop, daemon=True)
            self.manager_thread.start()
            logger.info("Job manager thread started")

    def _manager_loop(self):
        """Background thread for managing job execution"""
        while not self.shutdown_event.is_set():
            try:
                self._process_job_queue()
                self._update_running_jobs()
                time.sleep(0.1)  # Check every 100ms

            except Exception as e:
                logger.error(f"Job manager error: {e}")
                time.sleep(1)  # Wait before retrying

    def _process_job_queue(self):
        """Process queued jobs and start execution if resources available"""
        with self.execution_lock:
            # Check if we can start more jobs
            if len(self.running_jobs) >= self.max_concurrent_jobs:
                return

            # Get jobs from queue (ordered by priority)
            while len(self.running_jobs) < self.max_concurrent_jobs and not self.job_queue.empty():
                try:
                    priority_value, job_id, job = self.job_queue.get_nowait()

                    if job.status != JobStatus.QUEUED:
                        continue  # Skip if job status changed

                    # Start the job
                    self._start_job(job)

                except queue.Empty:
                    break
                except Exception as e:
                    logger.error(f"Error processing job queue: {e}")

    def _update_running_jobs(self):
        """Update status of running jobs and handle completion"""
        completed_jobs = []

        for job_id, job in self.running_jobs.items():
            try:
                # Check if job completed
                if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                    completed_jobs.append(job_id)
                    self._notify_job_update(job)

                # Update job status file
                job.save_status()

            except Exception as e:
                logger.error(f"Error updating running job {job_id}: {e}")

        # Remove completed jobs from running list
        for job_id in completed_jobs:
            del self.running_jobs[job_id]

    def _start_job(self, job: Job):
        """Start execution of a job"""
        try:
            job.prepare_execution()
            self.running_jobs[job.job_id] = job

            # Start job in separate thread
            job_thread = threading.Thread(
                target=self._execute_job_thread,
                args=(job,),
                daemon=True,
                name=f"Job-{job.job_id}"
            )
            job_thread.start()

            self._notify_job_update(job)
            logger.info(f"Started job execution: {job.job_id}")

        except Exception as e:
            job.status = JobStatus.FAILED
            job.error_message = f"Failed to start job: {str(e)}"
            logger.error(f"Failed to start job {job.job_id}: {e}")
            self._notify_job_update(job)

    def _execute_job_thread(self, job: Job):
        """Thread function for executing a job"""
        try:
            success = job.execute()
            if success:
                logger.info(f"Job {job.job_id} completed successfully")
            else:
                logger.error(f"Job {job.job_id} failed")

        except Exception as e:
            logger.error(f"Job execution thread error for {job.job_id}: {e}")
            job.status = JobStatus.FAILED
            job.error_message = f"Execution error: {str(e)}"

        finally:
            self._notify_job_update(job)

    def add_job(self, job_folder: str, job_id: Optional[str] = None) -> Optional[Job]:
        """
        Add a job from folder path

        Args:
            job_folder: Path to job configuration folder
            job_id: Optional explicit job ID

        Returns:
            Job object if successful, None otherwise
        """
        try:
            # Validate job configuration
            if not self.job_validator.validate_job_folder(job_folder):
                raise ValueError(f"Invalid job folder: {job_folder}")

            # Create job
            job = Job(job_folder, job_id)

            # Check if job already exists
            if job.job_id in self.jobs:
                raise ValueError(f"Job already exists: {job.job_id}")

            # Add to jobs collection
            self.jobs[job.job_id] = job

            # Add status callback
            job.add_status_callback(self._notify_job_update)

            # Queue job if auto-start is enabled, otherwise mark as pending
            if self.auto_start:
                self.queue_job(job.job_id)
            else:
                job.status = JobStatus.PENDING

            self._notify_job_update(job)
            logger.info(f"Added job: {job.job_id} from {job_folder}")
            return job

        except Exception as e:
            logger.error(f"Failed to add job from {job_folder}: {e}")
            return None

    def remove_job(self, job_id: str) -> bool:
        """
        Remove a job and cleanup resources

        Args:
            job_id: Job ID to remove

        Returns:
            bool: True if successful
        """
        try:
            job = self.jobs.get(job_id)
            if not job:
                return False

            # Cancel job if running
            job.cancel()

            # Remove from jobs collection
            del self.jobs[job_id]

            # Remove from running jobs
            if job_id in self.running_jobs:
                del self.running_jobs[job_id]

            self._notify_job_update(job)
            logger.info(f"Removed job: {job_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to remove job {job_id}: {e}")
            return False

    def queue_job(self, job_id: str, scheduled_time: Optional[float] = None) -> bool:
        """
        Queue a job for execution

        Args:
            job_id: Job ID to queue
            scheduled_time: Optional timestamp for scheduled execution

        Returns:
            bool: True if successful
        """
        try:
            job = self.jobs.get(job_id)
            if not job:
                return False

            if scheduled_time and scheduled_time > time.time():
                job.scheduled_time = scheduled_time
                # TODO: Implement scheduled execution timer

            # Add to priority queue (negative priority for max-heap behavior)
            priority = -job.priority.value
            self.job_queue.put((priority, job_id, job))

            job.status = JobStatus.QUEUED
            job.queued_time = time.time()

            self._notify_job_update(job)
            logger.info(f"Queued job: {job_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to queue job {job_id}: {e}")
            return False

    def start_job(self, job_id: str) -> bool:
        """Start a specific job immediately"""
        try:
            job = self.jobs.get(job_id)
            if not job:
                return False

            if job.status in [JobStatus.PENDING, JobStatus.PAUSED]:
                return self.queue_job(job_id)

            return False

        except Exception as e:
            logger.error(f"Failed to start job {job_id}: {e}")
            return False

    def pause_job(self, job_id: str) -> bool:
        """Pause a running job"""
        try:
            job = self.jobs.get(job_id)
            if not job:
                return False

            job.pause()
            self._notify_job_update(job)
            return True

        except Exception as e:
            logger.error(f"Failed to pause job {job_id}: {e}")
            return False

    def resume_job(self, job_id: str) -> bool:
        """Resume a paused job"""
        try:
            job = self.jobs.get(job_id)
            if not job:
                return False

            job.resume()
            self._notify_job_update(job)
            return True

        except Exception as e:
            logger.error(f"Failed to resume job {job_id}: {e}")
            return False

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        try:
            job = self.jobs.get(job_id)
            if not job:
                return False

            job.cancel()
            self._notify_job_update(job)
            return True

        except Exception as e:
            logger.error(f"Failed to cancel job {job_id}: {e}")
            return False

    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        return self.jobs.get(job_id)

    def get_all_jobs(self) -> List[Job]:
        """Get all jobs"""
        return list(self.jobs.values())

    def get_jobs_by_status(self, status: JobStatus) -> List[Job]:
        """Get jobs filtered by status"""
        return [job for job in self.jobs.values() if job.status == status]

    def get_system_resources(self) -> Dict[str, float]:
        """Get overall system resource usage"""
        try:
            import psutil

            # Calculate total resources used by all running jobs
            total_cpu = sum(job.resources.cpu_percent for job in self.running_jobs.values())
            total_memory = sum(job.resources.memory_mb for job in self.running_jobs.values())

            return {
                'cpu_percent': min(100.0, total_cpu),
                'memory_mb': total_memory,
                'active_jobs': len(self.running_jobs),
                'max_concurrent': self.max_concurrent_jobs,
                'queue_length': self.job_queue.qsize(),
                'system_cpu': psutil.cpu_percent(),
                'system_memory': psutil.virtual_memory().percent
            }

        except Exception as e:
            logger.error(f"Error getting system resources: {e}")
            return {
                'cpu_percent': 0.0,
                'memory_mb': 0.0,
                'active_jobs': 0,
                'max_concurrent': self.max_concurrent_jobs,
                'queue_length': 0,
                'system_cpu': 0.0,
                'system_memory': 0.0
            }

    def set_max_concurrent_jobs(self, count: int):
        """Set maximum number of concurrent jobs"""
        self.max_concurrent_jobs = max(1, count)
        logger.info(f"Set max concurrent jobs to: {self.max_concurrent_jobs}")

    def set_auto_start(self, enabled: bool):
        """Set auto-start behavior for new jobs"""
        self.auto_start = enabled
        logger.info(f"Auto-start set to: {enabled}")

    def start_folder_monitoring(self):
        """Start monitoring batch_jobs directory for new jobs"""
        if self.folder_monitor is None:
            self.folder_monitor = FolderMonitor(
                self.batch_jobs_dir,
                callback=self._on_folder_detected
            )
            self.folder_monitor.start()
            logger.info("Started folder monitoring")

    def stop_folder_monitoring(self):
        """Stop folder monitoring"""
        if self.folder_monitor:
            self.folder_monitor.stop()
            self.folder_monitor = None
            logger.info("Stopped folder monitoring")

    def _on_folder_detected(self, folder_path: str):
        """Callback when new folder detected"""
        try:
            # Auto-add job if it's valid
            job = self.add_job(folder_path)
            if job:
                logger.info(f"Auto-detected and added job from: {folder_path}")
            else:
                logger.warning(f"Invalid job folder detected: {folder_path}")
        except Exception as e:
            logger.error(f"Error handling detected folder {folder_path}: {e}")

    def add_job_callback(self, callback: Callable):
        """Add callback for job updates"""
        self.job_callbacks.append(callback)

    def remove_job_callback(self, callback: Callable):
        """Remove job update callback"""
        if callback in self.job_callbacks:
            self.job_callbacks.remove(callback)

    def _notify_job_update(self, job: Job):
        """Notify all callbacks of job update"""
        for callback in self.job_callbacks:
            try:
                callback(job)
            except Exception as e:
                logger.error(f"Job callback error: {e}")

    def shutdown(self):
        """Shutdown job manager and cleanup resources"""
        logger.info("Shutting down job manager")

        # Stop folder monitoring
        self.stop_folder_monitoring()

        # Cancel all jobs
        for job in self.jobs.values():
            job.cancel()

        # Wait for running jobs to finish (with timeout)
        shutdown_timeout = 30
        start_time = time.time()

        while self.running_jobs and (time.time() - start_time) < shutdown_timeout:
            time.sleep(0.1)

        # Set shutdown event
        self.shutdown_event.set()

        # Wait for manager thread
        if self.manager_thread and self.manager_thread.is_alive():
            self.manager_thread.join(timeout=5)

        logger.info("Job manager shutdown complete")

    def get_statistics(self) -> Dict[str, Any]:
        """Get job manager statistics"""
        status_counts = defaultdict(int)
        for job in self.jobs.values():
            status_counts[job.status.value] += 1

        return {
            'total_jobs': len(self.jobs),
            'status_counts': dict(status_counts),
            'running_jobs': len(self.running_jobs),
            'queue_length': self.job_queue.qsize(),
            'max_concurrent_jobs': self.max_concurrent_jobs,
            'auto_start': self.auto_start,
            'system_resources': self.get_system_resources()
        }