"""
Pipeline Validator Implementation
Pipeline validation and health checking for batch jobs.
"""

import time
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import yaml
from pathlib import Path

from ...utils.logger import get_logger

logger = get_logger(__name__)


class ValidationStatus(Enum):
    """Validation status levels"""
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class ValidationResult:
    """Result of a validation check"""
    check_name: str
    status: ValidationStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


@dataclass
class PipelineHealth:
    """Overall pipeline health status"""
    overall_status: ValidationStatus
    validation_results: List[ValidationResult]
    recommendations: List[str]
    health_score: float  # 0-100
    timestamp: float


class PipelineValidator:
    """Validates pipeline configuration and monitors pipeline health"""

    def __init__(self):
        """Initialize pipeline validator"""
        self.validation_rules = self._load_validation_rules()
        self.health_history: List[PipelineHealth] = []
        self.max_history_size = 100

    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules configuration"""
        return {
            'strategy_validation': {
                'required_fields': ['strategy'],
                'valid_strategies': [
                    'greedy', 'random', 'genetic', 'simulated_annealing',
                    'hill_climbing', 'beam_search', 'depth_first', 'breadth_first'
                ],
                'parameter_limits': {
                    'genetic': {
                        'population_size': {'min': 10, 'max': 1000},
                        'generations': {'min': 10, 'max': 1000},
                        'mutation_rate': {'min': 0.0, 'max': 1.0},
                        'crossover_rate': {'min': 0.0, 'max': 1.0}
                    },
                    'simulated_annealing': {
                        'initial_temperature': {'min': 0.1, 'max': 1000.0},
                        'cooling_rate': {'min': 0.1, 'max': 0.99},
                        'min_temperature': {'min': 0.001, 'max': 1.0}
                    }
                }
            },
            'cost_model_validation': {
                'required_fields': ['type'],
                'valid_types': ['linear', 'exponential', 'logarithmic', 'custom'],
                'parameter_limits': {
                    'linear': {
                        'cost_per_operation': {'min': 0.0, 'max': 1000.0}
                    },
                    'exponential': {
                        'base': {'min': 1.01, 'max': 10.0},
                        'multiplier': {'min': 0.1, 'max': 100.0}
                    }
                }
            },
            'metrics_validation': {
                'valid_metrics': [
                    'file_ideality_score', 'entropy_global', 'entropy_local',
                    'lz77_ratio', 'bzip2_ratio', 'gzip_ratio', 'compression_ratio',
                    'pattern_density', 'repetitiveness', 'complexity_score'
                ],
                'target_validation': {
                    'valid_directions': ['min', 'max'],
                    'max_metrics_count': 10
                }
            },
            'resource_validation': {
                'max_memory_mb': 16384,  # 16GB
                'max_execution_time_minutes': 480,  # 8 hours
                'max_concurrent_jobs': 16
            },
            'performance_validation': {
                'min_operations_per_second': 0.1,
                'max_memory_leak_threshold': 100.0,  # MB
                'max_error_rate': 0.1  # 10%
            }
        }

    def validate_job_configuration(self, job_folder: str) -> List[ValidationResult]:
        """
        Validate complete job configuration

        Args:
            job_folder: Path to job configuration folder

        Returns:
            List of validation results
        """
        results = []

        try:
            folder = Path(job_folder)

            # Validate configuration files exist
            results.extend(self._validate_required_files(folder))

            # Load and validate configuration
            config = self._load_yaml_safe(folder / 'config.yaml')
            if config:
                results.extend(self._validate_main_config(config, folder))

                # Validate strategy
                strategy = self._load_yaml_safe(folder / 'strategy.yaml')
                if strategy:
                    results.extend(self._validate_strategy_config(strategy))

                # Validate cost model
                cost_model = self._load_yaml_safe(folder / 'cost_model.yaml')
                if cost_model:
                    results.extend(self._validate_cost_model_config(cost_model))

                # Validate metrics
                metrics = self._load_yaml_safe(folder / 'metrics.yaml')
                if metrics:
                    results.extend(self._validate_metrics_config(metrics))

                # Validate resource limits
                results.extend(self._validate_resource_limits(config))

            else:
                results.append(ValidationResult(
                    "config_loading",
                    ValidationStatus.FAILED,
                    "Failed to load main configuration file"
                ))

        except Exception as e:
            results.append(ValidationResult(
                "configuration_validation",
                ValidationStatus.FAILED,
                f"Configuration validation failed: {str(e)}"
            ))

        return results

    def _validate_required_files(self, folder: Path) -> List[ValidationResult]:
        """Validate required configuration files exist"""
        results = []
        required_files = ['config.yaml']

        for file_name in required_files:
            file_path = folder / file_name
            if not file_path.exists():
                results.append(ValidationResult(
                    f"required_file_{file_name}",
                    ValidationStatus.FAILED,
                    f"Required file missing: {file_name}"
                ))
            else:
                results.append(ValidationResult(
                    f"required_file_{file_name}",
                    ValidationStatus.PASSED,
                    f"Required file present: {file_name}"
                ))

        return results

    def _validate_main_config(self, config: Dict[str, Any], folder: Path) -> List[ValidationResult]:
        """Validate main configuration file"""
        results = []
        rules = self.validation_rules

        # Validate required fields
        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in config:
                results.append(ValidationResult(
                    f"config_field_{field}",
                    ValidationStatus.WARNING,
                    f"Optional field missing: {field}"
                ))

        # Validate job name
        if 'name' in config:
            name = config['name']
            if not isinstance(name, str) or len(name.strip()) == 0:
                results.append(ValidationResult(
                    "job_name",
                    ValidationStatus.FAILED,
                    "Job name must be a non-empty string"
                ))
            elif len(name) > 50:
                results.append(ValidationResult(
                    "job_name",
                    ValidationStatus.WARNING,
                    "Job name is very long (>50 characters)"
                ))
            else:
                results.append(ValidationResult(
                    "job_name",
                    ValidationStatus.PASSED,
                    "Job name is valid"
                ))

        # Validate max operations
        if 'max_operations' in config:
            max_ops = config['max_operations']
            if not isinstance(max_ops, int) or max_ops <= 0:
                results.append(ValidationResult(
                    "max_operations",
                    ValidationStatus.FAILED,
                    "max_operations must be a positive integer"
                ))
            elif max_ops > 100000:
                results.append(ValidationResult(
                    "max_operations",
                    ValidationStatus.WARNING,
                    "max_operations is very large (>100,000)"
                ))
            else:
                results.append(ValidationResult(
                    "max_operations",
                    ValidationStatus.PASSED,
                    "max_operations is reasonable"
                ))

        # Validate max cost
        if 'max_cost' in config:
            max_cost = config['max_cost']
            if not isinstance(max_cost, (int, float)) or max_cost <= 0:
                results.append(ValidationResult(
                    "max_cost",
                    ValidationStatus.FAILED,
                    "max_cost must be a positive number"
                ))
            else:
                results.append(ValidationResult(
                    "max_cost",
                    ValidationStatus.PASSED,
                    "max_cost is valid"
                ))

        return results

    def _validate_strategy_config(self, strategy: Dict[str, Any]) -> List[ValidationResult]:
        """Validate strategy configuration"""
        results = []
        rules = self.validation_rules['strategy_validation']

        # Check required fields
        if 'strategy' not in strategy:
            results.append(ValidationResult(
                "strategy_field",
                ValidationStatus.FAILED,
                "Strategy field is required"
            ))
            return results

        strategy_name = strategy['strategy']
        if strategy_name not in rules['valid_strategies']:
            results.append(ValidationResult(
                "strategy_name",
                ValidationStatus.FAILED,
                f"Invalid strategy: {strategy_name}. Valid options: {rules['valid_strategies']}"
            ))
        else:
            results.append(ValidationResult(
                "strategy_name",
                ValidationStatus.PASSED,
                f"Valid strategy: {strategy_name}"
            ))

        # Validate parameters
        if strategy_name in rules['parameter_limits'] and 'parameters' in strategy:
            params = strategy['parameters']
            param_rules = rules['parameter_limits'][strategy_name]

            for param_name, param_value in params.items():
                if param_name in param_rules:
                    limits = param_rules[param_name]
                    if 'min' in limits and param_value < limits['min']:
                        results.append(ValidationResult(
                            f"strategy_parameter_{param_name}",
                            ValidationStatus.WARNING,
                            f"Parameter {param_name} below recommended minimum: {limits['min']}"
                        ))
                    elif 'max' in limits and param_value > limits['max']:
                        results.append(ValidationResult(
                            f"strategy_parameter_{param_name}",
                            ValidationStatus.WARNING,
                            f"Parameter {param_name} above recommended maximum: {limits['max']}"
                        ))
                    else:
                        results.append(ValidationResult(
                            f"strategy_parameter_{param_name}",
                            ValidationStatus.PASSED,
                            f"Parameter {param_name} is within recommended range"
                        ))

        return results

    def _validate_cost_model_config(self, cost_model: Dict[str, Any]) -> List[ValidationResult]:
        """Validate cost model configuration"""
        results = []
        rules = self.validation_rules['cost_model_validation']

        # Check required fields
        if 'type' not in cost_model:
            results.append(ValidationResult(
                "cost_model_type",
                ValidationStatus.FAILED,
                "Cost model type is required"
            ))
            return results

        cost_type = cost_model['type']
        if cost_type not in rules['valid_types']:
            results.append(ValidationResult(
                "cost_model_type",
                ValidationStatus.WARNING,
                f"Unknown cost model type: {cost_type}"
            ))
        else:
            results.append(ValidationResult(
                "cost_model_type",
                ValidationStatus.PASSED,
                f"Valid cost model type: {cost_type}"
            ))

        # Validate parameters
        if cost_type in rules['parameter_limits'] and 'parameters' in cost_model:
            params = cost_model['parameters']
            param_rules = rules['parameter_limits'][cost_type]

            for param_name, param_value in params.items():
                if param_name in param_rules:
                    limits = param_rules[param_name]
                    if 'min' in limits and param_value < limits['min']:
                        results.append(ValidationResult(
                            f"cost_parameter_{param_name}",
                            ValidationStatus.WARNING,
                            f"Cost parameter {param_name} below recommended minimum: {limits['min']}"
                        ))
                    elif 'max' in limits and param_value > limits['max']:
                        results.append(ValidationResult(
                            f"cost_parameter_{param_name}",
                            ValidationStatus.FAILED,
                            f"Cost parameter {param_name} exceeds maximum: {limits['max']}"
                        ))
                    else:
                        results.append(ValidationResult(
                            f"cost_parameter_{param_name}",
                            ValidationStatus.PASSED,
                            f"Cost parameter {param_name} is valid"
                        ))

        return results

    def _validate_metrics_config(self, metrics: Dict[str, Any]) -> List[ValidationResult]:
        """Validate metrics configuration"""
        results = []
        rules = self.validation_rules['metrics_validation']

        # Validate metrics list
        if 'metrics' in metrics:
            metrics_list = metrics['metrics']
            if not isinstance(metrics_list, list):
                results.append(ValidationResult(
                    "metrics_list",
                    ValidationStatus.FAILED,
                    "Metrics must be a list"
                ))
            elif len(metrics_list) > rules['target_validation']['max_metrics_count']:
                results.append(ValidationResult(
                    "metrics_list",
                    ValidationStatus.WARNING,
                    f"Too many metrics ({len(metrics_list)}). Maximum recommended: {rules['target_validation']['max_metrics_count']}"
                ))
            else:
                for metric in metrics_list:
                    if metric not in rules['valid_metrics']:
                        results.append(ValidationResult(
                            f"metric_{metric}",
                            ValidationStatus.WARNING,
                            f"Unknown metric: {metric}"
                        ))
                    else:
                        results.append(ValidationResult(
                            f"metric_{metric}",
                            ValidationStatus.PASSED,
                            f"Valid metric: {metric}"
                        ))

        # Validate target metrics
        if 'target_metrics' in metrics:
            target_metrics = metrics['target_metrics']
            if not isinstance(target_metrics, dict):
                results.append(ValidationResult(
                    "target_metrics",
                    ValidationStatus.FAILED,
                    "Target metrics must be a dictionary"
                ))
            else:
                for metric, direction in target_metrics.items():
                    if metric not in rules['valid_metrics']:
                        results.append(ValidationResult(
                            f"target_metric_{metric}",
                            ValidationStatus.WARNING,
                            f"Unknown target metric: {metric}"
                        ))
                    elif direction not in rules['target_validation']['valid_directions']:
                        results.append(ValidationResult(
                            f"target_direction_{metric}",
                            ValidationStatus.FAILED,
                            f"Invalid direction for {metric}: {direction}. Valid: {rules['target_validation']['valid_directions']}"
                        ))
                    else:
                        results.append(ValidationResult(
                            f"target_metric_{metric}",
                            ValidationStatus.PASSED,
                            f"Valid target metric: {metric} = {direction}"
                        ))

        return results

    def _validate_resource_limits(self, config: Dict[str, Any]) -> List[ValidationResult]:
        """Validate resource limits"""
        results = []
        rules = self.validation_rules['resource_validation']

        if 'resource_limits' in config:
            limits = config['resource_limits']

            # Validate memory limit
            if 'max_memory_mb' in limits:
                memory_limit = limits['max_memory_mb']
                if memory_limit > rules['max_memory_mb']:
                    results.append(ValidationResult(
                        "memory_limit",
                        ValidationStatus.WARNING,
                        f"Memory limit ({memory_limit}MB) exceeds recommended maximum ({rules['max_memory_mb']}MB)"
                    ))
                else:
                    results.append(ValidationResult(
                        "memory_limit",
                        ValidationStatus.PASSED,
                        f"Memory limit is reasonable: {memory_limit}MB"
                    ))

            # Validate execution time limit
            if 'max_execution_time' in limits:
                time_limit = limits['max_execution_time']
                if time_limit > rules['max_execution_time_minutes']:
                    results.append(ValidationResult(
                        "execution_time_limit",
                        ValidationStatus.WARNING,
                        f"Execution time limit ({time_limit}min) exceeds recommended maximum ({rules['max_execution_time_minutes']}min)"
                    ))
                else:
                    results.append(ValidationResult(
                        "execution_time_limit",
                        ValidationStatus.PASSED,
                        f"Execution time limit is reasonable: {time_limit}min"
                    ))

        return results

    def monitor_pipeline_health(self, job_performance_data: Dict[str, Any]) -> PipelineHealth:
        """
        Monitor pipeline health based on performance data

        Args:
            job_performance_data: Performance data from running jobs

        Returns:
            PipelineHealth object with current status
        """
        validation_results = []
        recommendations = []

        # Performance validation
        if 'execution_time' in job_performance_data:
            exec_time = job_performance_data['execution_time']
            if exec_time > 3600:  # > 1 hour
                validation_results.append(ValidationResult(
                    "execution_time",
                    ValidationStatus.WARNING,
                    f"Long execution time: {exec_time:.1f}s",
                    {'execution_time': exec_time}
                ))
                recommendations.append("Consider breaking down large jobs into smaller tasks")

        # Resource usage validation
        if 'resource_analysis' in job_performance_data:
            resource_analysis = job_performance_data['resource_analysis']

            if 'memory' in resource_analysis:
                memory_stats = resource_analysis['memory']
                if memory_stats.get('max', 0) > 8000:  # > 8GB
                    validation_results.append(ValidationResult(
                        "memory_usage",
                        ValidationStatus.WARNING,
                        f"High memory usage: {memory_stats['max']:.1f}MB",
                        memory_stats
                    ))
                    recommendations.append("Monitor for memory leaks or optimize memory usage")

            if 'cpu' in resource_analysis:
                cpu_stats = resource_analysis['cpu']
                if cpu_stats.get('mean', 0) < 10:  # < 10% CPU
                    validation_results.append(ValidationResult(
                        "cpu_usage",
                        ValidationStatus.WARNING,
                        f"Low CPU utilization: {cpu_stats['mean']:.1f}%",
                        cpu_stats
                    ))
                    recommendations.append("Consider increasing parallelism or optimizing algorithm")

        # Error validation
        error_count = job_performance_data.get('error_count', 0)
        if error_count > 0:
            validation_results.append(ValidationResult(
                "error_rate",
                ValidationStatus.FAILED if error_count > 5 else ValidationStatus.WARNING,
                f"Job encountered {error_count} errors",
                {'error_count': error_count}
            ))
            recommendations.append("Review job configuration and input data")

        # Calculate overall health score
        health_score = self._calculate_health_score(validation_results)

        # Determine overall status
        overall_status = ValidationStatus.PASSED
        if any(r.status == ValidationStatus.FAILED for r in validation_results):
            overall_status = ValidationStatus.FAILED
        elif any(r.status == ValidationStatus.WARNING for r in validation_results):
            overall_status = ValidationStatus.WARNING

        # Add some default recommendations if none were generated
        if not recommendations:
            if overall_status == ValidationStatus.PASSED:
                recommendations.append("Pipeline is performing well")
            elif overall_status == ValidationStatus.WARNING:
                recommendations.append("Monitor performance and consider optimization")

        health = PipelineHealth(
            overall_status=overall_status,
            validation_results=validation_results,
            recommendations=recommendations,
            health_score=health_score,
            timestamp=time.time()
        )

        # Store in history
        self.health_history.append(health)
        if len(self.health_history) > self.max_history_size:
            self.health_history.pop(0)

        return health

    def _calculate_health_score(self, validation_results: List[ValidationResult]) -> float:
        """Calculate overall health score (0-100)"""
        if not validation_results:
            return 100.0

        # Weight scores
        passed_weight = 1.0
        warning_weight = 0.7
        failed_weight = 0.2

        total_weight = 0
        total_score = 0

        for result in validation_results:
            if result.status == ValidationStatus.PASSED:
                weight = passed_weight
                score = 100
            elif result.status == ValidationStatus.WARNING:
                weight = warning_weight
                score = 60
            elif result.status == ValidationStatus.FAILED:
                weight = failed_weight
                score = 20
            else:
                continue  # Skip unknown status

            total_weight += weight
            total_score += score * weight

        if total_weight == 0:
            return 100.0

        return total_score / total_weight

    def _load_yaml_safe(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Safely load YAML file"""
        try:
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return yaml.safe_load(f)
            return None
        except Exception as e:
            logger.error(f"Error loading YAML file {file_path}: {e}")
            return None

    def get_optimization_suggestions(self, validation_results: List[ValidationResult]) -> List[str]:
        """Get optimization suggestions based on validation results"""
        suggestions = []

        for result in validation_results:
            if result.status in [ValidationStatus.WARNING, ValidationStatus.FAILED]:
                if "memory" in result.check_name.lower():
                    suggestions.append("Consider reducing memory usage through streaming or chunked processing")
                elif "cpu" in result.check_name.lower():
                    suggestions.append("Optimize algorithms or increase parallelism for better CPU utilization")
                elif "execution_time" in result.check_name.lower():
                    suggestions.append("Break down large jobs or optimize time-consuming operations")
                elif "error" in result.check_name.lower():
                    suggestions.append("Review job configuration and implement better error handling")

        return list(set(suggestions))  # Remove duplicates

    def generate_validation_report(self, job_folder: str) -> Dict[str, Any]:
        """Generate comprehensive validation report for a job"""
        validation_results = self.validate_job_configuration(job_folder)

        # Categorize results
        passed = [r for r in validation_results if r.status == ValidationStatus.PASSED]
        warnings = [r for r in validation_results if r.status == ValidationStatus.WARNING]
        failures = [r for r in validation_results if r.status == ValidationStatus.FAILED]

        # Calculate overall status
        if failures:
            overall_status = ValidationStatus.FAILED
        elif warnings:
            overall_status = ValidationStatus.WARNING
        else:
            overall_status = ValidationStatus.PASSED

        # Generate recommendations
        recommendations = self.get_optimization_suggestions(validation_results)

        return {
            'job_folder': job_folder,
            'overall_status': overall_status.value,
            'validation_timestamp': time.time(),
            'summary': {
                'total_checks': len(validation_results),
                'passed': len(passed),
                'warnings': len(warnings),
                'failures': len(failures)
            },
            'results': [asdict(result) for result in validation_results],
            'recommendations': recommendations,
            'can_proceed': len(failures) == 0
        }