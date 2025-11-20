"""
Job Details Panel Implementation
Detailed view of selected job with analytics dropdowns and controls.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
from typing import Optional
import subprocess
import platform

from ...batch import Job, JobStatus
from ...utils.logger import get_logger

logger = get_logger(__name__)


class AnalyticsSection(ttk.Frame):
    """Collapsible analytics section"""

    def __init__(self, parent, title: str, content_widget):
        super().__init__(parent)

        self.title = title
        self.content_widget = content_widget
        self.expanded = False

        self._setup_ui()

    def _setup_ui(self):
        """Setup collapsible section UI"""
        # Header with title and toggle button
        header_frame = ttk.Frame(self)
        header_frame.pack(fill=tk.X, pady=2)

        # Toggle button
        self.toggle_button = ttk.Button(
            header_frame,
            text=f"▶ {self.title}",
            command=self._toggle,
            width=20
        )
        self.toggle_button.pack(side=tk.LEFT)

        # Content frame (initially hidden)
        self.content_frame = ttk.Frame(self)
        self.content_widget.pack(fill=tk.BOTH, expand=True, padx=(20, 0))

        self.content_frame.pack_forget()

    def _toggle(self):
        """Toggle section expansion"""
        self.expanded = not self.expanded

        if self.expanded:
            self.toggle_button.config(text=f"▼ {self.title}")
            self.content_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        else:
            self.toggle_button.config(text=f"▶ {self.title}")
            self.content_frame.pack_forget()


class JobDetailsPanel:
    """Panel showing detailed information about selected job"""

    def __init__(self, parent, job_manager):
        """
        Initialize job details panel

        Args:
            parent: Parent widget
            job_manager: JobManager instance
        """
        self.parent = parent
        self.job_manager = job_manager
        self.current_job: Optional[Job] = None

        self._setup_ui()

    def _setup_ui(self):
        """Setup panel UI"""
        # Title
        title_label = ttk.Label(
            self.parent,
            text="Job Details",
            font=('TkDefaultFont', 12, 'bold')
        )
        title_label.pack(pady=(0, 10))

        # Main scrollable area
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Empty state
        self._create_empty_state()

    def _create_empty_state(self):
        """Create empty state display"""
        empty_frame = ttk.Frame(self.scrollable_frame)
        empty_frame.pack(expand=True)

        ttk.Label(
            empty_frame,
            text="No job selected",
            font=('TkDefaultFont', 11, 'bold')
        ).pack(pady=20)

        ttk.Label(
            empty_frame,
            text="Select a job from the list to view details",
            font=('TkDefaultFont', 9)
        ).pack()

        self.empty_frame = empty_frame

    def _create_job_details(self, job: Job):
        """Create job details display"""
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            if widget != self.empty_frame:
                widget.destroy()

        # Job header section
        self._create_header_section(job)

        # Analytics sections
        self._create_analytics_sections(job)

        # Action buttons
        self._create_action_buttons(job)

        # Logs section
        self._create_logs_section(job)

    def _create_header_section(self, job: Job):
        """Create job header section"""
        header_frame = ttk.LabelFrame(self.scrollable_frame, text="Job Information", padding=10)
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Basic info grid
        info_frame = ttk.Frame(header_frame)
        info_frame.pack(fill=tk.X)

        # Left column
        left_frame = ttk.Frame(info_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._add_info_row(left_frame, "Job ID:", job.job_id)
        self._add_info_row(left_frame, "Name:", job.name)
        self._add_info_row(left_frame, "Status:", job.status.value.upper())

        if job.error_message:
            self._add_info_row(left_frame, "Error:", job.error_message[:50] + "...")

        # Right column
        right_frame = ttk.Frame(info_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))

        self._add_info_row(right_frame, "Progress:", f"{job.progress:.1f}%")
        self._add_info_row(right_frame, "Current Stage:", job.current_stage)
        self._add_info_row(right_frame, "Priority:", job.priority.name)

        # Progress bar
        progress_frame = ttk.Frame(header_frame)
        progress_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Label(progress_frame, text="Progress:").pack(side=tk.LEFT)

        progress_var = tk.DoubleVar(value=job.progress)
        progress_bar = ttk.Progressbar(
            progress_frame,
            variable=progress_var,
            mode='determinate'
        )
        progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))

        progress_label = ttk.Label(progress_frame, text=f"{job.progress:.1f}%")
        progress_label.pack(side=tk.LEFT, padx=(10, 0))

        # Timing information
        timing_frame = ttk.Frame(header_frame)
        timing_frame.pack(fill=tk.X, pady=(10, 0))

        created_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(job.created_time))
        self._add_info_row(timing_frame, "Created:", created_time)

        if job.started_time:
            started_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(job.started_time))
            self._add_info_row(timing_frame, "Started:", started_time)

        if job.completed_time:
            completed_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(job.completed_time))
            execution_time = job.completed_time - job.started_time if job.started_time else 0
            self._add_info_row(timing_frame, "Completed:", completed_time)
            self._add_info_row(timing_frame, "Execution Time:", f"{execution_time:.2f}s")

    def _create_analytics_sections(self, job: Job):
        """Create analytics dropdown sections"""
        analytics_frame = ttk.LabelFrame(self.scrollable_frame, text="Analytics", padding=10)
        analytics_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Resource usage section
        resource_content = self._create_resource_content(job)
        AnalyticsSection(analytics_frame, "Resource Usage", resource_content).pack(fill=tk.X, pady=2)

        # Configuration section
        config_content = self._create_config_content(job)
        AnalyticsSection(analytics_frame, "Configuration", config_content).pack(fill=tk.X, pady=2)

        # Performance metrics section
        if job.status in [JobStatus.RUNNING, JobStatus.COMPLETED]:
            performance_content = self._create_performance_content(job)
            AnalyticsSection(analytics_frame, "Performance Metrics", performance_content).pack(fill=tk.X, pady=2)

    def _create_resource_content(self, job: Job) -> ttk.Frame:
        """Create resource usage content"""
        content_frame = ttk.Frame()

        # Resource grid
        resource_frame = ttk.Frame(content_frame)
        resource_frame.pack(fill=tk.X)

        self._add_info_row(resource_frame, "CPU Usage:", f"{job.resources.cpu_percent:.1f}%")
        self._add_info_row(resource_frame, "Memory Usage:", f"{job.resources.memory_mb:.1f} MB")
        self._add_info_row(resource_frame, "Peak Memory:", f"{job.resources.peak_memory_mb:.1f} MB")
        self._add_info_row(resource_frame, "Active Threads:", str(job.resources.active_threads))

        return content_frame

    def _create_config_content(self, job: Job) -> ttk.Frame:
        """Create configuration content"""
        content_frame = ttk.Frame()

        if job.config:
            config_frame = ttk.Frame(content_frame)
            config_frame.pack(fill=tk.X)

            self._add_info_row(config_frame, "Description:", job.config.description or "None")

            if job.config.strategy_config:
                strategy = job.config.strategy_config.get('strategy', 'Unknown')
                self._add_info_row(config_frame, "Strategy:", strategy)

            if job.config.metrics_config:
                metrics = job.config.metrics_config.get('metrics', [])
                if metrics:
                    self._add_info_row(config_frame, "Metrics:", ", ".join(metrics[:3]))
                    if len(metrics) > 3:
                        self._add_info_row(config_frame, "", f"... and {len(metrics) - 3} more")
        else:
            ttk.Label(content_frame, text="Configuration not loaded").pack()

        return content_frame

    def _create_performance_content(self, job: Job) -> ttk.Frame:
        """Create performance metrics content"""
        content_frame = ttk.Frame()

        perf_frame = ttk.Frame(content_frame)
        perf_frame.pack(fill=tk.X)

        if job.started_time and job.completed_time:
            execution_time = job.completed_time - job.started_time
            self._add_info_row(perf_frame, "Total Execution Time:", f"{execution_time:.2f}s")

        self._add_info_row(perf_frame, "Operations per Second:", "N/A")  # TODO: Calculate from actual data
        self._add_info_row(perf_frame, "Efficiency Score:", "N/A")  # TODO: Calculate from metrics

        return content_frame

    def _create_action_buttons(self, job: Job):
        """Create action buttons"""
        actions_frame = ttk.LabelFrame(self.scrollable_frame, text="Actions", padding=10)
        actions_frame.pack(fill=tk.X, pady=(0, 10))

        button_frame = ttk.Frame(actions_frame)
        button_frame.pack()

        # Job control buttons
        if job.status == JobStatus.PENDING:
            ttk.Button(
                button_frame,
                text="Start Job",
                command=lambda: self._start_job(job)
            ).pack(side=tk.LEFT, padx=5)

        elif job.status == JobStatus.RUNNING:
            ttk.Button(
                button_frame,
                text="Pause Job",
                command=lambda: self._pause_job(job)
            ).pack(side=tk.LEFT, padx=5)

        elif job.status == JobStatus.PAUSED:
            ttk.Button(
                button_frame,
                text="Resume Job",
                command=lambda: self._resume_job(job)
            ).pack(side=tk.LEFT, padx=5)

        if job.status in [JobStatus.PENDING, JobStatus.QUEUED, JobStatus.RUNNING, JobStatus.PAUSED]:
            ttk.Button(
                button_frame,
                text="Cancel Job",
                command=lambda: self._cancel_job(job)
            ).pack(side=tk.LEFT, padx=5)

        # Results and view buttons
        ttk.Separator(button_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=10, fill=tk.Y)

        ttk.Button(
            button_frame,
            text="Open Results",
            command=lambda: self._open_results(job)
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="View Binary",
            command=lambda: self._view_binary(job)
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Open Folder",
            command=lambda: self._open_folder(job)
        ).pack(side=tk.LEFT, padx=5)

    def _create_logs_section(self, job: Job):
        """Create logs section"""
        logs_frame = ttk.LabelFrame(self.scrollable_frame, text="Job Logs", padding=10)
        logs_frame.pack(fill=tk.BOTH, expand=True)

        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            height=8,
            wrap=tk.WORD,
            font=('Consolas', 9)
        )
        self.logs_text.pack(fill=tk.BOTH, expand=True)

        # Update logs
        self._update_logs(job)

    def _add_info_row(self, parent, label: str, value: str):
        """Add an info row with label and value"""
        row_frame = ttk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=1)

        ttk.Label(row_frame, text=label, font=('TkDefaultFont', 9, 'bold')).pack(side=tk.LEFT)
        ttk.Label(row_frame, text=value, font=('TkDefaultFont', 9)).pack(side=tk.LEFT, padx=(10, 0))

    def _update_logs(self, job: Job):
        """Update logs display"""
        if hasattr(self, 'logs_text'):
            self.logs_text.delete('1.0', tk.END)

            if job.logs:
                for log_entry in job.logs[-50:]:  # Show last 50 entries
                    self.logs_text.insert(tk.END, log_entry + '\n')
            else:
                self.logs_text.insert(tk.END, "No logs available for this job.\n")

            self.logs_text.see(tk.END)

    def _start_job(self, job: Job):
        """Start job"""
        self.job_manager.start_job(job.job_id)

    def _pause_job(self, job: Job):
        """Pause job"""
        self.job_manager.pause_job(job.job_id)

    def _resume_job(self, job: Job):
        """Resume job"""
        self.job_manager.resume_job(job.job_id)

    def _cancel_job(self, job: Job):
        """Cancel job"""
        result = messagebox.askyesno("Cancel Job", f"Cancel job '{job.name}'?")
        if result:
            self.job_manager.cancel_job(job.job_id)

    def _open_results(self, job: Job):
        """Open results folder"""
        results_folder = job.results_folder
        if not results_folder.exists():
            messagebox.showinfo("No Results", "Results folder does not exist yet.")
            return

        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(results_folder)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(results_folder)])
            else:  # Linux
                subprocess.run(["xdg-open", str(results_folder)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open results folder: {e}")

    def _view_binary(self, job: Job):
        """View binary analysis"""
        messagebox.showinfo(
            "Binary Viewer",
            "Binary viewer integration will be available in the next version.\n"
            "For now, check the results folder for analysis files."
        )

    def _open_folder(self, job: Job):
        """Open job folder"""
        try:
            if platform.system() == "Windows":
                subprocess.run(["explorer", str(job.job_folder)])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(job.job_folder)])
            else:  # Linux
                subprocess.run(["xdg-open", str(job.job_folder)])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open job folder: {e}")

    def set_job(self, job: Optional[Job]):
        """Set the selected job"""
        self.current_job = job

        # Clear empty state
        if hasattr(self, 'empty_frame'):
            self.empty_frame.pack_forget()

        if job:
            self._create_job_details(job)
        else:
            # Show empty state
            for widget in self.scrollable_frame.winfo_children():
                if widget != self.empty_frame:
                    widget.destroy()
            self.empty_frame.pack(expand=True)

    def refresh(self):
        """Refresh the current job display"""
        if self.current_job:
            # Get updated job from manager
            updated_job = self.job_manager.get_job(self.current_job.job_id)
            if updated_job:
                self.set_job(updated_job)