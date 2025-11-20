"""
Test folder monitoring and auto-discovery
"""

import unittest
import tempfile
import shutil
import yaml
import time
import threading
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from bsee.batch import FolderMonitor, JobValidator


class TestFolderMonitor(unittest.TestCase):
    """Test folder monitoring functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.monitor_dir = self.temp_dir / "batch_jobs"
        self.monitor_dir.mkdir()
        self.original_cwd = Path.cwd()
        os.chdir(self.temp_dir)

        self.callback_events = []
        self.callback_lock = threading.Lock()

    def tearDown(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _callback_handler(self, folder_path, event_type):
        """Callback handler for folder events"""
        with self.callback_lock:
            self.callback_events.append({
                'folder_path': folder_path,
                'event_type': event_type,
                'timestamp': time.time()
            })

    def _create_job_config(self, job_name: str):
        """Create a basic job configuration"""
        job_dir = self.monitor_dir / job_name
        job_dir.mkdir()

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

    def test_folder_monitor_initialization(self):
        """Test folder monitor initialization"""
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)

        self.assertIsNotNone(monitor)
        self.assertEqual(str(monitor.monitor_path), str(self.monitor_dir))
        self.assertFalse(monitor.running)

    def test_folder_monitor_start_stop(self):
        """Test starting and stopping folder monitoring"""
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)

        monitor.start()
        self.assertTrue(monitor.running)

        monitor.stop()
        self.assertFalse(monitor.running)

    def test_folder_creation_detection(self):
        """Test detection of new folder creation"""
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)
        monitor.start()

        # Create a job folder
        job_dir = self._create_job_config("TestJob")

        # Wait for event processing
        time.sleep(1)

        monitor.stop()

        # Check if callback was called
        with self.callback_lock:
            self.assertGreater(len(self.callback_events), 0)

            # Find the creation event
            creation_event = None
            for event in self.callback_events:
                if event['event_type'].name == 'CREATED' and 'TestJob' in event['folder_path']:
                    creation_event = event
                    break

            self.assertIsNotNone(creation_event)

    def test_folder_validation(self):
        """Test job folder validation"""
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)

        # Test invalid folder (no config.yaml)
        invalid_dir = self.monitor_dir / "InvalidJob"
        invalid_dir.mkdir()

        self.assertFalse(monitor._is_valid_job_folder(str(invalid_dir)))

        # Test valid folder (with config.yaml)
        valid_dir = self._create_job_config("ValidJob")
        self.assertTrue(monitor._is_valid_job_folder(str(valid_dir)))

    def test_folder_monitor_status(self):
        """Test folder monitor status reporting"""
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)

        status = monitor.get_status()

        self.assertIn('running', status)
        self.assertIn('monitor_path', status)
        self.assertIn('monitoring_type', status)
        self.assertIn('known_folders', status)
        self.assertIn('watchdog_available', status)

    def test_polling_fallback(self):
        """Test polling fallback when watchdog is not available"""
        # Test with polling (even if watchdog is available)
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)
        monitor.start()

        # Create a folder
        job_dir = self._create_job_config("PollingJob")

        # Wait for polling
        time.sleep(3)  # Give more time for polling

        monitor.stop()

        # Check if folder was discovered
        with self.callback_lock:
            found_creation = any(
                event['event_type'].name == 'CREATED' and 'PollingJob' in event['folder_path']
                for event in self.callback_events
            )
            self.assertTrue(found_creation, f"Events: {self.callback_events}")

    def test_multiple_folder_creation(self):
        """Test detection of multiple folder creations"""
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)
        monitor.start()

        # Create multiple job folders
        job_names = ["Job1", "Job2", "Job3"]
        created_dirs = []

        for job_name in job_names:
            job_dir = self._create_job_config(job_name)
            created_dirs.append(job_dir)
            time.sleep(0.5)  # Small delay between creations

        # Wait for event processing
        time.sleep(2)

        monitor.stop()

        # Check all folders were detected
        with self.callback_lock:
            detected_jobs = set()
            for event in self.callback_events:
                if event['event_type'].name == 'CREATED':
                    for job_name in job_names:
                        if job_name in event['folder_path']:
                            detected_jobs.add(job_name)

            self.assertEqual(len(detected_jobs), len(job_names))

    def test_folder_deletion_detection(self):
        """Test detection of folder deletion"""
        monitor = FolderMonitor(str(self.monitor_dir), self._callback_handler)

        # Create a folder first
        job_dir = self._create_job_config("DeleteTestJob")
        monitor.start()

        # Small delay to ensure creation is processed
        time.sleep(1)

        # Delete the folder
        shutil.rmtree(job_dir)

        # Wait for deletion event
        time.sleep(2)

        monitor.stop()

        # Check for deletion event
        with self.callback_lock:
            deletion_events = [
                event for event in self.callback_events
                if event['event_type'].name == 'DELETED'
            ]
            self.assertGreater(len(deletion_events), 0)


class TestJobValidator(unittest.TestCase):
    """Test job validation functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_job_folder(self, job_name: str, files: dict = None):
        """Create a job folder with specified files"""
        job_dir = Path(job_name)
        job_dir.mkdir()

        if files is None:
            files = {
                'config.yaml': {
                    "name": job_name,
                    "description": f"Test job: {job_name}",
                    "strategy": "greedy",
                    "max_operations": 1000,
                    "max_cost": 5000
                }
            }

        for filename, content in files.items():
            file_path = job_dir / filename
            if isinstance(content, dict):
                with open(file_path, 'w') as f:
                    yaml.dump(content, f, default_flow_style=False)
            else:
                with open(file_path, 'w') as f:
                    f.write(str(content))

        return job_dir

    def test_job_validator_initialization(self):
        """Test job validator initialization"""
        validator = JobValidator()
        self.assertIsNotNone(validator)

    def test_validate_valid_job(self):
        """Test validation of valid job"""
        validator = JobValidator()

        # Create a complete job folder
        job_dir = self._create_job_folder("ValidJob")

        result = validator.validate_job_folder(str(job_dir))
        self.assertTrue(result)

    def test_validate_missing_config(self):
        """Test validation with missing config file"""
        validator = JobValidator()

        # Create job folder without config.yaml
        job_dir = Path("MissingConfigJob")
        job_dir.mkdir()

        result = validator.validate_job_folder(str(job_dir))
        self.assertFalse(result)

    def test_validate_invalid_yaml(self):
        """Test validation with invalid YAML"""
        validator = JobValidator()

        # Create job folder with invalid YAML
        job_dir = Path("InvalidYamlJob")
        job_dir.mkdir()

        with open(job_dir / "config.yaml", 'w') as f:
            f.write("invalid: yaml: content:[")

        result = validator.validate_job_folder(str(job_dir))
        self.assertFalse(result)

    def test_validate_invalid_job_name(self):
        """Test validation with invalid job name"""
        validator = JobValidator()

        # Create job with invalid name (too long)
        long_name = "A" * 100
        config_data = {
            "name": long_name,
            "description": "Job with invalid name",
            "strategy": "greedy",
            "max_operations": 1000,
            "max_cost": 5000
        }

        job_dir = self._create_job_folder("InvalidNameJob", {'config.yaml': config_data})

        result = validator.validate_job_folder(str(job_dir))
        # Should still be valid but with warnings
        self.assertTrue(result)

    def test_validate_invalid_strategy(self):
        """Test validation with invalid strategy"""
        validator = JobValidator()

        strategy_data = {
            "strategy": "invalid_strategy",
            "parameters": {}
        }

        job_dir = self._create_job_folder("InvalidStrategyJob", {
            'config.yaml': {
                "name": "InvalidStrategyJob",
                "strategy": "greedy"
            },
            'strategy.yaml': strategy_data
        })

        result = validator.validate_job_folder(str(job_dir))
        # Should still be valid but with warnings
        self.assertTrue(result)

    def test_validate_invalid_cost_model_type(self):
        """Test validation with invalid cost model type"""
        validator = JobValidator()

        cost_data = {
            "type": "invalid_cost_model",
            "parameters": {}
        }

        job_dir = self._create_job_folder("InvalidCostJob", {
            'config.yaml': {
                "name": "InvalidCostJob",
                "strategy": "greedy"
            },
            'cost_model.yaml': cost_data
        })

        result = validator.validate_job_folder(str(job_dir))
        # Should still be valid but with warnings
        self.assertTrue(result)

    def test_validate_invalid_metrics(self):
        """Test validation with invalid metrics"""
        validator = JobValidator()

        metrics_data = {
            "metrics": ["invalid_metric"],
            "target_metrics": {
                "invalid_metric": "invalid_direction"
            }
        }

        job_dir = self._create_job_folder("InvalidMetricsJob", {
            'config.yaml': {
                "name": "InvalidMetricsJob",
                "strategy": "greedy"
            },
            'metrics.yaml': metrics_data
        })

        result = validator.validate_job_folder(str(job_dir))
        # Should still be valid but with warnings
        self.assertTrue(result)

    def test_validation_summary(self):
        """Test validation summary generation"""
        validator = JobValidator()

        # Create a job with some issues
        job_dir = self._create_job_folder("SummaryTestJob", {
            'config.yaml': {
                "name": "SummaryTestJob",
                "description": "Job for testing validation summary",
                "strategy": "greedy",
                "max_operations": 1000,
                "max_cost": 5000
            },
            'strategy.yaml': {
                "strategy": "invalid_strategy",
                "parameters": {}
            }
        })

        summary = validator.get_validation_summary(str(job_dir))

        self.assertIn('job_folder', summary)
        self.assertIn('overall_status', summary)
        self.assertIn('validation_timestamp', summary)
        self.assertIn('summary', summary)
        self.assertIn('results', summary)
        self.assertIn('recommendations', summary)
        self.assertIn('can_proceed', summary)

        # Should have validation results
        self.assertGreater(len(summary['results']), 0)

    def test_estimating_resources(self):
        """Test resource estimation for jobs"""
        validator = JobValidator()

        job_dir = self._create_job_folder("ResourceTestJob")

        estimates = validator.estimate_resources(str(job_dir))

        self.assertIn('estimated_memory_mb', estimates)
        self.assertIn('estimated_execution_time', estimates)
        self.assertIn('estimated_cpu_cores', estimates)
        self.assertIn('estimated_disk_space_mb', estimates)

        # Should have reasonable default values
        self.assertGreater(estimates['estimated_memory_mb'], 0)
        self.assertGreater(estimates['estimated_execution_time'], 0)
        self.assertGreater(estimates['estimated_cpu_cores'], 0)

    def test_cross_file_consistency_validation(self):
        """Test cross-file consistency validation"""
        validator = JobValidator()

        # Create job with strategy mismatch
        job_dir = self._create_job_folder("ConsistencyTestJob", {
            'config.yaml': {
                "name": "ConsistencyTestJob",
                "description": "Test job for consistency validation",
                "strategy": "greedy"  # Different from strategy.yaml
            },
            'strategy.yaml': {
                "strategy": "genetic",
                "parameters": {}
            }
        })

        result = validator.validate_job_folder(str(job_dir))
        # Should still be valid but with warnings
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()