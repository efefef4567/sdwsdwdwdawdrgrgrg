"""
Test job creation and configuration loading
"""

import unittest
import tempfile
import shutil
import yaml
import json
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from bsee.batch import Job, JobStatus, JobPriority


class TestJobCreation(unittest.TestCase):
    """Test job creation and configuration loading"""

    def setUp(self):
        """Set up test fixtures"""
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

    def tearDown(self):
        """Clean up test fixtures"""
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

    def test_job_creation_basic(self):
        """Test basic job creation"""
        job_dir = self._create_job_config("TestJob")

        job = Job(str(job_dir))

        self.assertEqual(job.name, "TestJob")
        self.assertEqual(job.status, JobStatus.PENDING)
        self.assertEqual(job.priority, JobPriority.NORMAL)
        self.assertIsNotNone(job.job_id)
        self.assertIsNotNone(job.config)

    def test_job_creation_with_custom_id(self):
        """Test job creation with custom ID"""
        job_dir = self._create_job_config("CustomJob")
        custom_id = "CUSTOM123"

        job = Job(str(job_dir), job_id=custom_id)

        self.assertEqual(job.job_id, custom_id)

    def test_job_config_loading(self):
        """Test configuration file loading"""
        config_data = {
            "name": "ComplexJob",
            "description": "A complex test job",
            "strategy": "genetic",
            "max_operations": 5000,
            "max_cost": 25000
        }
        job_dir = self._create_job_config("ComplexJob", config_data)

        job = Job(str(job_dir))

        self.assertEqual(job.config.name, "ComplexJob")
        self.assertEqual(job.config.description, "A complex test job")
        self.assertEqual(job.config.strategy_config.get("strategy"), "genetic")

    def test_job_with_strategy_file(self):
        """Test job loading with strategy file"""
        job_dir = self._create_job_config("StrategyJob")

        # Create strategy file
        strategy_data = {
            "strategy": "genetic",
            "parameters": {
                "population_size": 100,
                "generations": 200,
                "mutation_rate": 0.1
            }
        }
        with open(job_dir / "strategy.yaml", 'w') as f:
            yaml.dump(strategy_data, f)

        job = Job(str(job_dir))

        self.assertEqual(job.config.strategy_config["strategy"], "genetic")
        self.assertEqual(job.config.strategy_config["parameters"]["population_size"], 100)

    def test_job_with_metrics_file(self):
        """Test job loading with metrics file"""
        job_dir = self._create_job_config("MetricsJob")

        # Create metrics file
        metrics_data = {
            "metrics": ["file_ideality_score", "entropy_global", "compression_ratio"],
            "target_metrics": {
                "file_ideality_score": "max",
                "entropy_global": "min"
            },
            "weights": {
                "file_ideality_score": 0.6,
                "entropy_global": 0.4
            }
        }
        with open(job_dir / "metrics.yaml", 'w') as f:
            yaml.dump(metrics_data, f)

        job = Job(str(job_dir))

        self.assertEqual(len(job.config.metrics_config["metrics"]), 3)
        self.assertEqual(job.config.metrics_config["target_metrics"]["file_ideality_score"], "max")

    def test_job_priority_from_queue_settings(self):
        """Test job priority extraction from queue settings"""
        job_dir = self._create_job_config("PriorityJob")

        # Create queue settings with high priority
        queue_data = {
            "priority": "high",
            "estimated_time": 60
        }
        with open(job_dir / "queue_settings.yaml", 'w') as f:
            yaml.dump(queue_data, f)

        job = Job(str(job_dir))

        self.assertEqual(job.priority, JobPriority.HIGH)

    def test_job_missing_config_file(self):
        """Test job creation with missing config file"""
        job_dir = self.jobs_dir / "NoConfigJob"
        job_dir.mkdir()  # Don't create config.yaml

        with self.assertRaises(FileNotFoundError):
            Job(str(job_dir))

    def test_job_invalid_yaml_config(self):
        """Test job creation with invalid YAML"""
        job_dir = self.jobs_dir / "InvalidYamlJob"
        job_dir.mkdir()

        # Create invalid YAML file
        with open(job_dir / "config.yaml", 'w') as f:
            f.write("invalid: yaml: content: [")

        job = Job(str(job_dir))
        self.assertEqual(job.status, JobStatus.FAILED)
        self.assertIn("Failed to load configuration", job.error_message)

    def test_job_status_dict(self):
        """Test job status dictionary generation"""
        job_dir = self._create_job_config("StatusTestJob")
        job = Job(str(job_dir))

        status_dict = job.get_status_dict()

        self.assertIn('job_id', status_dict)
        self.assertIn('name', status_dict)
        self.assertIn('status', status_dict)
        self.assertIn('priority', status_dict)
        self.assertIn('progress', status_dict)
        self.assertIn('current_stage', status_dict)
        self.assertIn('folder', status_dict)
        self.assertIn('results_folder', status_dict)
        self.assertIn('resources', status_dict)

    def test_job_save_status(self):
        """Test saving job status to file"""
        job_dir = self._create_job_config("SaveStatusJob")
        job = Job(str(job_dir))

        job.save_status()

        status_file = job_dir / "status.json"
        self.assertTrue(status_file.exists())

        with open(status_file, 'r') as f:
            saved_status = json.load(f)

        self.assertEqual(saved_status['job_id'], job.job_id)
        self.assertEqual(saved_status['status'], job.status.value)

    def test_job_results_folder_creation(self):
        """Test results folder creation"""
        job_dir = self._create_job_config("ResultsJob")
        job = Job(str(job_dir))

        # Results folder should be in current working directory
        expected_results = Path.cwd() / 'results' / 'ResultsJob'
        self.assertEqual(job.results_folder, expected_results)

    def test_job_logging(self):
        """Test job logging functionality"""
        job_dir = self._create_job_config("LoggingJob")
        job = Job(str(job_dir))

        # Add a log entry
        job._log("Test log message")

        self.assertEqual(len(job.logs), 1)
        self.assertIn("Test log message", job.logs[0])

    def test_job_callback_system(self):
        """Test job status callback system"""
        job_dir = self._create_job_config("CallbackJob")
        job = Job(str(job_dir))

        callback_called = False
        callback_job = None

        def test_callback(j):
            nonlocal callback_called, callback_job
            callback_called = True
            callback_job = j

        job.add_status_callback(test_callback)
        job._notify_status_change()

        self.assertTrue(callback_called)
        self.assertEqual(callback_job, job)

        job.remove_status_callback(test_callback)

    def test_multiple_jobs_creation(self):
        """Test creating multiple jobs"""
        job_names = ["Job1", "Job2", "Job3"]
        jobs = []

        for job_name in job_names:
            job_dir = self._create_job_config(job_name)
            job = Job(str(job_dir))
            jobs.append(job)

        self.assertEqual(len(jobs), 3)
        self.assertEqual(jobs[0].name, "Job1")
        self.assertEqual(jobs[1].name, "Job2")
        self.assertEqual(jobs[2].name, "Job3")

        # Ensure all jobs have unique IDs
        job_ids = [job.job_id for job in jobs]
        self.assertEqual(len(set(job_ids)), len(job_ids))


if __name__ == '__main__':
    unittest.main()