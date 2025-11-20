"""
# DISABLED: Folder Monitor Implementation
# DISABLED: Watchdog-based file system monitoring for automatic job discovery.
"""

# DISABLED: import os
# DISABLED: import time
# DISABLED: import threading
# DISABLED: from typing import Callable, Optional, Set
# DISABLED: from pathlib import Path
# DISABLED: from enum import Enum

# DISABLED: try:
# DISABLED:     from watchdog.observers import Observer
# DISABLED:     from watchdog.events import FileSystemEventHandler
# DISABLED:     WATCHDOG_AVAILABLE = True
# DISABLED: except ImportError:
# DISABLED:     WATCHDOG_AVAILABLE = False

# DISABLED: from bsee.utils.logger import get_logger

# DISABLED: logger = get_logger(__name__)


# DISABLED: class FolderEventType(Enum):
    """Folder event types"""
# DISABLED:     CREATED = "created"
# DISABLED:     MODIFIED = "modified"
# DISABLED:     DELETED = "deleted"
# DISABLED:     MOVED = "moved"


# DISABLED: class BatchFolderEventHandler(FileSystemEventHandler):
    """Event handler for batch job folder monitoring"""

# DISABLED:     def __init__(self, callback: Callable[[str, FolderEventType], None]):
        """
# DISABLED:         Initialize event handler

# DISABLED:         Args:
# DISABLED:             callback: Callback function called when folder events occur
# DISABLED:                       Signature: callback(folder_path: str, event_type: FolderEventType)
        """
# DISABLED:         super().__init__()
# DISABLED:         self.callback = callback
# DISABLED:         self.debounce_times = {}  # Debounce rapid events
# DISABLED:         self.debounce_interval = 1.0  # seconds

# DISABLED:     def on_created(self, event):
        """Handle folder creation events"""
# DISABLED:         if event.is_directory:
# DISABLED:             self._handle_event(event.src_path, FolderEventType.CREATED)

# DISABLED:     def on_modified(self, event):
        """Handle folder modification events"""
# DISABLED:         if event.is_directory:
# DISABLED:             self._handle_event(event.src_path, FolderEventType.MODIFIED)

# DISABLED:     def on_deleted(self, event):
        """Handle folder deletion events"""
# DISABLED:         if event.is_directory:
# DISABLED:             self._handle_event(event.src_path, FolderEventType.DELETED)

# DISABLED:     def on_moved(self, event):
        """Handle folder move events"""
# DISABLED:         if event.is_directory:
# DISABLED:             self._handle_event(event.src_path, FolderEventType.MOVED)
# DISABLED:             self._handle_event(event.dest_path, FolderEventType.CREATED)

# DISABLED:     def _handle_event(self, folder_path: str, event_type: FolderEventType):
        """Handle folder event with debouncing"""
# DISABLED:         try:
# DISABLED:             current_time = time.time()
# DISABLED:             folder_key = str(Path(folder_path).absolute())

            # Debounce rapid events for same folder
# DISABLED:             if (folder_key in self.debounce_times and
# DISABLED:                 current_time - self.debounce_times[folder_key] < self.debounce_interval):
# DISABLED:                 return

# DISABLED:             self.debounce_times[folder_key] = current_time

            # Call callback
# DISABLED:             try:
# DISABLED:                 self.callback(folder_path, event_type)
# DISABLED:             except Exception as e:
# DISABLED:                 logger.error(f"Error in folder monitor callback: {e}")

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Error handling folder event: {e}")


# DISABLED: class FolderMonitor:
    """Monitor batch_jobs directory for new jobs"""

# DISABLED:     def __init__(self, monitor_path: str, callback: Callable[[str], None]):
        """
# DISABLED:         Initialize folder monitor

# DISABLED:         Args:
# DISABLED:             monitor_path: Path to directory to monitor
# DISABLED:             callback: Callback function when new folder detected
# DISABLED:                       Signature: callback(folder_path: str)
        """
# DISABLED:         self.monitor_path = Path(monitor_path).absolute()
# DISABLED:         self.callback = callback
# DISABLED:         self.observer: Optional[Observer] = None
# DISABLED:         self.monitor_thread: Optional[threading.Thread] = None
# DISABLED:         self.running = False
# DISABLED:         self.event_handler: Optional[BatchFolderEventHandler] = None

        # Fallback polling settings
# DISABLED:         self.poll_interval = 2.0  # seconds
# DISABLED:         self.known_folders: Set[str] = set()

# DISABLED:         logger.info(f"Folder monitor initialized for: {self.monitor_path}")

# DISABLED:     def start(self):
        """Start monitoring"""
# DISABLED:         if self.running:
# DISABLED:             return

# DISABLED:         self.running = True

# DISABLED:         if WATCHDOG_AVAILABLE:
# DISABLED:             self._start_watchdog_monitoring()
# DISABLED:         else:
# DISABLED:             self._start_polling_monitoring()

# DISABLED:         logger.info(f"Started folder monitoring: {self.monitor_path}")

# DISABLED:     def stop(self):
        """Stop monitoring"""
# DISABLED:         if not self.running:
# DISABLED:             return

# DISABLED:         self.running = False

# DISABLED:         if self.observer:
# DISABLED:             self.observer.stop()
# DISABLED:             self.observer.join()

# DISABLED:         if self.monitor_thread and self.monitor_thread.is_alive():
# DISABLED:             self.monitor_thread.join(timeout=5)

# DISABLED:         logger.info(f"Stopped folder monitoring: {self.monitor_path}")

# DISABLED:     def _start_watchdog_monitoring(self):
        """Start watchdog-based monitoring"""
# DISABLED:         try:
# DISABLED:             self.event_handler = BatchFolderEventHandler(
# DISABLED:                 lambda path, event_type: self._handle_folder_event(path, event_type)
# DISABLED:             )

# DISABLED:             self.observer = Observer()
# DISABLED:             self.observer.schedule(
# DISABLED:                 self.event_handler,
# DISABLED:                 str(self.monitor_path),
# DISABLED:                 recursive=True
# DISABLED:             )
# DISABLED:             self.observer.start()

            # Initialize known folders
# DISABLED:             self._scan_existing_folders()

# DISABLED:             logger.info("Started watchdog-based folder monitoring")

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Failed to start watchdog monitoring: {e}")
# DISABLED:             self._start_polling_monitoring()

# DISABLED:     def _start_polling_monitoring(self):
        """Start polling-based monitoring (fallback)"""
# DISABLED:         self.monitor_thread = threading.Thread(
# DISABLED:             target=self._polling_loop,
# DISABLED:             daemon=True
# DISABLED:         )
# DISABLED:         self.monitor_thread.start()

        # Initialize known folders
# DISABLED:         self._scan_existing_folders()

# DISABLED:         logger.info("Started polling-based folder monitoring")

# DISABLED:     def _polling_loop(self):
        """Polling loop for monitoring"""
# DISABLED:         while self.running:
# DISABLED:             try:
# DISABLED:                 self._scan_for_new_folders()
# DISABLED:                 time.sleep(self.poll_interval)
# DISABLED:             except Exception as e:
# DISABLED:                 logger.error(f"Error in polling loop: {e}")
# DISABLED:                 time.sleep(self.poll_interval)

# DISABLED:     def _scan_existing_folders(self):
        """Scan for existing folders"""
# DISABLED:         try:
# DISABLED:             if not self.monitor_path.exists():
# DISABLED:                 return

# DISABLED:             self.known_folders.clear()
# DISABLED:             for item in self.monitor_path.iterdir():
# DISABLED:                 if item.is_dir():
# DISABLED:                     self.known_folders.add(str(item))

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Error scanning existing folders: {e}")

# DISABLED:     def _scan_for_new_folders(self):
        """Scan for new folders"""
# DISABLED:         try:
# DISABLED:             if not self.monitor_path.exists():
# DISABLED:                 return

# DISABLED:             current_folders = set()
# DISABLED:             for item in self.monitor_path.iterdir():
# DISABLED:                 if item.is_dir():
# DISABLED:                     current_folders.add(str(item))

            # Find new folders
# DISABLED:             new_folders = current_folders - self.known_folders
# DISABLED:             for folder_path in new_folders:
# DISABLED:                 self._handle_folder_event(folder_path, FolderEventType.CREATED)

            # Find deleted folders
# DISABLED:             deleted_folders = self.known_folders - current_folders
# DISABLED:             for folder_path in deleted_folders:
# DISABLED:                 self._handle_folder_event(folder_path, FolderEventType.DELETED)

# DISABLED:             self.known_folders = current_folders

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Error scanning for new folders: {e}")

# DISABLED:     def _handle_folder_event(self, folder_path: str, event_type: FolderEventType):
        """Handle folder events"""
# DISABLED:         try:
# DISABLED:             folder_path = str(Path(folder_path).absolute())

# DISABLED:             if event_type == FolderEventType.CREATED:
                # Check if it's a valid job folder
# DISABLED:                 if self._is_valid_job_folder(folder_path):
# DISABLED:                     logger.info(f"Detected new job folder: {folder_path}")
# DISABLED:                     try:
# DISABLED:                         self.callback(folder_path)
# DISABLED:                     except Exception as e:
# DISABLED:                         logger.error(f"Error in folder callback for {folder_path}: {e}")
# DISABLED:                 else:
# DISABLED:                     logger.debug(f"Ignored non-job folder: {folder_path}")

# DISABLED:             elif event_type == FolderEventType.DELETED:
# DISABLED:                 logger.info(f"Job folder deleted: {folder_path}")

# DISABLED:             elif event_type == FolderEventType.MODIFIED:
                # Check if folder became valid after modification
# DISABLED:                 if self._is_valid_job_folder(folder_path):
# DISABLED:                     logger.info(f"Job folder modified and is now valid: {folder_path}")
# DISABLED:                     try:
# DISABLED:                         self.callback(folder_path)
# DISABLED:                     except Exception as e:
# DISABLED:                         logger.error(f"Error in folder callback for {folder_path}: {e}")

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Error handling folder event: {e}")

# DISABLED:     def _is_valid_job_folder(self, folder_path: str) -> bool:
        """Check if folder is a valid job folder"""
# DISABLED:         try:
# DISABLED:             folder = Path(folder_path)

# DISABLED:             if not folder.is_dir():
# DISABLED:                 return False

            # Check for required configuration files
# DISABLED:             required_files = ['config.yaml']
# DISABLED:             optional_files = ['strategy.yaml', 'cost_model.yaml', 'metrics.yaml']

            # Check for required files
# DISABLED:             for required_file in required_files:
# DISABLED:                 if not (folder / required_file).exists():
# DISABLED:                     return False

            # Check for at least one optional file (to avoid false positives)
# DISABLED:             has_optional = any((folder / f).exists() for f in optional_files)
# DISABLED:             if not has_optional:
# DISABLED:                 logger.debug(f"Folder {folder_path} missing optional job files")
# DISABLED:                 return False

# DISABLED:             return True

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Error validating job folder {folder_path}: {e}")
# DISABLED:             return False

# DISABLED:     def get_status(self) -> dict:
        """Get monitor status"""
# DISABLED:         return {
# DISABLED:             'running': self.running,
# DISABLED:             'monitor_path': str(self.monitor_path),
# DISABLED:             'monitoring_type': 'watchdog' if WATCHDOG_AVAILABLE and self.observer else 'polling',
# DISABLED:             'known_folders': len(self.known_folders),
# DISABLED:             'watchdog_available': WATCHDOG_AVAILABLE
# DISABLED:         }