"""
Batch Window Implementation
Main batch processing interface with three-panel layout.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
from typing import Optional
import os
import subprocess
import platform

from .app_controller import AppController
from ..batch import JobManager, Job, JobStatus
from .panels.batch_jobs_panel import BatchJobsPanel
from .panels.job_details_panel import JobDetailsPanel
from .panels.system_resources_panel import SystemResourcesPanel
from ..utils.logger import get_logger

logger = get_logger(__name__)


class BatchWindow:
    """Main batch processing window"""

    def __init__(self, parent: tk.Tk):
        """
        Initialize batch processing window

        Args:
            parent: Parent Tk root window
        """
        self.parent = parent
        self.app_controller = AppController()
        self.job_manager = JobManager()

        # Window configuration
        self.window = tk.Toplevel(parent)
        self.window.title("BSEE Batch Processing")
        self.window.geometry("1400x900")

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('winnative' if platform.system() == 'Windows' else 'default')

        # Selected job
        self.selected_job: Optional[Job] = None

        # Refresh settings
        self.auto_refresh_enabled = tk.BooleanVar(value=True)
        self.refresh_interval = 2000  # 2 seconds
        self.refresh_job: Optional[str] = None

        # Setup GUI
        self._setup_menu()
        self._setup_ui()
        self._setup_callbacks()

        # Start monitoring and auto-refresh
        self.job_manager.start_folder_monitoring()
        self._start_auto_refresh()

        # Center window
        self._center_window()

        logger.info("Batch processing window initialized")

    def _setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Add Job Folder", command=self._add_job_folder)
        file_menu.add_command(label="Create New Job", command=self._create_new_job)
        file_menu.add_separator()
        file_menu.add_command(label="Exit Batch Mode", command=self._close_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit Application", command=self._exit_app)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Preferences", command=self._show_preferences)
        edit_menu.add_command(label="Clear Completed Jobs", command=self._clear_completed_jobs)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_checkbutton(label="Auto Refresh", variable=self.auto_refresh_enabled)
        view_menu.add_command(label="Refresh Now", command=self._refresh_all)
        view_menu.add_separator()
        view_menu.add_command(label="Open Batch Jobs Folder", command=self._open_batch_folder)

        # Jobs menu
        jobs_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Jobs", menu=jobs_menu)
        jobs_menu.add_command(label="Start All Jobs", command=self._start_all_jobs)
        jobs_menu.add_command(label="Pause All Jobs", command=self._pause_all_jobs)
        jobs_menu.add_command(label="Cancel All Jobs", command=self._cancel_all_jobs)
        jobs_menu.add_separator()
        jobs_menu.add_command(label="Export Job List", command=self._export_job_list)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Batch Processing Guide", command=self._show_help)
        help_menu.add_command(label="About", command=self._show_about)

    def _setup_ui(self):
        """Setup main UI layout"""
        # Main container
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Top toolbar
        self._setup_toolbar(main_frame)

        # Three-panel layout
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Left panel - Job list
        self.left_frame = ttk.Frame(paned_window)
        paned_window.add(self.left_frame, weight=1)

        # Center panel - Job details
        self.center_frame = ttk.Frame(paned_window)
        paned_window.add(self.center_frame, weight=2)

        # Right panel - System resources
        self.right_frame = ttk.Frame(paned_window)
        paned_window.add(self.right_frame, weight=1)

        # Initialize panels
        self.batch_jobs_panel = BatchJobsPanel(
            self.left_frame,
            self.job_manager,
            job_selected_callback=self._on_job_selected
        )

        self.job_details_panel = JobDetailsPanel(
            self.center_frame,
            self.job_manager
        )

        self.system_resources_panel = SystemResourcesPanel(
            self.right_frame,
            self.job_manager,
            add_job_callback=self._add_job_folder
        )

        # Bottom status bar
        self._setup_status_bar()

    def _setup_toolbar(self, parent):
        """Setup toolbar"""
        toolbar_frame = ttk.Frame(parent)
        toolbar_frame.pack(fill=tk.X, pady=(0, 5))

        # Left side - actions
        left_frame = ttk.Frame(toolbar_frame)
        left_frame.pack(side=tk.LEFT)

        ttk.Button(left_frame, text="Add Jobs", command=self._add_job_folder).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(left_frame, text="Create Job", command=self._create_new_job).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Separator(left_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        ttk.Button(left_frame, text="Start All", command=self._start_all_jobs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(left_frame, text="Pause All", command=self._pause_all_jobs).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(left_frame, text="Cancel All", command=self._cancel_all_jobs).pack(side=tk.LEFT, padx=(0, 5))

        # Right side - settings
        right_frame = ttk.Frame(toolbar_frame)
        right_frame.pack(side=tk.RIGHT)

        ttk.Checkbutton(
            right_frame,
            text="Auto Refresh",
            variable=self.auto_refresh_enabled
        ).pack(side=tk.RIGHT, padx=(10, 0))

    def _setup_status_bar(self):
        """Setup status bar"""
        status_frame = ttk.Frame(self.window)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Status label
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(status_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # Job counts
        self.job_counts_label = ttk.Label(status_frame, text="0 jobs")
        self.job_counts_label.pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(status_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        # Auto-start indicator
        self.autostart_label = ttk.Label(status_frame, text="")
        self.autostart_label.pack(side=tk.LEFT, padx=5)

    def _setup_callbacks(self):
        """Setup event callbacks"""
        self.window.protocol("WM_DELETE_WINDOW", self._close_window)

        # Job manager callback for job updates
        self.job_manager.add_job_callback(self._on_job_update)

    def _start_auto_refresh(self):
        """Start auto-refresh loop"""
        def refresh_loop():
            while True:
                if self.auto_refresh_enabled.get():
                    try:
                        self.window.after(0, self._refresh_all)
                    except:
                        break
                time.sleep(self.refresh_interval / 1000.0)

        self.refresh_thread = threading.Thread(target=refresh_loop, daemon=True)
        self.refresh_thread.start()

    def _refresh_all(self):
        """Refresh all panels"""
        try:
            # Update panels
            self.batch_jobs_panel.refresh()
            self.job_details_panel.refresh()
            self.system_resources_panel.refresh()

            # Update status bar
            self._update_status_bar()

        except Exception as e:
            logger.error(f"Error refreshing: {e}")

    def _update_status_bar(self):
        """Update status bar information"""
        try:
            stats = self.job_manager.get_statistics()

            # Update job counts
            total = stats['total_jobs']
            running = stats['running_jobs']
            queued = stats['queue_length']

            self.job_counts_label.config(
                text=f"{total} jobs ({running} running, {queued} queued)"
            )

            # Update auto-start indicator
            if stats['auto_start']:
                self.autostart_label.config(text="🟢 Auto-start ON")
            else:
                self.autostart_label.config(text="🔴 Auto-start OFF")

            # Update main status
            if running > 0:
                self.status_label.config(text=f"Processing {running} jobs...")
            elif queued > 0:
                self.status_label.config(text=f"{queued} jobs queued")
            else:
                self.status_label.config(text="Ready")

        except Exception as e:
            logger.error(f"Error updating status bar: {e}")

    def _on_job_selected(self, job: Job):
        """Handle job selection"""
        self.selected_job = job
        self.job_details_panel.set_job(job)

    def _on_job_update(self, job: Job):
        """Handle job updates from job manager"""
        # Update if this is the selected job
        if self.selected_job and self.selected_job.job_id == job.job_id:
            self.window.after(0, lambda: self.job_details_panel.set_job(job))

    def _center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def _add_job_folder(self):
        """Add job folder dialog"""
        folder_path = filedialog.askdirectory(
            title="Select Job Folder",
            initialdir=str(Path.cwd())
        )

        if folder_path:
            job = self.job_manager.add_job(folder_path)
            if job:
                self.status_label.config(text=f"Added job: {job.name}")
            else:
                messagebox.showerror("Error", f"Failed to add job from {folder_path}")

    def _create_new_job(self):
        """Create new job dialog"""
        # This would open a dialog for creating new job templates
        # For now, just show info
        messagebox.showinfo(
            "Create New Job",
            "Job creation wizard not yet implemented.\n"
            "Use the CLI: python main.py batch create <job_name> --template <template>"
        )

    def _start_all_jobs(self):
        """Start all pending/queued jobs"""
        jobs = self.job_manager.get_jobs_by_status(JobStatus.PENDING)
        jobs.extend(self.job_manager.get_jobs_by_status(JobStatus.QUEUED))

        for job in jobs:
            self.job_manager.start_job(job.job_id)

        self.status_label.config(text=f"Started {len(jobs)} jobs")

    def _pause_all_jobs(self):
        """Pause all running jobs"""
        jobs = self.job_manager.get_jobs_by_status(JobStatus.RUNNING)

        for job in jobs:
            self.job_manager.pause_job(job.job_id)

        self.status_label.config(text=f"Paused {len(jobs)} jobs")

    def _cancel_all_jobs(self):
        """Cancel all active jobs"""
        active_statuses = [JobStatus.RUNNING, JobStatus.QUEUED, JobStatus.PENDING]
        jobs = []

        for status in active_statuses:
            jobs.extend(self.job_manager.get_jobs_by_status(status))

        if jobs:
            result = messagebox.askyesno(
                "Cancel Jobs",
                f"Cancel {len(jobs)} active jobs?"
            )

            if result:
                for job in jobs:
                    self.job_manager.cancel_job(job.job_id)
                self.status_label.config(text=f"Cancelled {len(jobs)} jobs")

    def _clear_completed_jobs(self):
        """Clear completed and failed jobs"""
        completed_jobs = self.job_manager.get_jobs_by_status(JobStatus.COMPLETED)
        failed_jobs = self.job_manager.get_jobs_by_status(JobStatus.FAILED)
        jobs_to_clear = completed_jobs + failed_jobs

        if jobs_to_clear:
            result = messagebox.askyesno(
                "Clear Jobs",
                f"Clear {len(jobs_to_clear)} completed/failed jobs?"
            )

            if result:
                for job in jobs_to_clear:
                    self.job_manager.remove_job(job.job_id)
                self.status_label.config(text=f"Cleared {len(jobs_to_clear)} jobs")

    def _export_job_list(self):
        """Export job list to file"""
        filename = filedialog.asksaveasfilename(
            title="Export Job List",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filename:
            try:
                import csv

                jobs = self.job_manager.get_all_jobs()

                with open(filename, 'w', newline='') as csvfile:
                    fieldnames = ['job_id', 'name', 'status', 'progress', 'created_time', 'execution_time']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for job in jobs:
                        writer.writerow({
                            'job_id': job.job_id,
                            'name': job.name,
                            'status': job.status.value,
                            'progress': f"{job.progress:.1f}%",
                            'created_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(job.created_time)),
                            'execution_time': f"{job.completed_time - job.started_time:.2f}s" if job.started_time and job.completed_time else ""
                        })

                messagebox.showinfo("Export Complete", f"Job list exported to {filename}")

            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export job list: {e}")

    def _show_preferences(self):
        """Show preferences dialog"""
        # This would open a preferences dialog
        messagebox.showinfo("Preferences", "Preferences dialog not yet implemented.")

    def _open_batch_folder(self):
        """Open batch jobs folder in system file manager"""
        batch_folder = Path.cwd() / 'batch_jobs'
        batch_folder.mkdir(exist_ok=True)

        try:
            if platform.system() == "Windows":
                os.startfile(str(batch_folder))
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(batch_folder)])
            else:  # Linux
                subprocess.run(["xdg-open", str(batch_folder)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open folder: {e}")

    def _show_help(self):
        """Show help dialog"""
        help_text = """
BSEE Batch Processing Help

Batch Processing allows you to:
• Create and manage multiple analysis jobs
• Monitor resource usage and progress
• Schedule jobs for specific times
• View detailed analytics and results

Getting Started:
1. Create job folders in the batch_jobs/ directory
2. Each folder needs a config.yaml file
3. Jobs are automatically discovered and can be queued
4. Use the GUI to monitor and control job execution

Job Configuration:
• config.yaml - Main job configuration
• strategy.yaml - Search strategy settings
• cost_model.yaml - Cost model parameters
• metrics.yaml - Metrics configuration
• queue_settings.yaml - Scheduling settings

For more information, see the BSEE documentation.
        """

        # Create help window
        help_window = tk.Toplevel(self.window)
        help_window.title("Batch Processing Help")
        help_window.geometry("600x500")

        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert("1.0", help_text)
        text_widget.config(state=tk.DISABLED)

        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10)

    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About BSEE Batch Processing",
            "BSEE Batch Processing System\n\n"
            "Version 1.0.0\n\n"
            "Advanced batch job management for binary structure analysis.\n\n"
            "Features:\n"
            "• Multi-job execution and scheduling\n"
            "• Real-time resource monitoring\n"
            "• Comprehensive job analytics\n"
            "• Auto-discovery of job folders"
        )

    def _close_window(self):
        """Close batch window"""
        # Stop monitoring
        self.job_manager.stop_folder_monitoring()

        # Hide window instead of destroying to allow reopening
        self.window.withdraw()

    def _exit_app(self):
        """Exit entire application"""
        result = messagebox.askyesno("Exit", "Exit BSEE application?")
        if result:
            self.job_manager.shutdown()
            self.parent.quit()
            self.parent.destroy()

    def show(self):
        """Show the batch window"""
        self.window.deiconify()
        self.window.lift()
        self._refresh_all()

    def hide(self):
        """Hide the batch window"""
        self.window.withdraw()