"""
Folder Monitor Implementation
Watchdog-based file system monitoring for automatic job discovery.
"""

import os
import time
import threading
from typing import Callable, Optional, Set
from pathlib import Path
from enum import Enum

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False

from bsee.utils.logger import get_logger

logger = get_logger(__name__)


class FolderEventType(Enum):
    """Folder event types"""
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"
    MOVED = "moved"


class BatchFolderEventHandler(FileSystemEventHandler):
    """Event handler for batch job folder monitoring"""

    def __init__(self, callback: Callable[[str, FolderEventType], None]):
        """
        Initialize event handler

        Args:
            callback: Callback function called when folder events occur
                      Signature: callback(folder_path: str, event_type: FolderEventType)
        """
        super().__init__()
        self.callback = callback
        self.debounce_times = {}  # Debounce rapid events
        self.debounce_interval = 1.0  # seconds

    def on_created(self, event):
        """Handle folder creation events"""
        if event.is_directory:
            self._handle_event(event.src_path, FolderEventType.CREATED)

    def on_modified(self, event):
        """Handle folder modification events"""
        if event.is_directory:
            self._handle_event(event.src_path, FolderEventType.MODIFIED)

    def on_deleted(self, event):
        """Handle folder deletion events"""
        if event.is_directory:
            self._handle_event(event.src_path, FolderEventType.DELETED)

    def on_moved(self, event):
        """Handle folder move events"""
        if event.is_directory:
            self._handle_event(event.src_path, FolderEventType.MOVED)
            self._handle_event(event.dest_path, FolderEventType.CREATED)

    def _handle_event(self, folder_path: str, event_type: FolderEventType):
        """Handle folder event with debouncing"""
        try:
            current_time = time.time()
            folder_key = str(Path(folder_path).absolute())

            # Debounce rapid events for same folder
            if (folder_key in self.debounce_times and
                current_time - self.debounce_times[folder_key] < self.debounce_interval):
                return

            self.debounce_times[folder_key] = current_time

            # Call callback
            try:
                self.callback(folder_path, event_type)
            except Exception as e:
                logger.error(f"Error in folder monitor callback: {e}")

        except Exception as e:
            logger.error(f"Error handling folder event: {e}")


class FolderMonitor:
    """Monitor batch_jobs directory for new jobs"""

    def __init__(self, monitor_path: str, callback: Callable[[str], None]):
        """
        Initialize folder monitor

        Args:
            monitor_path: Path to directory to monitor
            callback: Callback function when new folder detected
                      Signature: callback(folder_path: str)
        """
        self.monitor_path = Path(monitor_path).absolute()
        self.callback = callback
        self.observer: Optional[Observer] = None
        self.monitor_thread: Optional[threading.Thread] = None
        self.running = False
        self.event_handler: Optional[BatchFolderEventHandler] = None

        # Fallback polling settings
        self.poll_interval = 2.0  # seconds
        self.known_folders: Set[str] = set()

        logger.info(f"Folder monitor initialized for: {self.monitor_path}")

    def start(self):
        """Start monitoring"""
        if self.running:
            return

        self.running = True

        if WATCHDOG_AVAILABLE:
            self._start_watchdog_monitoring()
        else:
            self._start_polling_monitoring()

        logger.info(f"Started folder monitoring: {self.monitor_path}")

    def stop(self):
        """Stop monitoring"""
        if not self.running:
            return

        self.running = False

        if self.observer:
            self.observer.stop()
            self.observer.join()

        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)

        logger.info(f"Stopped folder monitoring: {self.monitor_path}")

    def _start_watchdog_monitoring(self):
        """Start watchdog-based monitoring"""
        try:
            self.event_handler = BatchFolderEventHandler(
                lambda path, event_type: self._handle_folder_event(path, event_type)
            )

            self.observer = Observer()
            self.observer.schedule(
                self.event_handler,
                str(self.monitor_path),
                recursive=True
            )
            self.observer.start()

            # Initialize known folders
            self._scan_existing_folders()

            logger.info("Started watchdog-based folder monitoring")

        except Exception as e:
            logger.error(f"Failed to start watchdog monitoring: {e}")
            self._start_polling_monitoring()

    def _start_polling_monitoring(self):
        """Start polling-based monitoring (fallback)"""
        self.monitor_thread = threading.Thread(
            target=self._polling_loop,
            daemon=True
        )
        self.monitor_thread.start()

        # Initialize known folders
        self._scan_existing_folders()

        logger.info("Started polling-based folder monitoring")

    def _polling_loop(self):
        """Polling loop for monitoring"""
        while self.running:
            try:
                self._scan_for_new_folders()
                time.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"Error in polling loop: {e}")
                time.sleep(self.poll_interval)

    def _scan_existing_folders(self):
        """Scan for existing folders"""
        try:
            if not self.monitor_path.exists():
                return

            self.known_folders.clear()
            for item in self.monitor_path.iterdir():
                if item.is_dir():
                    self.known_folders.add(str(item))

        except Exception as e:
            logger.error(f"Error scanning existing folders: {e}")

    def _scan_for_new_folders(self):
        """Scan for new folders"""
        try:
            if not self.monitor_path.exists():
                return

            current_folders = set()
            for item in self.monitor_path.iterdir():
                if item.is_dir():
                    current_folders.add(str(item))

            # Find new folders
            new_folders = current_folders - self.known_folders
            for folder_path in new_folders:
                self._handle_folder_event(folder_path, FolderEventType.CREATED)

            # Find deleted folders
            deleted_folders = self.known_folders - current_folders
            for folder_path in deleted_folders:
                self._handle_folder_event(folder_path, FolderEventType.DELETED)

            self.known_folders = current_folders

        except Exception as e:
            logger.error(f"Error scanning for new folders: {e}")

    def _handle_folder_event(self, folder_path: str, event_type: FolderEventType):
        """Handle folder events"""
        try:
            folder_path = str(Path(folder_path).absolute())

            if event_type == FolderEventType.CREATED:
                # Check if it's a valid job folder
                if self._is_valid_job_folder(folder_path):
                    logger.info(f"Detected new job folder: {folder_path}")
                    try:
                        self.callback(folder_path)
                    except Exception as e:
                        logger.error(f"Error in folder callback for {folder_path}: {e}")
                else:
                    logger.debug(f"Ignored non-job folder: {folder_path}")

            elif event_type == FolderEventType.DELETED:
                logger.info(f"Job folder deleted: {folder_path}")

            elif event_type == FolderEventType.MODIFIED:
                # Check if folder became valid after modification
                if self._is_valid_job_folder(folder_path):
                    logger.info(f"Job folder modified and is now valid: {folder_path}")
                    try:
                        self.callback(folder_path)
                    except Exception as e:
                        logger.error(f"Error in folder callback for {folder_path}: {e}")

        except Exception as e:
            logger.error(f"Error handling folder event: {e}")

    def _is_valid_job_folder(self, folder_path: str) -> bool:
        """Check if folder is a valid job folder"""
        try:
            folder = Path(folder_path)

            if not folder.is_dir():
                return False

            # Check for required configuration files
            required_files = ['config.yaml']
            optional_files = ['strategy.yaml', 'cost_model.yaml', 'metrics.yaml']

            # Check for required files
            for required_file in required_files:
                if not (folder / required_file).exists():
                    return False

            # Check for at least one optional file (to avoid false positives)
            has_optional = any((folder / f).exists() for f in optional_files)
            if not has_optional:
                logger.debug(f"Folder {folder_path} missing optional job files")
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating job folder {folder_path}: {e}")
            return False

    def get_status(self) -> dict:
        """Get monitor status"""
        return {
            'running': self.running,
            'monitor_path': str(self.monitor_path),
            'monitoring_type': 'watchdog' if WATCHDOG_AVAILABLE and self.observer else 'polling',
            'known_folders': len(self.known_folders),
            'watchdog_available': WATCHDOG_AVAILABLE
        }