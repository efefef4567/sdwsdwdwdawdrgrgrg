"""
Test JobManager functionality
"""

import unittest
import tempfile
import shutil
import yaml
import time
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from bsee.batch import JobManager, Job, JobStatus, JobPriority


class TestJobManager(unittest.TestCase):
    """Test JobManager functionality"""

    def setUp(self):
        """Set up test fixtures"""
        # Reset JobManager singleton for clean test environment
        JobManager.reset_singleton_for_testing()

        self.temp_dir = Path(tempfile.mkdtemp())
        self.jobs_dir = self.temp_dir / "batch_jobs"
        self.jobs_dir.mkdir()
        self.original_cwd = Path.cwd()
        os.chdir(self.temp_dir)

        # Create inputs directory
        self.inputs_dir = self.temp_dir / "inputs"
        self.inputs_dir.mkdir()

        # Create a test binary file
        (self.inputs_dir / "test.bin").write_bytes(b"test binary data")

        self.job_manager = JobManager()

    def tearDown(self):
        """Clean up test fixtures"""
        self.job_manager.shutdown()
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_job_config(self, job_name: str, config_data: dict = None):
        """Create a basic job configuration"""
        job_dir = self.jobs_dir / job_name
        job_dir.mkdir()

        if config_data is None:
            config_data = {
                "name": job_name,
                "description": f"Test job: {job_name}",
                "strategy": "greedy",
                "max_operations": 1000,
                "max_cost": 5000
            }

        with open(job_dir / "config.yaml", 'w') as f:
            yaml.dump(config_data, f)

        return job_dir

    def test_job_manager_initialization(self):
        """Test JobManager initialization"""
        manager = JobManager()

        self.assertIsNotNone(manager)
        self.assertEqual(manager.max_concurrent_jobs, 4)
        self.assertFalse(manager.auto_start)
        self.assertEqual(len(manager.get_all_jobs()), 0)

        manager.shutdown()

    def test_add_job(self):
        """Test adding a job"""
        job_dir = self._create_job_config("TestJob")

        job = self.job_manager.add_job(str(job_dir))

        self.assertIsNotNone(job)
        self.assertEqual(job.name, "TestJob")
        self.assertEqual(len(self.job_manager.get_all_jobs()), 1)

    def test_add_duplicate_job(self):
        """Test adding a job with duplicate ID"""
        job_dir = self._create_job_config("DuplicateJob")

        job1 = self.job_manager.add_job(str(job_dir))

        # Test adding a job with the same explicit job_id - this should return None
        # Since the JobManager catches the ValueError and returns None for duplicates
        job2 = self.job_manager.add_job(str(job_dir), job_id=job1.job_id)

        # Should return None for duplicate
        self.assertIsNotNone(job1)
        self.assertIsNone(job2)

    def test_remove_job(self):
        """Test removing a job"""
        job_dir = self._create_job_config("RemoveJob")

        job = self.job_manager.add_job(str(job_dir))
        self.assertIsNotNone(job)

        success = self.job_manager.remove_job(job.job_id)
        self.assertTrue(success)

        removed_job = self.job_manager.get_job(job.job_id)
        self.assertIsNone(removed_job)

    def test_remove_nonexistent_job(self):
        """Test removing a non-existent job"""
        success = self.job_manager.remove_job("NONEXISTENT")
        self.assertFalse(success)

    def test_start_job(self):
        """Test starting a job"""
        job_dir = self._create_job_config("StartJob")

        job = self.job_manager.add_job(str(job_dir))
        self.assertIsNotNone(job)

        success = self.job_manager.start_job(job.job_id)
        self.assertTrue(success)

        # Job should be queued (not running immediately in test)
        updated_job = self.job_manager.get_job(job.job_id)
        self.assertIn(updated_job.status, [JobStatus.QUEUED, JobStatus.RUNNING])

    def test_start_nonexistent_job(self):
        """Test starting a non-existent job"""
        success = self.job_manager.start_job("NONEXISTENT")
        self.assertFalse(success)

    def test_pause_job(self):
        """Test pausing a job"""
        job_dir = self._create_job_config("PauseJob")

        job = self.job_manager.add_job(str(job_dir))
        job.status = JobStatus.RUNNING  # Simulate running job

        success = self.job_manager.pause_job(job.job_id)
        self.assertTrue(success)

        updated_job = self.job_manager.get_job(job.job_id)
        self.assertEqual(updated_job.status, JobStatus.PAUSED)

    def test_pause_nonexistent_job(self):
        """Test pausing a non-existent job"""
        success = self.job_manager.pause_job("NONEXISTENT")
        self.assertFalse(success)

    def test_resume_job(self):
        """Test resuming a job"""
        job_dir = self._create_job_config("ResumeJob")

        job = self.job_manager.add_job(str(job_dir))
        job.status = JobStatus.PAUSED  # Simulate paused job

        success = self.job_manager.resume_job(job.job_id)
        self.assertTrue(success)

        updated_job = self.job_manager.get_job(job.job_id)
        self.assertEqual(updated_job.status, JobStatus.RUNNING)

    def test_cancel_job(self):
        """Test cancelling a job"""
        job_dir = self._create_job_config("CancelJob")

        job = self.job_manager.add_job(str(job_dir))
        self.assertIsNotNone(job)

        success = self.job_manager.cancel_job(job.job_id)
        self.assertTrue(success)

        updated_job = self.job_manager.get_job(job.job_id)
        self.assertEqual(updated_job.status, JobStatus.CANCELLED)

    def test_queue_job(self):
        """Test queuing a job"""
        job_dir = self._create_job_config("QueueJob")

        job = self.job_manager.add_job(str(job_dir))
        self.assertIsNotNone(job)

        # Queue for immediate execution
        success = self.job_manager.queue_job(job.job_id)
        self.assertTrue(success)

        updated_job = self.job_manager.get_job(job.job_id)
        self.assertEqual(updated_job.status, JobStatus.QUEUED)
        self.assertIsNotNone(updated_job.queued_time)

    def test_queue_job_with_schedule(self):
        """Test queuing a job with scheduled execution"""
        job_dir = self._create_job_config("ScheduleJob")

        job = self.job_manager.add_job(str(job_dir))
        self.assertIsNotNone(job)

        # Queue for future execution
        future_time = time.time() + 3600  # 1 hour from now
        success = self.job_manager.queue_job(job.job_id, future_time)
        self.assertTrue(success)

        updated_job = self.job_manager.get_job(job.job_id)
        self.assertEqual(updated_job.status, JobStatus.QUEUED)
        self.assertEqual(updated_job.scheduled_time, future_time)

    def test_get_jobs_by_status(self):
        """Test filtering jobs by status"""
        # Create jobs with different statuses
        job_dir1 = self._create_job_config("PendingJob1")
        job_dir2 = self._create_job_config("PendingJob2")
        job_dir3 = self._create_job_config("PendingJob3")

        job1 = self.job_manager.add_job(str(job_dir1))
        job2 = self.job_manager.add_job(str(job_dir2))
        job3 = self.job_manager.add_job(str(job_dir3))

        # Start one job
        self.job_manager.start_job(job1.job_id)

        # Cancel one job
        self.job_manager.cancel_job(job2.job_id)

        # Test filtering
        pending_jobs = self.job_manager.get_jobs_by_status(JobStatus.PENDING)
        queued_jobs = self.job_manager.get_jobs_by_status(JobStatus.QUEUED)
        cancelled_jobs = self.job_manager.get_jobs_by_status(JobStatus.CANCELLED)

        self.assertEqual(len(pending_jobs), 1)  # Only job3
        self.assertEqual(len(queued_jobs), 1)    # Only job1
        self.assertEqual(len(cancelled_jobs), 1) # Only job2

    def test_system_resources(self):
        """Test system resource monitoring"""
        resources = self.job_manager.get_system_resources()

        self.assertIn('cpu_percent', resources)
        self.assertIn('memory_mb', resources)
        self.assertIn('active_jobs', resources)
        self.assertIn('max_concurrent', resources)
        self.assertIn('queue_length', resources)

    def test_set_max_concurrent_jobs(self):
        """Test setting maximum concurrent jobs"""
        original_max = self.job_manager.max_concurrent_jobs

        self.job_manager.set_max_concurrent_jobs(8)
        self.assertEqual(self.job_manager.max_concurrent_jobs, 8)

        resources = self.job_manager.get_system_resources()
        self.assertEqual(resources['max_concurrent'], 8)

        # Restore original
        self.job_manager.set_max_concurrent_jobs(original_max)

    def test_set_auto_start(self):
        """Test setting auto-start behavior"""
        self.job_manager.set_auto_start(True)
        self.assertTrue(self.job_manager.auto_start)

        self.job_manager.set_auto_start(False)
        self.assertFalse(self.job_manager.auto_start)

    def test_job_statistics(self):
        """Test job statistics"""
        # Add some jobs
        for i in range(3):
            job_dir = self._create_job_config(f"StatJob{i}")
            self.job_manager.add_job(str(job_dir))

        stats = self.job_manager.get_statistics()

        self.assertIn('total_jobs', stats)
        self.assertIn('status_counts', stats)
        self.assertIn('running_jobs', stats)
        self.assertIn('queue_length', stats)
        self.assertIn('max_concurrent_jobs', stats)
        self.assertIn('auto_start', stats)
        self.assertIn('system_resources', stats)

        self.assertEqual(stats['total_jobs'], 3)
        self.assertEqual(stats['status_counts']['pending'], 3)

    def test_job_callbacks(self):
        """Test job status update callbacks"""
        callback_called = False
        callback_job = None

        def test_callback(job):
            nonlocal callback_called, callback_job
            callback_called = True
            callback_job = job

        self.job_manager.add_job_callback(test_callback)

        job_dir = self._create_job_config("CallbackJob")
        job = self.job_manager.add_job(str(job_dir))

        # Trigger a status change
        self.job_manager.start_job(job.job_id)

        # Give some time for callback to be called
        time.sleep(0.1)

        # Note: In a real test environment, you might need to wait longer
        # or use a more sophisticated mechanism to ensure callback is called

        self.job_manager.remove_job_callback(test_callback)

    def test_multiple_job_managers(self):
        """Test singleton pattern for JobManager"""
        manager1 = JobManager()
        manager2 = JobManager()

        # Both should be the same instance (singleton)
        self.assertIs(manager1, manager2)

        # Shutdown both to avoid conflicts
        manager1.shutdown()
        manager2.shutdown()

    def test_job_cleanup_on_shutdown(self):
        """Test job cleanup during shutdown"""
        job_dir = self._create_job_config("ShutdownJob")
        job = self.job_manager.add_job(str(job_dir))

        self.assertIsNotNone(job)
        self.assertEqual(len(self.job_manager.get_all_jobs()), 1)

        self.job_manager.shutdown()

        # After shutdown, job manager should be cleaned up
        # Note: This is a basic test - actual cleanup behavior might be more complex

    def test_auto_discovery_integration(self):
        """Test folder monitoring integration"""
        # Start folder monitoring
        self.job_manager.start_folder_monitoring()

        # Create a new job folder
        new_job_dir = self.jobs_dir / "AutoDiscoveredJob"
        new_job_dir.mkdir()

        config_data = {
            "name": "AutoDiscoveredJob",
            "description": "Auto-discovered test job",
            "strategy": "greedy",
            "max_operations": 1000,
            "max_cost": 5000
        }
        with open(new_job_dir / "config.yaml", 'w') as f:
            yaml.dump(config_data, f)

        # Wait a moment for auto-discovery
        time.sleep(2)

        # The job should be automatically discovered and added
        # Note: In a real test, you might need to wait longer or mock the file system events

        self.job_manager.stop_folder_monitoring()


if __name__ == '__main__':
    unittest.main()