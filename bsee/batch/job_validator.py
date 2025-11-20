"""
Job Validator Implementation
Validation and health checking for job configurations.
"""

import os
import yaml
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import re

from ...utils.logger import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Job validation error"""
    pass


class JobValidator:
    """Validate job configurations and provide detailed error reporting"""

    def __init__(self):
        """Initialize job validator"""
        self.required_config_fields = [
            'name',
            'description'
        ]

        self.valid_strategies = [
            'greedy', 'random', 'genetic', 'simulated_annealing',
            'hill_climbing', 'beam_search', 'depth_first', 'breadth_first'
        ]

        self.valid_metrics = [
            'file_ideality_score', 'entropy_global', 'entropy_local',
            'lz77_ratio', 'bzip2_ratio', 'gzip_ratio', 'compression_ratio',
            'pattern_density', 'repetitiveness', 'complexity_score'
        ]

        self.valid_cost_models = [
            'linear', 'exponential', 'logarithmic', 'custom'
        ]

    def validate_job_folder(self, folder_path: str) -> bool:
        """
        Validate job folder and all configuration files

        Args:
            folder_path: Path to job configuration folder

        Returns:
            bool: True if valid
        """
        try:
            folder = Path(folder_path)

            if not folder.exists():
                logger.error(f"Job folder does not exist: {folder_path}")
                return False

            if not folder.is_dir():
                logger.error(f"Job path is not a directory: {folder_path}")
                return False

            # Validate required files exist
            if not self._validate_required_files(folder):
                return False

            # Validate configuration files
            config_valid, config_errors = self._validate_config_file(folder)
            if not config_valid:
                logger.error(f"Configuration validation failed: {config_errors}")
                return False

            # Validate optional files if they exist
            strategy_valid, strategy_errors = self._validate_strategy_file(folder)
            if not strategy_valid:
                logger.error(f"Strategy validation failed: {strategy_errors}")
                return False

            cost_valid, cost_errors = self._validate_cost_model_file(folder)
            if not cost_valid:
                logger.error(f"Cost model validation failed: {cost_errors}")
                return False

            metrics_valid, metrics_errors = self._validate_metrics_file(folder)
            if not metrics_valid:
                logger.error(f"Metrics validation failed: {metrics_errors}")
                return False

            # Validate cross-file consistency
            consistency_valid, consistency_errors = self._validate_file_consistency(folder)
            if not consistency_valid:
                logger.error(f"Consistency validation failed: {consistency_errors}")
                return False

            return True

        except Exception as e:
            logger.error(f"Job folder validation error: {e}")
            return False

    def _validate_required_files(self, folder: Path) -> bool:
        """Validate that required files exist"""
        required_files = ['config.yaml']

        for required_file in required_files:
            file_path = folder / required_file
            if not file_path.exists():
                logger.error(f"Required file missing: {file_path}")
                return False

            if not file_path.is_file():
                logger.error(f"Required path is not a file: {file_path}")
                return False

        return True

    def _validate_config_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate main configuration file"""
        errors = []
        config_file = folder / 'config.yaml'

        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)

            if not config:
                errors.append("Configuration file is empty")
                return False, errors

            # Check required fields
            for field in self.required_config_fields:
                if field not in config:
                    errors.append(f"Missing required field: {field}")

            # Validate name
            if 'name' in config:
                name = str(config['name'])
                if not re.match(r'^[a-zA-Z0-9_-]+$', name):
                    errors.append("Job name contains invalid characters")
                if len(name) > 50:
                    errors.append("Job name too long (max 50 characters)")

            # Validate description
            if 'description' in config:
                if len(str(config['description'])) > 500:
                    errors.append("Description too long (max 500 characters)")

            return len(errors) == 0, errors

        except yaml.YAMLError as e:
            errors.append(f"YAML parsing error: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"Configuration file error: {e}")
            return False, errors

    def _validate_strategy_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate strategy configuration file"""
        errors = []
        strategy_file = folder / 'strategy.yaml'

        if not strategy_file.exists():
            return True, errors  # Optional file

        try:
            with open(strategy_file, 'r') as f:
                strategy = yaml.safe_load(f)

            if not strategy:
                errors.append("Strategy file is empty")
                return False, errors

            # Validate strategy name
            if 'strategy' in strategy:
                strategy_name = strategy['strategy']
                if strategy_name not in self.valid_strategies:
                    errors.append(f"Invalid strategy: {strategy_name}")

            # Validate strategy parameters
            if 'parameters' in strategy:
                params = strategy['parameters']
                if not isinstance(params, dict):
                    errors.append("Strategy parameters must be a dictionary")

                # Validate common parameters based on strategy
                strategy_name = strategy.get('strategy', '')
                if strategy_name == 'genetic':
                    genetic_params = ['population_size', 'generations', 'mutation_rate', 'crossover_rate']
                    for param in genetic_params:
                        if param in params and not isinstance(params[param], (int, float)):
                            errors.append(f"Invalid parameter type for {param}")

                elif strategy_name == 'simulated_annealing':
                    sa_params = ['initial_temperature', 'cooling_rate', 'min_temperature']
                    for param in sa_params:
                        if param in params and not isinstance(params[param], (int, float)):
                            errors.append(f"Invalid parameter type for {param}")

            return len(errors) == 0, errors

        except yaml.YAMLError as e:
            errors.append(f"Strategy YAML parsing error: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"Strategy file error: {e}")
            return False, errors

    def _validate_cost_model_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate cost model configuration file"""
        errors = []
        cost_file = folder / 'cost_model.yaml'

        if not cost_file.exists():
            return True, errors  # Optional file

        try:
            with open(cost_file, 'r') as f:
                cost_model = yaml.safe_load(f)

            if not cost_model:
                errors.append("Cost model file is empty")
                return False, errors

            # Validate cost model type
            if 'type' in cost_model:
                cost_type = cost_model['type']
                if cost_type not in self.valid_cost_models:
                    errors.append(f"Invalid cost model type: {cost_type}")

            # Validate cost parameters
            if 'parameters' in cost_model:
                params = cost_model['parameters']
                if not isinstance(params, dict):
                    errors.append("Cost model parameters must be a dictionary")

                # Validate parameter values are numeric
                for key, value in params.items():
                    if not isinstance(value, (int, float)):
                        errors.append(f"Cost parameter {key} must be numeric")

            return len(errors) == 0, errors

        except yaml.YAMLError as e:
            errors.append(f"Cost model YAML parsing error: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"Cost model file error: {e}")
            return False, errors

    def _validate_metrics_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate metrics configuration file"""
        errors = []
        metrics_file = folder / 'metrics.yaml'

        if not metrics_file.exists():
            return True, errors  # Optional file

        try:
            with open(metrics_file, 'r') as f:
                metrics = yaml.safe_load(f)

            if not metrics:
                errors.append("Metrics file is empty")
                return False, errors

            # Validate metrics list
            if 'metrics' in metrics:
                metrics_list = metrics['metrics']
                if not isinstance(metrics_list, list):
                    errors.append("Metrics must be a list")
                else:
                    for metric in metrics_list:
                        if metric not in self.valid_metrics:
                            errors.append(f"Invalid metric: {metric}")

            # Validate target metrics
            if 'target_metrics' in metrics:
                target_metrics = metrics['target_metrics']
                if not isinstance(target_metrics, dict):
                    errors.append("Target metrics must be a dictionary")
                else:
                    for metric, target in target_metrics.items():
                        if metric not in self.valid_metrics:
                            errors.append(f"Invalid target metric: {metric}")
                        if target not in ['min', 'max']:
                            errors.append(f"Invalid target direction for {metric}: {target}")

            return len(errors) == 0, errors

        except yaml.YAMLError as e:
            errors.append(f"Metrics YAML parsing error: {e}")
            return False, errors
        except Exception as e:
            errors.append(f"Metrics file error: {e}")
            return False, errors

    def _validate_file_consistency(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate consistency between configuration files"""
        errors = []

        try:
            # Load all configuration files
            config = self._load_yaml_safe(folder / 'config.yaml')
            strategy = self._load_yaml_safe(folder / 'strategy.yaml')
            cost_model = self._load_yaml_safe(folder / 'cost_model.yaml')
            metrics = self._load_yaml_safe(folder / 'metrics.yaml')

            # Check strategy referenced in config exists
            if strategy and 'strategy' in config and 'strategy' in strategy:
                if config.get('strategy') != strategy.get('strategy'):
                    errors.append("Strategy mismatch between config and strategy files")

            # Validate resource limits are reasonable
            if 'resource_limits' in config:
                limits = config['resource_limits']
                if 'max_memory_mb' in limits:
                    if not isinstance(limits['max_memory_mb'], int) or limits['max_memory_mb'] <= 0:
                        errors.append("Invalid max_memory_mb value")
                if 'max_execution_time' in limits:
                    if not isinstance(limits['max_execution_time'], (int, float)) or limits['max_execution_time'] <= 0:
                        errors.append("Invalid max_execution_time value")

            return len(errors) == 0, errors

        except Exception as e:
            errors.append(f"Consistency validation error: {e}")
            return False, errors

    def _load_yaml_safe(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Safely load YAML file"""
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f)
            return None
        except Exception:
            return None

    def estimate_resources(self, folder_path: str) -> Dict[str, Any]:
        """
        Estimate resource requirements for a job

        Args:
            folder_path: Path to job folder

        Returns:
            Dict with resource estimates
        """
        try:
            folder = Path(folder_path)

            # Load configuration
            config = self._load_yaml_safe(folder / 'config.yaml')
            strategy = self._load_yaml_safe(folder / 'strategy.yaml')
            cost_model = self._load_yaml_safe(folder / 'cost_model.yaml')

            # Base estimates
            estimates = {
                'estimated_memory_mb': 512,
                'estimated_execution_time': 300,  # 5 minutes
                'estimated_cpu_cores': 2,
                'estimated_disk_space_mb': 100
            }

            # Adjust based on strategy
            if strategy:
                strategy_name = strategy.get('strategy', '')
                if strategy_name == 'genetic':
                    estimates['estimated_cpu_cores'] = 4
                    estimates['estimated_execution_time'] *= 2
                    estimates['estimated_memory_mb'] *= 1.5
                elif strategy_name == 'simulated_annealing':
                    estimates['estimated_execution_time'] *= 1.5

            # Adjust based on resource limits in config
            if config and 'resource_limits' in config:
                limits = config['resource_limits']
                if 'max_memory_mb' in limits:
                    estimates['estimated_memory_mb'] = min(estimates['estimated_memory_mb'], limits['max_memory_mb'])

            return estimates

        except Exception as e:
            logger.error(f"Error estimating resources: {e}")
            return {
                'estimated_memory_mb': 512,
                'estimated_execution_time': 300,
                'estimated_cpu_cores': 2,
                'estimated_disk_space_mb': 100
            }

    def get_validation_summary(self, folder_path: str) -> Dict[str, Any]:
        """
        Get detailed validation summary for a job folder

        Args:
            folder_path: Path to job folder

        Returns:
            Dict with validation results
        """
        folder = Path(folder_path)

        summary = {
            'valid': False,
            'folder_exists': folder.exists() and folder.is_dir(),
            'required_files': {},
            'optional_files': {},
            'errors': [],
            'warnings': [],
            'resource_estimates': {}
        }

        if not summary['folder_exists']:
            summary['errors'].append("Job folder does not exist")
            return summary

        # Check file existence
        required_files = ['config.yaml']
        optional_files = ['strategy.yaml', 'cost_model.yaml', 'metrics.yaml', 'queue_settings.yaml']

        for file_name in required_files:
            file_path = folder / file_name
            summary['required_files'][file_name] = file_path.exists()

        for file_name in optional_files:
            file_path = folder / file_name
            summary['optional_files'][file_name] = file_path.exists()

        # Validate configuration
        config_valid, config_errors = self._validate_config_file(folder)
        summary['errors'].extend(config_errors)

        # Validate strategy if exists
        strategy_file = folder / 'strategy.yaml'
        if strategy_file.exists():
            strategy_valid, strategy_errors = self._validate_strategy_file(folder)
            summary['errors'].extend(strategy_errors)

        # Get resource estimates
        if all(summary['required_files'].values()):
            summary['resource_estimates'] = self.estimate_resources(folder_path)

        summary['valid'] = len(summary['errors']) == 0 and all(summary['required_files'].values())

        return summary