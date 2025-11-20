"""
Batch Jobs Panel Implementation
Job list and management interface for batch processing GUI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional, Callable, List

from ...batch import JobManager, Job, JobStatus, JobPriority
from ...utils.logger import get_logger

logger = get_logger(__name__)


class JobListFrame(ttk.Frame):
    """Custom frame for displaying a single job in the list"""

    def __init__(self, parent, job: Job, job_manager: JobManager, callback: Callable):
        super().__init__(parent, relief=tk.RIDGE, borderwidth=1)

        self.job = job
        self.job_manager = job_manager
        self.callback = callback
        self.selected = False

        self._setup_ui()
        self._update_display()

    def _setup_ui(self):
        """Setup job display UI"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=3)

        # Left side - Job info
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Job name and ID
        self.name_label = ttk.Label(
            info_frame,
            text=f"{self.job.name}",
            font=('TkDefaultFont', 10, 'bold')
        )
        self.name_label.pack(anchor=tk.W)

        self.id_label = ttk.Label(
            info_frame,
            text=f"ID: {self.job.job_id[:8]}",
            font=('TkDefaultFont', 8)
        )
        self.id_label.pack(anchor=tk.W)

        # Status label
        self.status_label = ttk.Label(
            info_frame,
            text="",
            font=('TkDefaultFont', 8)
        )
        self.status_label.pack(anchor=tk.W)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            info_frame,
            variable=self.progress_var,
            length=150,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(2, 0))

        # Right side - Controls
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(side=tk.RIGHT, padx=(10, 0))

        # Control buttons
        self.play_button = ttk.Button(
            control_frame,
            text="▶",
            width=3,
            command=self._on_play_clicked
        )
        self.play_button.pack(side=tk.LEFT, padx=1)

        self.pause_button = ttk.Button(
            control_frame,
            text="⏸",
            width=3,
            command=self._on_pause_clicked,
            state=tk.DISABLED
        )
        self.pause_button.pack(side=tk.LEFT, padx=1)

        self.cancel_button = ttk.Button(
            control_frame,
            text="✕",
            width=3,
            command=self._on_cancel_clicked
        )
        self.cancel_button.pack(side=tk.LEFT, padx=1)

        # Resource indicator
        self.resource_label = ttk.Label(
            control_frame,
            text="",
            font=('TkDefaultFont', 7)
        )
        self.resource_label.pack(anchor=tk.E, pady=(2, 0))

        # Bind click events
        self.bind("<Button-1>", self._on_clicked)
        for child in self.winfo_children():
            child.bind("<Button-1>", self._on_clicked)

    def _update_display(self):
        """Update job display based on current status"""
        # Update status
        status_text = self.job.status.value.upper()
        if self.job.error_message:
            status_text += f" ({self.job.error_message[:20]}...)"

        self.status_label.config(text=status_text)

        # Update progress
        self.progress_var.set(self.job.progress)

        # Update resource usage
        if self.job.status == JobStatus.RUNNING:
            memory_mb = self.job.resources.memory_mb
            cpu_percent = self.job.resources.cpu_percent
            self.resource_label.config(text=f"{memory_mb:.0f}MB {cpu_percent:.0f}%")
        else:
            self.resource_label.config(text="")

        # Update control buttons
        if self.job.status == JobStatus.PENDING:
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
        elif self.job.status == JobStatus.RUNNING:
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
        elif self.job.status == JobStatus.PAUSED:
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
        elif self.job.status in [JobStatus.QUEUED]:
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED)
        else:  # COMPLETED, FAILED, CANCELLED
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.DISABLED)

        # Update frame color based on status
        if self.selected:
            self.configure(relief=tk.SOLID, borderwidth=2)
        else:
            self.configure(relief=tk.RIDGE, borderwidth=1)

    def _on_clicked(self, event):
        """Handle frame click"""
        self.callback(self.job)

    def _on_play_clicked(self):
        """Handle play button click"""
        if self.job.status == JobStatus.PENDING:
            self.job_manager.start_job(self.job.job_id)
        elif self.job.status == JobStatus.PAUSED:
            self.job_manager.resume_job(self.job.job_id)

    def _on_pause_clicked(self):
        """Handle pause button click"""
        self.job_manager.pause_job(self.job.job_id)

    def _on_cancel_clicked(self):
        """Handle cancel button click"""
        result = messagebox.askyesno(
            "Cancel Job",
            f"Cancel job '{self.job.name}'?"
        )
        if result:
            self.job_manager.cancel_job(self.job.job_id)

    def set_selected(self, selected: bool):
        """Set selection state"""
        self.selected = selected
        self._update_display()

    def update_job(self, job: Job):
        """Update job reference and display"""
        self.job = job
        self._update_display()


class BatchJobsPanel:
    """Panel displaying and managing batch jobs"""

    def __init__(
        self,
        parent,
        job_manager: JobManager,
        job_selected_callback: Callable[[Job], None]
    ):
        """
        Initialize batch jobs panel

        Args:
            parent: Parent widget
            job_manager: JobManager instance
            job_selected_callback: Callback when job is selected
        """
        self.parent = parent
        self.job_manager = job_manager
        self.job_selected_callback = job_selected_callback

        self.selected_job: Optional[Job] = None
        self.job_frames: dict[str, JobListFrame] = {}

        self._setup_ui()
        self._setup_callbacks()

    def _setup_ui(self):
        """Setup panel UI"""
        # Title
        title_label = ttk.Label(
            self.parent,
            text="Batch Jobs",
            font=('TkDefaultFont', 12, 'bold')
        )
        title_label.pack(pady=(0, 10))

        # Filter controls
        filter_frame = ttk.Frame(self.parent)
        filter_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)

        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Pending", "Queued", "Running", "Paused", "Completed", "Failed"],
            state="readonly",
            width=12
        )
        filter_combo.pack(side=tk.LEFT, padx=(5, 0))
        filter_combo.bind("<<ComboboxSelected>>", self._on_filter_changed)

        # Auto-start checkbox
        self.autostart_var = tk.BooleanVar(value=self.job_manager.auto_start)
        autostart_check = ttk.Checkbutton(
            filter_frame,
            text="Auto-start",
            variable=self.autostart_var,
            command=self._on_autostart_changed
        )
        autostart_check.pack(side=tk.RIGHT)

        # Scrollable area for job list
        canvas_frame = ttk.Frame(self.parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar
        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)

        # Empty state label
        self.empty_label = ttk.Label(
            self.scrollable_frame,
            text="No jobs found.\nAdd job folders to get started.",
            justify=tk.CENTER
        )

    def _setup_callbacks(self):
        """Setup event callbacks"""
        self.job_manager.add_job_callback(self._on_job_update)

    def _on_filter_changed(self, event=None):
        """Handle filter change"""
        self.refresh()

    def _on_autostart_changed(self):
        """Handle auto-start checkbox change"""
        self.job_manager.set_auto_start(self.autostart_var.get())

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_job_update(self, job: Job):
        """Handle job update from job manager"""
        self.parent.after(0, lambda: self._update_job_frame(job))

    def _update_job_frame(self, job: Job):
        """Update specific job frame"""
        if job.job_id in self.job_frames:
            job_frame = self.job_frames[job.job_id]
            job_frame.update_job(job)

    def _on_job_selected(self, job: Job):
        """Handle job selection"""
        # Update previous selection
        if self.selected_job and self.selected_job.job_id in self.job_frames:
            self.job_frames[self.selected_job.job_id].set_selected(False)

        # Update new selection
        self.selected_job = job
        if job and job.job_id in self.job_frames:
            self.job_frames[job.job_id].set_selected(True)

        # Notify callback
        self.job_selected_callback(job)

    def refresh(self):
        """Refresh job list"""
        try:
            # Clear existing frames
            for frame in self.job_frames.values():
                frame.destroy()
            self.job_frames.clear()

            # Get jobs based on filter
            jobs = self.job_manager.get_all_jobs()
            filter_value = self.filter_var.get()

            if filter_value != "All":
                try:
                    filter_status = JobStatus(filter_value.lower())
                    jobs = [job for job in jobs if job.status == filter_status]
                except ValueError:
                    pass  # Invalid filter, show all

            # Sort by creation time (newest first) and priority
            jobs.sort(key=lambda j: (j.priority.value, -j.created_time), reverse=True)

            if jobs:
                self.empty_label.pack_forget()

                # Create job frames
                for job in jobs:
                    job_frame = JobListFrame(
                        self.scrollable_frame,
                        job,
                        self.job_manager,
                        self._on_job_selected
                    )
                    job_frame.pack(fill=tk.X, pady=2)
                    self.job_frames[job.job_id] = job_frame

                # Restore selection
                if self.selected_job:
                    for job in jobs:
                        if job.job_id == self.selected_job.job_id:
                            self._on_job_selected(job)
                            break

            else:
                self.empty_label.pack(expand=True)

        except Exception as e:
            logger.error(f"Error refreshing job list: {e}")

    def set_selected_job(self, job: Job):
        """Set selected job programmatically"""
        self._on_job_selected(job)

    def get_selected_job(self) -> Optional[Job]:
        """Get currently selected job"""
        return self.selected_job