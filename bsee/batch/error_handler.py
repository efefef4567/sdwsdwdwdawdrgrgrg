"""
Batch Error Handler Implementation
Error handling and recovery mechanisms for batch job operations.
"""

import time
import traceback
import threading
import functools
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import json
from pathlib import Path

from ...utils.logger import get_logger

logger = get_logger(__name__)


class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """Error categories for classification"""
    CONFIGURATION = "configuration"
    RESOURCE = "resource"
    EXECUTION = "execution"
    IO = "io"
    NETWORK = "network"
    VALIDATION = "validation"
    SYSTEM = "system"
    UNKNOWN = "unknown"


@dataclass
class BatchError:
    """Represents a batch operation error"""
    error_id: str
    job_id: Optional[str]
    timestamp: float
    category: ErrorCategory
    severity: ErrorSeverity
    message: str
    exception: Optional[Exception]
    traceback_str: Optional[str]
    context: Dict[str, Any]
    retry_count: int = 0
    resolved: bool = False
    resolution_message: Optional[str] = None


class ErrorHandler:
    """Centralized error handling for batch operations"""

    def __init__(self, max_error_history: int = 1000):
        """
        Initialize error handler

        Args:
            max_error_history: Maximum number of errors to keep in memory
        """
        self.max_error_history = max_error_history
        self.errors: List[BatchError] = []
        self.error_callbacks: List[Callable[[BatchError], None]] = []
        self.error_handlers: Dict[ErrorCategory, List[Callable]] = {}
        self.recovery_strategies: Dict[ErrorCategory, List[Callable]] = {}
        self.error_lock = threading.Lock()

        # Error statistics
        self.error_stats = {
            'total_errors': 0,
            'by_category': {},
            'by_severity': {},
            'by_job': {},
            'resolved_count': 0
        }

        # Setup default handlers and recovery strategies
        self._setup_default_handlers()

    def _setup_default_handlers(self):
        """Setup default error handlers and recovery strategies"""
        # Configuration errors
        self.register_recovery_strategy(
            ErrorCategory.CONFIGURATION,
            self._handle_configuration_error
        )

        # Resource errors
        self.register_recovery_strategy(
            ErrorCategory.RESOURCE,
            self._handle_resource_error
        )

        # Execution errors
        self.register_recovery_strategy(
            ErrorCategory.EXECUTION,
            self._handle_execution_error
        )

        # I/O errors
        self.register_recovery_strategy(
            ErrorCategory.IO,
            self._handle_io_error
        )

        # Validation errors
        self.register_recovery_strategy(
            ErrorCategory.VALIDATION,
            self._handle_validation_error
        )

    def handle_error(
        self,
        error: Exception,
        job_id: Optional[str] = None,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[Dict[str, Any]] = None
    ) -> BatchError:
        """
        Handle an error that occurred during batch operations

        Args:
            error: The exception that occurred
            job_id: ID of the job where error occurred
            category: Error category
            severity: Error severity
            context: Additional context information

        Returns:
            BatchError object
        """
        import uuid

        error_id = str(uuid.uuid4())[:8]
        current_time = time.time()

        # Create error object
        batch_error = BatchError(
            error_id=error_id,
            job_id=job_id,
            timestamp=current_time,
            category=category,
            severity=severity,
            message=str(error),
            exception=error,
            traceback_str=traceback.format_exc(),
            context=context or {}
        )

        with self.error_lock:
            # Add to error history
            self.errors.append(batch_error)
            if len(self.errors) > self.max_error_history:
                self.errors.pop(0)

            # Update statistics
            self._update_error_stats(batch_error)

        # Log the error
        self._log_error(batch_error)

        # Notify callbacks
        for callback in self.error_callbacks:
            try:
                callback(batch_error)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")

        # Attempt recovery
        self._attempt_recovery(batch_error)

        return batch_error

    def register_error_callback(self, callback: Callable[[BatchError], None]):
        """Register a callback to be notified of errors"""
        self.error_callbacks.append(callback)

    def register_recovery_strategy(self, category: ErrorCategory, strategy: Callable):
        """Register a recovery strategy for an error category"""
        if category not in self.recovery_strategies:
            self.recovery_strategies[category] = []
        self.recovery_strategies[category].append(strategy)

    def get_errors(
        self,
        job_id: Optional[str] = None,
        category: Optional[ErrorCategory] = None,
        severity: Optional[ErrorSeverity] = None,
        resolved: Optional[bool] = None,
        limit: Optional[int] = None
    ) -> List[BatchError]:
        """
        Get filtered list of errors

        Args:
            job_id: Filter by job ID
            category: Filter by error category
            severity: Filter by severity
            resolved: Filter by resolution status
            limit: Maximum number of errors to return

        Returns:
            Filtered list of errors
        """
        with self.error_lock:
            filtered_errors = self.errors.copy()

        # Apply filters
        if job_id is not None:
            filtered_errors = [e for e in filtered_errors if e.job_id == job_id]

        if category is not None:
            filtered_errors = [e for e in filtered_errors if e.category == category]

        if severity is not None:
            filtered_errors = [e for e in filtered_errors if e.severity == severity]

        if resolved is not None:
            filtered_errors = [e for e in filtered_errors if e.resolved == resolved]

        # Sort by timestamp (newest first)
        filtered_errors.sort(key=lambda e: e.timestamp, reverse=True)

        # Apply limit
        if limit is not None:
            filtered_errors = filtered_errors[:limit]

        return filtered_errors

    def resolve_error(self, error_id: str, resolution_message: str):
        """Mark an error as resolved"""
        with self.error_lock:
            for error in self.errors:
                if error.error_id == error_id:
                    error.resolved = True
                    error.resolution_message = resolution_message
                    self.error_stats['resolved_count'] += 1
                    logger.info(f"Error {error_id} resolved: {resolution_message}")
                    break

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics"""
        with self.error_lock:
            return {
                'total_errors': self.error_stats['total_errors'],
                'resolved_errors': self.error_stats['resolved_count'],
                'unresolved_errors': self.error_stats['total_errors'] - self.error_stats['resolved_count'],
                'by_category': self.error_stats['by_category'].copy(),
                'by_severity': self.error_stats['by_severity'].copy(),
                'by_job': dict(sorted(self.error_stats['by_job'].items(), key=lambda x: x[1], reverse=True)[:10]),
                'error_rate': self._calculate_error_rate(),
                'common_errors': self._get_common_errors()
            }

    def export_errors(self, filename: str, format: str = "json") -> bool:
        """Export error log to file"""
        try:
            with self.error_lock:
                error_data = {
                    'export_timestamp': time.time(),
                    'total_errors': len(self.errors),
                    'statistics': self.get_error_statistics(),
                    'errors': [asdict(error) for error in self.errors]
                }

            if format.lower() == "json":
                with open(filename, 'w') as f:
                    json.dump(error_data, f, indent=2, default=str)
            else:
                # CSV format (simplified)
                import csv
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['error_id', 'job_id', 'timestamp', 'category', 'severity', 'message', 'resolved'])
                    for error in self.errors:
                        writer.writerow([
                            error.error_id,
                            error.job_id or '',
                            error.timestamp,
                            error.category.value,
                            error.severity.value,
                            error.message,
                            error.resolved
                        ])

            logger.info(f"Error log exported to {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to export error log: {e}")
            return False

    def _update_error_stats(self, error: BatchError):
        """Update error statistics"""
        self.error_stats['total_errors'] += 1

        # By category
        category_key = error.category.value
        self.error_stats['by_category'][category_key] = (
            self.error_stats['by_category'].get(category_key, 0) + 1
        )

        # By severity
        severity_key = error.severity.value
        self.error_stats['by_severity'][severity_key] = (
            self.error_stats['by_severity'].get(severity_key, 0) + 1
        )

        # By job
        if error.job_id:
            self.error_stats['by_job'][error.job_id] = (
                self.error_stats['by_job'].get(error.job_id, 0) + 1
            )

    def _log_error(self, error: BatchError):
        """Log error with appropriate level"""
        log_message = f"[{error.category.value.upper()}] {error.message}"
        if error.job_id:
            log_message += f" (Job: {error.job_id})"

        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(log_message)
        elif error.severity == ErrorSeverity.HIGH:
            logger.error(log_message)
        elif error.severity == ErrorSeverity.MEDIUM:
            logger.warning(log_message)
        else:
            logger.info(log_message)

    def _attempt_recovery(self, error: BatchError):
        """Attempt to recover from error"""
        if error.category in self.recovery_strategies:
            strategies = self.recovery_strategies[error.category]
            for strategy in strategies:
                try:
                    success = strategy(error)
                    if success:
                        self.resolve_error(error.error_id, f"Auto-recovered using strategy: {strategy.__name__}")
                        return True
                except Exception as e:
                    logger.error(f"Recovery strategy failed: {e}")

        return False

    def _handle_configuration_error(self, error: BatchError) -> bool:
        """Handle configuration errors"""
        # Check if it's a missing file error
        if "not found" in error.message.lower() or "does not exist" in error.message.lower():
            # Try to create missing configuration files
            try:
                if error.job_id:
                    # Attempt to create default configuration
                    self._create_default_config(error.job_id)
                    return True
            except Exception:
                pass

        return False

    def _handle_resource_error(self, error: BatchError) -> bool:
        """Handle resource-related errors"""
        if "memory" in error.message.lower():
            # Suggest memory optimization
            error.context['suggestion'] = "Reduce job memory requirements or increase system memory"
        elif "disk" in error.message.lower() or "space" in error.message.lower():
            # Suggest disk cleanup
            error.context['suggestion'] = "Clean up disk space or reduce output size"
        elif "timeout" in error.message.lower():
            # Suggest timeout adjustment
            error.context['suggestion'] = "Increase timeout limits or optimize algorithm"

        return False  # Don't auto-resolve resource errors

    def _handle_execution_error(self, error: BatchError) -> bool:
        """Handle execution errors"""
        if error.retry_count < 3:
            # Retry the operation
            error.retry_count += 1
            error.context['retry_scheduled'] = True
            return True

        return False

    def _handle_io_error(self, error: BatchError) -> bool:
        """Handle I/O errors"""
        # Check if it's a permission error
        if "permission" in error.message.lower():
            error.context['suggestion'] = "Check file permissions and access rights"
        elif "locked" in error.message.lower() or "in use" in error.message.lower():
            error.context['suggestion'] = "File is locked, try again later"
            return True  # Retry I/O errors

        return False

    def _handle_validation_error(self, error: BatchError) -> bool:
        """Handle validation errors"""
        # Don't auto-resolve validation errors, but provide suggestions
        error.context['suggestion'] = "Check input configuration and data format"
        return False

    def _create_default_config(self, job_id: str):
        """Create default configuration for a job"""
        # This would create default configuration files
        # Implementation depends on specific configuration structure
        pass

    def _calculate_error_rate(self) -> float:
        """Calculate recent error rate (errors per hour)"""
        if not self.errors:
            return 0.0

        current_time = time.time()
        one_hour_ago = current_time - 3600

        recent_errors = [
            error for error in self.errors
            if error.timestamp >= one_hour_ago
        ]

        return len(recent_errors)

    def _get_common_errors(self) -> List[Dict[str, Any]]:
        """Get most common errors"""
        error_messages = {}
        for error in self.errors:
            message = error.message
            if message not in error_messages:
                error_messages[message] = 0
            error_messages[message] += 1

        # Sort by frequency
        common_errors = sorted(
            error_messages.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5

        return [
            {'message': message, 'count': count}
            for message, count in common_errors
        ]

    def cleanup_old_errors(self, max_age_hours: int = 24):
        """Clean up old error records"""
        cutoff_time = time.time() - (max_age_hours * 3600)

        with self.error_lock:
            old_errors = [
                error for error in self.errors
                if error.timestamp < cutoff_time
            ]

            for error in old_errors:
                self.errors.remove(error)

            logger.info(f"Cleaned up {len(old_errors)} old error records")


class ErrorContext:
    """Context manager for handling errors in batch operations"""

    def __init__(
        self,
        error_handler: ErrorHandler,
        job_id: Optional[str] = None,
        category: ErrorCategory = ErrorCategory.UNKNOWN,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: Optional[Dict[str, Any]] = None
    ):
        self.error_handler = error_handler
        self.job_id = job_id
        self.category = category
        self.severity = severity
        self.context = context or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and issubclass(exc_type, Exception):
            self.error_handler.handle_error(
                error=exc_val,
                job_id=self.job_id,
                category=self.category,
                severity=self.severity,
                context=self.context
            )
            return True  # Suppress the exception
        return False


def handle_batch_errors(
    error_handler: ErrorHandler,
    job_id: Optional[str] = None,
    category: ErrorCategory = ErrorCategory.UNKNOWN,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    context: Optional[Dict[str, Any]] = None
):
    """Decorator for automatic error handling"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_handler.handle_error(
                    error=e,
                    job_id=job_id,
                    category=category,
                    severity=severity,
                    context=context
                )
                raise  # Re-raise the exception after handling
        return wrapper
    return decorator