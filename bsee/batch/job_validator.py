"""
# DISABLED: Job Validator Implementation
# DISABLED: Validation and health checking for job configurations.
"""

# DISABLED: import os
# DISABLED: import yaml
# DISABLED: import json
# DISABLED: from typing import Dict, Any, List, Optional, Tuple
# DISABLED: from pathlib import Path
# DISABLED: import re

# DISABLED: from bsee.utils.logger import get_logger

# DISABLED: logger = get_logger(__name__)


# DISABLED: class ValidationError(Exception):
    """Job validation error"""
# DISABLED:     pass


# DISABLED: class JobValidator:
    """Validate job configurations and provide detailed error reporting"""

# DISABLED:     def __init__(self):
        """Initialize job validator"""
# DISABLED:         self.required_config_fields = [
# DISABLED:             'name',
# DISABLED:             'description'
# DISABLED:         ]

# DISABLED:         self.valid_strategies = [
# DISABLED:             'greedy', 'random', 'genetic', 'simulated_annealing',
# DISABLED:             'hill_climbing', 'beam_search', 'depth_first', 'breadth_first'
# DISABLED:         ]

# DISABLED:         self.valid_metrics = [
# DISABLED:             'file_ideality_score', 'entropy_global', 'entropy_local',
# DISABLED:             'lz77_ratio', 'bzip2_ratio', 'gzip_ratio', 'compression_ratio',
# DISABLED:             'pattern_density', 'repetitiveness', 'complexity_score'
# DISABLED:         ]

# DISABLED:         self.valid_cost_models = [
# DISABLED:             'linear', 'exponential', 'logarithmic', 'custom'
# DISABLED:         ]

# DISABLED:     def validate_job_folder(self, folder_path: str) -> bool:
        """
# DISABLED:         Validate job folder and all configuration files

# DISABLED:         Args:
# DISABLED:             folder_path: Path to job configuration folder

# DISABLED:         Returns:
# DISABLED:             bool: True if valid
        """
# DISABLED:         try:
# DISABLED:             folder = Path(folder_path)

# DISABLED:             if not folder.exists():
# DISABLED:                 logger.error(f"Job folder does not exist: {folder_path}")
# DISABLED:                 return False

# DISABLED:             if not folder.is_dir():
# DISABLED:                 logger.error(f"Job path is not a directory: {folder_path}")
# DISABLED:                 return False

            # Validate required files exist
# DISABLED:             if not self._validate_required_files(folder):
# DISABLED:                 return False

            # Validate configuration files
# DISABLED:             config_valid, config_errors = self._validate_config_file(folder)
# DISABLED:             if not config_valid:
# DISABLED:                 logger.error(f"Configuration validation failed: {config_errors}")
# DISABLED:                 return False

            # Validate optional files if they exist
# DISABLED:             strategy_valid, strategy_errors = self._validate_strategy_file(folder)
# DISABLED:             if not strategy_valid:
# DISABLED:                 logger.error(f"Strategy validation failed: {strategy_errors}")
# DISABLED:                 return False

# DISABLED:             cost_valid, cost_errors = self._validate_cost_model_file(folder)
# DISABLED:             if not cost_valid:
# DISABLED:                 logger.error(f"Cost model validation failed: {cost_errors}")
# DISABLED:                 return False

# DISABLED:             metrics_valid, metrics_errors = self._validate_metrics_file(folder)
# DISABLED:             if not metrics_valid:
# DISABLED:                 logger.error(f"Metrics validation failed: {metrics_errors}")
# DISABLED:                 return False

            # Validate cross-file consistency
# DISABLED:             consistency_valid, consistency_errors = self._validate_file_consistency(folder)
# DISABLED:             if not consistency_valid:
# DISABLED:                 logger.error(f"Consistency validation failed: {consistency_errors}")
# DISABLED:                 return False

# DISABLED:             return True

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Job folder validation error: {e}")
# DISABLED:             return False

# DISABLED:     def _validate_required_files(self, folder: Path) -> bool:
        """Validate that required files exist"""
# DISABLED:         required_files = ['config.yaml']

# DISABLED:         for required_file in required_files:
# DISABLED:             file_path = folder / required_file
# DISABLED:             if not file_path.exists():
# DISABLED:                 logger.error(f"Required file missing: {file_path}")
# DISABLED:                 return False

# DISABLED:             if not file_path.is_file():
# DISABLED:                 logger.error(f"Required path is not a file: {file_path}")
# DISABLED:                 return False

# DISABLED:         return True

# DISABLED:     def _validate_config_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate main configuration file"""
# DISABLED:         errors = []
# DISABLED:         config_file = folder / 'config.yaml'

# DISABLED:         try:
# DISABLED:             with open(config_file, 'r') as f:
# DISABLED:                 config = yaml.safe_load(f)

# DISABLED:             if not config:
# DISABLED:                 errors.append("Configuration file is empty")
# DISABLED:                 return False, errors

            # Check required fields
# DISABLED:             for field in self.required_config_fields:
# DISABLED:                 if field not in config:
# DISABLED:                     errors.append(f"Missing required field: {field}")

            # Validate name
# DISABLED:             if 'name' in config:
# DISABLED:                 name = str(config['name'])
# DISABLED:                 if not re.match(r'^[a-zA-Z0-9_-]+$', name):
# DISABLED:                     errors.append("Job name contains invalid characters")
# DISABLED:                 if len(name) > 50:
# DISABLED:                     errors.append("Job name too long (max 50 characters)")

            # Validate description
# DISABLED:             if 'description' in config:
# DISABLED:                 if len(str(config['description'])) > 500:
# DISABLED:                     errors.append("Description too long (max 500 characters)")

# DISABLED:             return len(errors) == 0, errors

# DISABLED:         except yaml.YAMLError as e:
# DISABLED:             errors.append(f"YAML parsing error: {e}")
# DISABLED:             return False, errors
# DISABLED:         except Exception as e:
# DISABLED:             errors.append(f"Configuration file error: {e}")
# DISABLED:             return False, errors

# DISABLED:     def _validate_strategy_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate strategy configuration file"""
# DISABLED:         errors = []
# DISABLED:         strategy_file = folder / 'strategy.yaml'

# DISABLED:         if not strategy_file.exists():
# DISABLED:             return True, errors  # Optional file

# DISABLED:         try:
# DISABLED:             with open(strategy_file, 'r') as f:
# DISABLED:                 strategy = yaml.safe_load(f)

# DISABLED:             if not strategy:
# DISABLED:                 errors.append("Strategy file is empty")
# DISABLED:                 return False, errors

            # Validate strategy name
# DISABLED:             if 'strategy' in strategy:
# DISABLED:                 strategy_name = strategy['strategy']
# DISABLED:                 if strategy_name not in self.valid_strategies:
# DISABLED:                     errors.append(f"Invalid strategy: {strategy_name}")

            # Validate strategy parameters
# DISABLED:             if 'parameters' in strategy:
# DISABLED:                 params = strategy['parameters']
# DISABLED:                 if not isinstance(params, dict):
# DISABLED:                     errors.append("Strategy parameters must be a dictionary")

                # Validate common parameters based on strategy
# DISABLED:                 strategy_name = strategy.get('strategy', '')
# DISABLED:                 if strategy_name == 'genetic':
# DISABLED:                     genetic_params = ['population_size', 'generations', 'mutation_rate', 'crossover_rate']
# DISABLED:                     for param in genetic_params:
# DISABLED:                         if param in params and not isinstance(params[param], (int, float)):
# DISABLED:                             errors.append(f"Invalid parameter type for {param}")

# DISABLED:                 elif strategy_name == 'simulated_annealing':
# DISABLED:                     sa_params = ['initial_temperature', 'cooling_rate', 'min_temperature']
# DISABLED:                     for param in sa_params:
# DISABLED:                         if param in params and not isinstance(params[param], (int, float)):
# DISABLED:                             errors.append(f"Invalid parameter type for {param}")

# DISABLED:             return len(errors) == 0, errors

# DISABLED:         except yaml.YAMLError as e:
# DISABLED:             errors.append(f"Strategy YAML parsing error: {e}")
# DISABLED:             return False, errors
# DISABLED:         except Exception as e:
# DISABLED:             errors.append(f"Strategy file error: {e}")
# DISABLED:             return False, errors

# DISABLED:     def _validate_cost_model_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate cost model configuration file"""
# DISABLED:         errors = []
# DISABLED:         cost_file = folder / 'cost_model.yaml'

# DISABLED:         if not cost_file.exists():
# DISABLED:             return True, errors  # Optional file

# DISABLED:         try:
# DISABLED:             with open(cost_file, 'r') as f:
# DISABLED:                 cost_model = yaml.safe_load(f)

# DISABLED:             if not cost_model:
# DISABLED:                 errors.append("Cost model file is empty")
# DISABLED:                 return False, errors

            # Validate cost model type
# DISABLED:             if 'type' in cost_model:
# DISABLED:                 cost_type = cost_model['type']
# DISABLED:                 if cost_type not in self.valid_cost_models:
# DISABLED:                     errors.append(f"Invalid cost model type: {cost_type}")

            # Validate cost parameters
# DISABLED:             if 'parameters' in cost_model:
# DISABLED:                 params = cost_model['parameters']
# DISABLED:                 if not isinstance(params, dict):
# DISABLED:                     errors.append("Cost model parameters must be a dictionary")

                # Validate parameter values are numeric
# DISABLED:                 for key, value in params.items():
# DISABLED:                     if not isinstance(value, (int, float)):
# DISABLED:                         errors.append(f"Cost parameter {key} must be numeric")

# DISABLED:             return len(errors) == 0, errors

# DISABLED:         except yaml.YAMLError as e:
# DISABLED:             errors.append(f"Cost model YAML parsing error: {e}")
# DISABLED:             return False, errors
# DISABLED:         except Exception as e:
# DISABLED:             errors.append(f"Cost model file error: {e}")
# DISABLED:             return False, errors

# DISABLED:     def _validate_metrics_file(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate metrics configuration file"""
# DISABLED:         errors = []
# DISABLED:         metrics_file = folder / 'metrics.yaml'

# DISABLED:         if not metrics_file.exists():
# DISABLED:             return True, errors  # Optional file

# DISABLED:         try:
# DISABLED:             with open(metrics_file, 'r') as f:
# DISABLED:                 metrics = yaml.safe_load(f)

# DISABLED:             if not metrics:
# DISABLED:                 errors.append("Metrics file is empty")
# DISABLED:                 return False, errors

            # Validate metrics list
# DISABLED:             if 'metrics' in metrics:
# DISABLED:                 metrics_list = metrics['metrics']
# DISABLED:                 if not isinstance(metrics_list, list):
# DISABLED:                     errors.append("Metrics must be a list")
# DISABLED:                 else:
# DISABLED:                     for metric in metrics_list:
# DISABLED:                         if metric not in self.valid_metrics:
# DISABLED:                             errors.append(f"Invalid metric: {metric}")

            # Validate target metrics
# DISABLED:             if 'target_metrics' in metrics:
# DISABLED:                 target_metrics = metrics['target_metrics']
# DISABLED:                 if not isinstance(target_metrics, dict):
# DISABLED:                     errors.append("Target metrics must be a dictionary")
# DISABLED:                 else:
# DISABLED:                     for metric, target in target_metrics.items():
# DISABLED:                         if metric not in self.valid_metrics:
# DISABLED:                             errors.append(f"Invalid target metric: {metric}")
# DISABLED:                         if target not in ['min', 'max']:
# DISABLED:                             errors.append(f"Invalid target direction for {metric}: {target}")

# DISABLED:             return len(errors) == 0, errors

# DISABLED:         except yaml.YAMLError as e:
# DISABLED:             errors.append(f"Metrics YAML parsing error: {e}")
# DISABLED:             return False, errors
# DISABLED:         except Exception as e:
# DISABLED:             errors.append(f"Metrics file error: {e}")
# DISABLED:             return False, errors

# DISABLED:     def _validate_file_consistency(self, folder: Path) -> Tuple[bool, List[str]]:
        """Validate consistency between configuration files"""
# DISABLED:         errors = []

# DISABLED:         try:
            # Load all configuration files
# DISABLED:             config = self._load_yaml_safe(folder / 'config.yaml')
# DISABLED:             strategy = self._load_yaml_safe(folder / 'strategy.yaml')
# DISABLED:             cost_model = self._load_yaml_safe(folder / 'cost_model.yaml')
# DISABLED:             metrics = self._load_yaml_safe(folder / 'metrics.yaml')

            # Check strategy referenced in config exists
# DISABLED:             if strategy and 'strategy' in config and 'strategy' in strategy:
# DISABLED:                 if config.get('strategy') != strategy.get('strategy'):
# DISABLED:                     errors.append("Strategy mismatch between config and strategy files")

            # Validate resource limits are reasonable
# DISABLED:             if 'resource_limits' in config:
# DISABLED:                 limits = config['resource_limits']
# DISABLED:                 if 'max_memory_mb' in limits:
# DISABLED:                     if not isinstance(limits['max_memory_mb'], int) or limits['max_memory_mb'] <= 0:
# DISABLED:                         errors.append("Invalid max_memory_mb value")
# DISABLED:                 if 'max_execution_time' in limits:
# DISABLED:                     if not isinstance(limits['max_execution_time'], (int, float)) or limits['max_execution_time'] <= 0:
# DISABLED:                         errors.append("Invalid max_execution_time value")

# DISABLED:             return len(errors) == 0, errors

# DISABLED:         except Exception as e:
# DISABLED:             errors.append(f"Consistency validation error: {e}")
# DISABLED:             return False, errors

# DISABLED:     def _load_yaml_safe(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Safely load YAML file"""
# DISABLED:         try:
# DISABLED:             if file_path.exists():
# DISABLED:                 with open(file_path, 'r') as f:
# DISABLED:                     return yaml.safe_load(f)
# DISABLED:             return None
# DISABLED:         except Exception:
# DISABLED:             return None

# DISABLED:     def estimate_resources(self, folder_path: str) -> Dict[str, Any]:
        """
# DISABLED:         Estimate resource requirements for a job

# DISABLED:         Args:
# DISABLED:             folder_path: Path to job folder

# DISABLED:         Returns:
# DISABLED:             Dict with resource estimates
        """
# DISABLED:         try:
# DISABLED:             folder = Path(folder_path)

            # Load configuration
# DISABLED:             config = self._load_yaml_safe(folder / 'config.yaml')
# DISABLED:             strategy = self._load_yaml_safe(folder / 'strategy.yaml')
# DISABLED:             cost_model = self._load_yaml_safe(folder / 'cost_model.yaml')

            # Base estimates
# DISABLED:             estimates = {
# DISABLED:                 'estimated_memory_mb': 512,
# DISABLED:                 'estimated_execution_time': 300,  # 5 minutes
# DISABLED:                 'estimated_cpu_cores': 2,
# DISABLED:                 'estimated_disk_space_mb': 100
# DISABLED:             }

            # Adjust based on strategy
# DISABLED:             if strategy:
# DISABLED:                 strategy_name = strategy.get('strategy', '')
# DISABLED:                 if strategy_name == 'genetic':
# DISABLED:                     estimates['estimated_cpu_cores'] = 4
# DISABLED:                     estimates['estimated_execution_time'] *= 2
# DISABLED:                     estimates['estimated_memory_mb'] *= 1.5
# DISABLED:                 elif strategy_name == 'simulated_annealing':
# DISABLED:                     estimates['estimated_execution_time'] *= 1.5

            # Adjust based on resource limits in config
# DISABLED:             if config and 'resource_limits' in config:
# DISABLED:                 limits = config['resource_limits']
# DISABLED:                 if 'max_memory_mb' in limits:
# DISABLED:                     estimates['estimated_memory_mb'] = min(estimates['estimated_memory_mb'], limits['max_memory_mb'])

# DISABLED:             return estimates

# DISABLED:         except Exception as e:
# DISABLED:             logger.error(f"Error estimating resources: {e}")
# DISABLED:             return {
# DISABLED:                 'estimated_memory_mb': 512,
# DISABLED:                 'estimated_execution_time': 300,
# DISABLED:                 'estimated_cpu_cores': 2,
# DISABLED:                 'estimated_disk_space_mb': 100
# DISABLED:             }

# DISABLED:     def get_validation_summary(self, folder_path: str) -> Dict[str, Any]:
        """
# DISABLED:         Get detailed validation summary for a job folder

# DISABLED:         Args:
# DISABLED:             folder_path: Path to job folder

# DISABLED:         Returns:
# DISABLED:             Dict with validation results
        """
# DISABLED:         folder = Path(folder_path)

# DISABLED:         summary = {
# DISABLED:             'valid': False,
# DISABLED:             'folder_exists': folder.exists() and folder.is_dir(),
# DISABLED:             'required_files': {},
# DISABLED:             'optional_files': {},
# DISABLED:             'errors': [],
# DISABLED:             'warnings': [],
# DISABLED:             'resource_estimates': {}
# DISABLED:         }

# DISABLED:         if not summary['folder_exists']:
# DISABLED:             summary['errors'].append("Job folder does not exist")
# DISABLED:             return summary

        # Check file existence
# DISABLED:         required_files = ['config.yaml']
# DISABLED:         optional_files = ['strategy.yaml', 'cost_model.yaml', 'metrics.yaml', 'queue_settings.yaml']

# DISABLED:         for file_name in required_files:
# DISABLED:             file_path = folder / file_name
# DISABLED:             summary['required_files'][file_name] = file_path.exists()

# DISABLED:         for file_name in optional_files:
# DISABLED:             file_path = folder / file_name
# DISABLED:             summary['optional_files'][file_name] = file_path.exists()

        # Validate configuration
# DISABLED:         config_valid, config_errors = self._validate_config_file(folder)
# DISABLED:         summary['errors'].extend(config_errors)

        # Validate strategy if exists
# DISABLED:         strategy_file = folder / 'strategy.yaml'
# DISABLED:         if strategy_file.exists():
# DISABLED:             strategy_valid, strategy_errors = self._validate_strategy_file(folder)
# DISABLED:             summary['errors'].extend(strategy_errors)

        # Get resource estimates
# DISABLED:         if all(summary['required_files'].values()):
# DISABLED:             summary['resource_estimates'] = self.estimate_resources(folder_path)

# DISABLED:         summary['valid'] = len(summary['errors']) == 0 and all(summary['required_files'].values())

# DISABLED:         return summary