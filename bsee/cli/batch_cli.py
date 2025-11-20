"""
Batch CLI Interface
Command-line interface for BSEE batch job management.
"""

import os
import sys
import time
import json
import subprocess
from typing import Optional, List
from pathlib import Path

try:
    import click
    CLICK_AVAILABLE = True
except ImportError:
    CLICK_AVAILABLE = False

try:
    from tabulate import tabulate
    TABULATE_AVAILABLE = True
except ImportError:
    TABULATE_AVAILABLE = False

from ..batch import JobManager, Job, JobStatus
from ..batch.job_validator import JobValidator
from ..utils.logger import get_logger

logger = get_logger(__name__)


class BatchCLI:
    """Batch CLI interface"""

    def __init__(self):
        """Initialize CLI"""
        self.job_manager = JobManager()
        self.job_validator = JobValidator()

    def format_table(self, data: List[List[str]], headers: List[str]) -> str:
        """Format data as table"""
        if TABULATE_AVAILABLE:
            return tabulate(data, headers=headers, tablefmt='grid')
        else:
            # Fallback formatting
            result = []
            if headers:
                result.append(" | ".join(headers))
                result.append("-" * (len(" | ".join(headers))))
            for row in data:
                result.append(" | ".join(str(cell) for cell in row))
            return "\n".join(result)

    def format_job_info(self, job: Job) -> str:
        """Format job information for display"""
        status = job.status.value.upper()
        if job.error_message:
            status += f" ({job.error_message})"

        execution_time = ""
        if job.started_time and job.completed_time:
            execution_time = f"{job.completed_time - job.started_time:.1f}s"
        elif job.started_time:
            execution_time = f"{time.time() - job.started_time:.1f}s"

        return [
            job.job_id[:8],
            job.name[:20],
            status,
            f"{job.progress:.1f}%",
            job.current_stage[:15],
            execution_time,
            f"{job.resources.memory_mb:.1f}MB"
        ]

    def cmd_list(self, status_filter: Optional[str] = None):
        """List all batch jobs"""
        try:
            jobs = self.job_manager.get_all_jobs()

            if status_filter:
                try:
                    filter_status = JobStatus(status_filter.lower())
                    jobs = [job for job in jobs if job.status == filter_status]
                except ValueError:
                    click.echo(f"Invalid status filter: {status_filter}")
                    return

            if not jobs:
                click.echo("No jobs found.")
                return

            # Sort by creation time (newest first)
            jobs.sort(key=lambda j: j.created_time, reverse=True)

            # Prepare table data
            data = [self.format_job_info(job) for job in jobs]
            headers = ['ID', 'Name', 'Status', 'Progress', 'Stage', 'Time', 'Memory']

            click.echo(self.format_table(data, headers))

        except Exception as e:
            click.echo(f"Error listing jobs: {e}", err=True)

    def cmd_start(self, job_id: str):
        """Start a job"""
        try:
            success = self.job_manager.start_job(job_id)
            if success:
                click.echo(f"Job {job_id} started successfully.")
            else:
                click.echo(f"Failed to start job {job_id}.", err=True)

        except Exception as e:
            click.echo(f"Error starting job: {e}", err=True)

    def cmd_pause(self, job_id: str):
        """Pause a job"""
        try:
            success = self.job_manager.pause_job(job_id)
            if success:
                click.echo(f"Job {job_id} paused.")
            else:
                click.echo(f"Failed to pause job {job_id}.", err=True)

        except Exception as e:
            click.echo(f"Error pausing job: {e}", err=True)

    def cmd_resume(self, job_id: str):
        """Resume a job"""
        try:
            success = self.job_manager.resume_job(job_id)
            if success:
                click.echo(f"Job {job_id} resumed.")
            else:
                click.echo(f"Failed to resume job {job_id}.", err=True)

        except Exception as e:
            click.echo(f"Error resuming job: {e}", err=True)

    def cmd_cancel(self, job_id: str):
        """Cancel a job"""
        try:
            success = self.job_manager.cancel_job(job_id)
            if success:
                click.echo(f"Job {job_id} cancelled.")
            else:
                click.echo(f"Failed to cancel job {job_id}.", err=True)

        except Exception as e:
            click.echo(f"Error cancelling job: {e}", err=True)

    def cmd_queue(self, job_id: str, time_str: Optional[str] = None):
        """Queue a job for execution"""
        try:
            scheduled_time = None
            if time_str:
                # Parse time string (HH:MM format)
                try:
                    hour, minute = map(int, time_str.split(':'))
                    import datetime
                    now = datetime.datetime.now()
                    scheduled_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
                    if scheduled_dt <= now:
                        scheduled_dt += datetime.timedelta(days=1)
                    scheduled_time = scheduled_dt.timestamp()
                except ValueError:
                    click.echo(f"Invalid time format: {time_str}. Use HH:MM format.")
                    return

            success = self.job_manager.queue_job(job_id, scheduled_time)
            if success:
                if scheduled_time:
                    import datetime
                    scheduled_dt = datetime.datetime.fromtimestamp(scheduled_time)
                    click.echo(f"Job {job_id} queued for {scheduled_dt.strftime('%Y-%m-%d %H:%M')}.")
                else:
                    click.echo(f"Job {job_id} queued for immediate execution.")
            else:
                click.echo(f"Failed to queue job {job_id}.", err=True)

        except Exception as e:
            click.echo(f"Error queuing job: {e}", err=True)

    def cmd_status(self, job_id: str):
        """Show detailed job status"""
        try:
            job = self.job_manager.get_job(job_id)
            if not job:
                click.echo(f"Job {job_id} not found.", err=True)
                return

            status_dict = job.get_status_dict()

            click.echo(f"Job ID: {status_dict['job_id']}")
            click.echo(f"Name: {status_dict['name']}")
            click.echo(f"Status: {status_dict['status'].upper()}")
            click.echo(f"Priority: {status_dict['priority']}")
            click.echo(f"Progress: {status_dict['progress']:.1f}%")
            click.echo(f"Current Stage: {status_dict['current_stage']}")

            if status_dict['error_message']:
                click.echo(f"Error: {status_dict['error_message']}")

            # Timing information
            created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status_dict['created_time']))
            click.echo(f"Created: {created}")

            if status_dict['started_time']:
                started = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status_dict['started_time']))
                click.echo(f"Started: {started}")

            if status_dict['completed_time']:
                completed = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(status_dict['completed_time']))
                click.echo(f"Completed: {completed}")

            if status_dict['execution_time'] > 0:
                click.echo(f"Execution Time: {status_dict['execution_time']:.2f}s")

            # Resource usage
            resources = status_dict['resources']
            click.echo(f"CPU Usage: {resources['cpu_percent']:.1f}%")
            click.echo(f"Memory Usage: {resources['memory_mb']:.1f} MB")
            click.echo(f"Peak Memory: {resources['peak_memory_mb']:.1f} MB")
            click.echo(f"Active Threads: {resources['active_threads']}")

            # File paths
            click.echo(f"Job Folder: {status_dict['folder']}")
            click.echo(f"Results Folder: {status_dict['results_folder']}")

        except Exception as e:
            click.echo(f"Error getting job status: {e}", err=True)

    def cmd_logs(self, job_id: str, lines: int = 50):
        """Show job logs"""
        try:
            job = self.job_manager.get_job(job_id)
            if not job:
                click.echo(f"Job {job_id} not found.", err=True)
                return

            if not job.logs:
                click.echo("No logs available for this job.")
                return

            # Show last N lines
            log_lines = job.logs[-lines:]
            click.echo(f"Last {len(log_lines)} log entries for job {job_id}:")
            click.echo("-" * 60)
            for log_entry in log_lines:
                click.echo(log_entry)

        except Exception as e:
            click.echo(f"Error showing logs: {e}", err=True)

    def cmd_results(self, job_id: str):
        """Open results folder for a job"""
        try:
            job = self.job_manager.get_job(job_id)
            if not job:
                click.echo(f"Job {job_id} not found.", err=True)
                return

            results_folder = Path(job.results_folder)
            if not results_folder.exists():
                click.echo(f"Results folder does not exist: {results_folder}")
                return

            # Open folder using system default
            try:
                if sys.platform == "win32":
                    os.startfile(str(results_folder))
                elif sys.platform == "darwin":
                    subprocess.run(["open", str(results_folder)])
                else:
                    subprocess.run(["xdg-open", str(results_folder)])
                click.echo(f"Opened results folder: {results_folder}")
            except Exception as e:
                click.echo(f"Failed to open folder: {e}")
                click.echo(f"Results folder path: {results_folder}")

        except Exception as e:
            click.echo(f"Error opening results: {e}", err=True)

    def cmd_create(self, name: str, template: Optional[str] = None):
        """Create a new job from template"""
        try:
            # Create job folder
            batch_jobs_dir = Path.cwd() / 'batch_jobs'
            batch_jobs_dir.mkdir(exist_ok=True)

            job_folder = batch_jobs_dir / name
            if job_folder.exists():
                click.echo(f"Job folder already exists: {job_folder}")
                return

            job_folder.mkdir()

            # Load template
            if template:
                template_dir = Path.cwd() / 'config' / 'presets' / 'batch_templates'
                template_file = template_dir / f"{template}.yaml"
                if template_file.exists():
                    # Copy template files
                    self._copy_template(template_file, job_folder)
                    click.echo(f"Created job from template '{template}': {job_folder}")
                else:
                    click.echo(f"Template not found: {template}")
                    return
            else:
                # Create basic configuration
                self._create_basic_config(job_folder, name)
                click.echo(f"Created basic job: {job_folder}")

        except Exception as e:
            click.echo(f"Error creating job: {e}", err=True)

    def cmd_config(self, max_jobs: Optional[int] = None, auto_start: Optional[bool] = None):
        """Configure batch system settings"""
        try:
            updated = False

            if max_jobs is not None:
                self.job_manager.set_max_concurrent_jobs(max_jobs)
                click.echo(f"Set max concurrent jobs to: {max_jobs}")
                updated = True

            if auto_start is not None:
                self.job_manager.set_auto_start(auto_start)
                click.echo(f"Set auto-start to: {auto_start}")
                updated = True

            if not updated:
                # Show current configuration
                stats = self.job_manager.get_statistics()
                click.echo("Current batch system configuration:")
                click.echo(f"  Max concurrent jobs: {stats['max_concurrent_jobs']}")
                click.echo(f"  Auto-start: {stats['auto_start']}")
                click.echo(f"  Active jobs: {stats['running_jobs']}")
                click.echo(f"  Queue length: {stats['queue_length']}")

        except Exception as e:
            click.echo(f"Error configuring system: {e}", err=True)

    def cmd_monitor(self):
        """Monitor system resources and job status"""
        try:
            click.echo("Monitoring batch system... (Press Ctrl+C to stop)")
            click.echo()

            try:
                while True:
                    # Clear screen
                    os.system('cls' if os.name == 'nt' else 'clear')

                    # Show system resources
                    resources = self.job_manager.get_system_resources()
                    click.echo("=== System Resources ===")
                    click.echo(f"CPU Usage: {resources['cpu_percent']:.1f}%")
                    click.echo(f"Memory Usage: {resources['memory_mb']:.1f} MB")
                    click.echo(f"Active Jobs: {resources['active_jobs']}/{resources['max_concurrent']}")
                    click.echo(f"Queue Length: {resources['queue_length']}")
                    click.echo()

                    # Show running jobs
                    running_jobs = self.job_manager.get_jobs_by_status(JobStatus.RUNNING)
                    if running_jobs:
                        click.echo("=== Running Jobs ===")
                        data = [self.format_job_info(job) for job in running_jobs]
                        headers = ['ID', 'Name', 'Status', 'Progress', 'Stage', 'Time', 'Memory']
                        click.echo(self.format_table(data, headers))
                    else:
                        click.echo("No jobs currently running.")
                    click.echo()

                    time.sleep(2)

            except KeyboardInterrupt:
                click.echo("\nMonitoring stopped.")

        except Exception as e:
            click.echo(f"Error monitoring: {e}", err=True)

    def _copy_template(self, template_file: Path, job_folder: Path):
        """Copy template files to job folder"""
        try:
            import yaml
            import shutil

            with open(template_file, 'r') as f:
                template_data = yaml.safe_load(f)

            # Create configuration files based on template
            if 'config' in template_data:
                with open(job_folder / 'config.yaml', 'w') as f:
                    yaml.dump(template_data['config'], f, default_flow_style=False)

            if 'strategy' in template_data:
                with open(job_folder / 'strategy.yaml', 'w') as f:
                    yaml.dump(template_data['strategy'], f, default_flow_style=False)

            if 'cost_model' in template_data:
                with open(job_folder / 'cost_model.yaml', 'w') as f:
                    yaml.dump(template_data['cost_model'], f, default_flow_style=False)

            if 'metrics' in template_data:
                with open(job_folder / 'metrics.yaml', 'w') as f:
                    yaml.dump(template_data['metrics'], f, default_flow_style=False)

        except Exception as e:
            raise Exception(f"Failed to copy template: {e}")

    def _create_basic_config(self, job_folder: Path, name: str):
        """Create basic job configuration"""
        import yaml

        config = {
            'name': name,
            'description': f'Batch job: {name}',
            'strategy': 'greedy',
            'max_operations': 1000,
            'max_cost': 10000
        }

        with open(job_folder / 'config.yaml', 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        strategy = {
            'strategy': 'greedy',
            'parameters': {}
        }

        with open(job_folder / 'strategy.yaml', 'w') as f:
            yaml.dump(strategy, f, default_flow_style=False)


# Create CLI commands if click is available
if CLICK_AVAILABLE:
    @click.group()
    def batch():
        """BSEE Batch Job Management CLI"""
        pass

    @batch.command()
    @click.option('--status', '-s', help='Filter by job status')
    def list(status):
        """List all batch jobs"""
        cli = BatchCLI()
        cli.cmd_list(status)

    @batch.command()
    @click.argument('job_id')
    def start(job_id):
        """Start a job"""
        cli = BatchCLI()
        cli.cmd_start(job_id)

    @batch.command()
    @click.argument('job_id')
    def pause(job_id):
        """Pause a job"""
        cli = BatchCLI()
        cli.cmd_pause(job_id)

    @batch.command()
    @click.argument('job_id')
    def resume(job_id):
        """Resume a job"""
        cli = BatchCLI()
        cli.cmd_resume(job_id)

    @batch.command()
    @click.argument('job_id')
    def cancel(job_id):
        """Cancel a job"""
        cli = BatchCLI()
        cli.cmd_cancel(job_id)

    @batch.command()
    @click.argument('job_id')
    @click.option('--time', '-t', help='Schedule time (HH:MM format)')
    def queue(job_id, time):
        """Queue a job for execution"""
        cli = BatchCLI()
        cli.cmd_queue(job_id, time)

    @batch.command()
    @click.argument('job_id')
    def status(job_id):
        """Show detailed job status"""
        cli = BatchCLI()
        cli.cmd_status(job_id)

    @batch.command()
    @click.argument('job_id')
    @click.option('--lines', '-n', default=50, help='Number of log lines to show')
    def logs(job_id, lines):
        """Show job logs"""
        cli = BatchCLI()
        cli.cmd_logs(job_id, lines)

    @batch.command()
    @click.argument('job_id')
    def results(job_id):
        """Open results folder for a job"""
        cli = BatchCLI()
        cli.cmd_results(job_id)

    @batch.command()
    @click.argument('name')
    @click.option('--template', '-t', help='Template to use')
    def create(name, template):
        """Create a new job from template"""
        cli = BatchCLI()
        cli.cmd_create(name, template)

    @batch.command()
    @click.option('--max-jobs', '-m', type=int, help='Maximum concurrent jobs')
    @click.option('--auto-start', '-a', type=bool, help='Enable auto-start')
    def config(max_jobs, auto_start):
        """Configure batch system settings"""
        cli = BatchCLI()
        cli.cmd_config(max_jobs, auto_start)

    @batch.command()
    def monitor():
        """Monitor system resources and job status"""
        cli = BatchCLI()
        cli.cmd_monitor()


def main():
    """Main CLI entry point"""
    if CLICK_AVAILABLE:
        batch()
    else:
        click.echo("Click library not available. Please install click: pip install click")
        sys.exit(1)


if __name__ == '__main__':
    main()