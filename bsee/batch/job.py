"""
Batch Job Implementation
Individual job representation and execution logic for BSEE batch processing.
"""

import os
import time
import yaml
import json
import threading
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import uuid

from bsee.processing.parallel_processor import ParallelProcessor
from bsee.engine.pipeline import Pipeline
from bsee.utils.logger import get_logger

logger = get_logger(__name__)


class JobStatus(Enum):
    """Job execution status"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobPriority(Enum):
    """Job execution priority"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


@dataclass
class JobResource:
    """Resource usage tracking for a job"""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    disk_usage_mb: float = 0.0
    active_threads: int = 0
    peak_memory_mb: float = 0.0
    total_execution_time: float = 0.0


@dataclass
class JobConfiguration:
    """Job configuration loaded from YAML files"""
    job_id: str
    name: str
    description: str = ""
    strategy_config: Dict[str, Any] = field(default_factory=dict)
    cost_model: Dict[str, Any] = field(default_factory=dict)
    metrics_config: Dict[str, Any] = field(default_factory=dict)
    queue_settings: Dict[str, Any] = field(default_factory=dict)
    pipeline_config: Dict[str, Any] = field(default_factory=dict)
    resource_limits: Dict[str, Any] = field(default_factory=dict)


class Job:
    """Represents a single batch analysis job"""

    def __init__(self, job_folder: str, job_id: Optional[str] = None):
        """
        Initialize job from folder path

        Args:
            job_folder: Path to job configuration folder
            job_id: Optional explicit job ID (auto-generated if not provided)
        """
        self.job_id = job_id or str(uuid.uuid4())[:8]
        self.job_folder = Path(job_folder).absolute()
        self.name = self.job_folder.name
        self.status = JobStatus.PENDING
        self.priority = JobPriority.NORMAL

        # Timing information
        self.created_time = time.time()
        self.started_time: Optional[float] = None
        self.completed_time: Optional[float] = None
        self.queued_time: Optional[float] = None
        self.scheduled_time: Optional[float] = None

        # Execution state
        self.config: Optional[JobConfiguration] = None
        self.pipeline: Optional[Pipeline] = None
        self.progress = 0.0
        self.current_stage = "initialization"
        self.error_message: Optional[str] = None

        # Resource tracking
        self.resources = JobResource()
        self.resource_lock = threading.Lock()

        # Results and logs
        self.results_folder = Path.cwd() / 'results' / self.name
        self.logs: List[str] = []
        self.log_lock = threading.Lock()

        # Callbacks for status updates
        self.status_callbacks: List[Callable] = []

        # Load configuration
        self._load_configuration()

    def _load_configuration(self):
        """Load job configuration from YAML files"""
        try:
            # Main config file
            config_file = self.job_folder / 'config.yaml'
            if not config_file.exists():
                raise FileNotFoundError(f"Job config not found: {config_file}")

            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)

            # Load additional configuration files
            strategy_file = self.job_folder / 'strategy.yaml'
            cost_file = self.job_folder / 'cost_model.yaml'
            metrics_file = self.job_folder / 'metrics.yaml'
            queue_file = self.job_folder / 'queue_settings.yaml'
            pipeline_file = self.job_folder / 'pipeline_config.yaml'
            resource_file = self.job_folder / 'resource_limits.yaml'

            self.config = JobConfiguration(
                job_id=self.job_id,
                name=config_data.get('name', self.name),
                description=config_data.get('description', ''),
                strategy_config=yaml.safe_load(strategy_file) if strategy_file.exists() else {},
                cost_model=yaml.safe_load(cost_file) if cost_file.exists() else {},
                metrics_config=yaml.safe_load(metrics_file) if metrics_file.exists() else {},
                queue_settings=yaml.safe_load(queue_file) if queue_file.exists() else {},
                pipeline_config=yaml.safe_load(pipeline_file) if pipeline_file.exists() else {},
                resource_limits=yaml.safe_load(resource_file) if resource_file.exists() else {}
            )

            # Extract priority from queue settings
            priority_name = self.config.queue_settings.get('priority', 'normal').upper()
            if priority_name in JobPriority.__members__:
                self.priority = JobPriority[priority_name]

            self._log(f"Configuration loaded from {self.job_folder}")

        except Exception as e:
            self.error_message = f"Failed to load configuration: {str(e)}"
            self.status = JobStatus.FAILED
            self._log(f"Configuration loading failed: {e}")
            raise

    def prepare_execution(self):
        """Prepare job for execution by setting up pipeline and resources"""
        try:
            self._log("Preparing job execution")
            self.status = JobStatus.QUEUED
            self.queued_time = time.time()

            # Create results folder
            self.results_folder.mkdir(parents=True, exist_ok=True)

            # Initialize pipeline with configuration
            self.pipeline = Pipeline(
                strategy_config=self.config.strategy_config,
                cost_model=self.config.cost_model,
                metrics_config=self.config.metrics_config,
                **self.config.pipeline_config
            )

            self._notify_status_change()

        except Exception as e:
            self.error_message = f"Failed to prepare execution: {str(e)}"
            self.status = JobStatus.FAILED
            self._log(f"Execution preparation failed: {e}")
            raise

    def execute(self) -> bool:
        """
        Execute the job analysis

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._log(f"Starting job execution")
            self.status = JobStatus.RUNNING
            self.started_time = time.time()
            self.current_stage = "analysis"
            self._notify_status_change()

            # Start resource monitoring
            monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
            monitor_thread.start()

            # Execute pipeline
            with self.resource_lock:
                input_files = list(Path.cwd().glob('inputs/*'))
                if not input_files:
                    raise ValueError("No input files found in inputs directory")

                # Execute analysis
                results = self.pipeline.analyze_files(input_files, progress_callback=self._update_progress)

                # Save results
                self._save_results(results)

            # Complete job
            self.status = JobStatus.COMPLETED
            self.completed_time = time.time()
            self.current_stage = "completed"
            self.progress = 100.0

            self._log(f"Job completed successfully in {self.completed_time - self.started_time:.2f}s")
            self._notify_status_change()
            return True

        except Exception as e:
            self.error_message = f"Job execution failed: {str(e)}"
            self.status = JobStatus.FAILED
            self.completed_time = time.time()
            self.current_stage = "failed"

            self._log(f"Job execution failed: {e}")
            self._notify_status_change()
            return False

    def pause(self):
        """Pause job execution"""
        if self.status == JobStatus.RUNNING:
            self.status = JobStatus.PAUSED
            self._log("Job paused")
            self._notify_status_change()

    def resume(self):
        """Resume job execution"""
        if self.status == JobStatus.PAUSED:
            self.status = JobStatus.RUNNING
            self._log("Job resumed")
            self._notify_status_change()

    def cancel(self):
        """Cancel job execution"""
        if self.status in [JobStatus.PENDING, JobStatus.QUEUED, JobStatus.RUNNING, JobStatus.PAUSED]:
            self.status = JobStatus.CANCELLED
            self.completed_time = time.time()
            self._log("Job cancelled")
            self._notify_status_change()

    def _update_progress(self, progress: float, stage: str = None):
        """Update job progress and current stage"""
        self.progress = min(100.0, max(0.0, progress))
        if stage:
            self.current_stage = stage
        self._notify_status_change()

    def _monitor_resources(self):
        """Monitor job resource usage in background"""
        try:
            import psutil
            process = psutil.Process()

            while self.status in [JobStatus.RUNNING]:
                with self.resource_lock:
                    self.resources.cpu_percent = process.cpu_percent()
                    memory_info = process.memory_info()
                    self.resources.memory_mb = memory_info.rss / 1024 / 1024
                    self.resources.peak_memory_mb = max(self.resources.peak_memory_mb, self.resources.memory_mb)
                    self.resources.active_threads = process.num_threads()

                time.sleep(1)  # Update every second

        except Exception as e:
            self._log(f"Resource monitoring error: {e}")

    def _save_results(self, results: Dict[str, Any]):
        """Save analysis results to results folder"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        results_file = self.results_folder / f"results_{timestamp}.json"

        result_data = {
            'job_id': self.job_id,
            'job_name': self.name,
            'execution_time': self.completed_time - self.started_time if self.started_time else 0,
            'timestamp': timestamp,
            'results': results,
            'resources': {
                'peak_memory_mb': self.resources.peak_memory_mb,
                'total_execution_time': self.resources.total_execution_time
            }
        }

        with open(results_file, 'w') as f:
            json.dump(result_data, f, indent=2)

        self._log(f"Results saved to {results_file}")

    def _log(self, message: str):
        """Add message to job log"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"

        with self.log_lock:
            self.logs.append(log_entry)
            # Keep only last 1000 log entries
            if len(self.logs) > 1000:
                self.logs = self.logs[-1000:]

        logger.info(f"Job {self.job_id}: {message}")

    def _notify_status_change(self):
        """Notify all callbacks of status change"""
        for callback in self.status_callbacks:
            try:
                callback(self)
            except Exception as e:
                logger.error(f"Status callback error: {e}")

    def add_status_callback(self, callback: Callable):
        """Add callback for status updates"""
        self.status_callbacks.append(callback)

    def remove_status_callback(self, callback: Callable):
        """Remove status callback"""
        if callback in self.status_callbacks:
            self.status_callbacks.remove(callback)

    def get_status_dict(self) -> Dict[str, Any]:
        """Get job status as dictionary for GUI display"""
        return {
            'job_id': self.job_id,
            'name': self.name,
            'status': self.status.value,
            'priority': self.priority.value,
            'progress': self.progress,
            'current_stage': self.current_stage,
            'error_message': self.error_message,
            'created_time': self.created_time,
            'started_time': self.started_time,
            'completed_time': self.completed_time,
            'execution_time': (self.completed_time - self.started_time) if self.started_time and self.completed_time else 0,
            'resources': {
                'cpu_percent': self.resources.cpu_percent,
                'memory_mb': self.resources.memory_mb,
                'peak_memory_mb': self.resources.peak_memory_mb,
                'active_threads': self.resources.active_threads
            },
            'folder': str(self.job_folder),
            'results_folder': str(self.results_folder)
        }

    def save_status(self):
        """Save current job status to status.json file"""
        status_file = self.job_folder / 'status.json'
        try:
            with open(status_file, 'w') as f:
                json.dump(self.get_status_dict(), f, indent=2)
        except Exception as e:
            self._log(f"Failed to save status: {e}")