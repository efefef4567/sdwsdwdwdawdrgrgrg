"""""
# DISABLED: Validation utilities for BSEE configuration and data.
"""""

# DISABLED: import yaml
# DISABLED: from typing import Any, Dict, List


# DISABLED: def validate_config_file(config: Dict[str, Any]) -> None:
    """Validate a configuration dictionary."""""
# DISABLED:     if not isinstance(config, dict):
# DISABLED:         raise ValueError("Configuration must be a dictionary")""

    # Validate required fields based on config type
# DISABLED:     if 'metric_weights' in config:''
# DISABLED:         _validate_metric_weights(config['metric_weights'])''

# DISABLED:     if 'base_costs' in config:''
# DISABLED:         _validate_base_costs(config['base_costs'])''

# DISABLED:     if 'parameters' in config:''
# DISABLED:         _validate_strategy_parameters(config['parameters'])''


# DISABLED: def _validate_metric_weights(metric_weights: Dict[str, float]) -> None:
    """Validate metric weights configuration."""""
# DISABLED:     if not isinstance(metric_weights, dict):
# DISABLED:         raise ValueError("metric_weights must be a dictionary")""

# DISABLED:     for metric_name, weight in metric_weights.items():
# DISABLED:         if not isinstance(metric_name, str):
# DISABLED:             raise ValueError(f"Metric name must be string: {metric_name}")""

# DISABLED:         if not isinstance(weight, (int, float)):
# DISABLED:             raise ValueError(f"Metric weight must be numeric: {metric_name} -> {weight}")""

# DISABLED:         if weight < -1000 or weight > 1000:
# DISABLED:             raise ValueError(f"Metric weight should be between -1000 and 1000: {metric_name} -> {weight}")""


# DISABLED: def _validate_base_costs(base_costs: Dict[str, float]) -> None:
    """Validate base costs configuration."""""
# DISABLED:     if not isinstance(base_costs, dict):
# DISABLED:         raise ValueError("base_costs must be a dictionary")""

# DISABLED:     for operation_name, cost in base_costs.items():
# DISABLED:         if not isinstance(operation_name, str):
# DISABLED:             raise ValueError(f"Operation name must be string: {operation_name}")""

# DISABLED:         if not isinstance(cost, (int, float)):
# DISABLED:             raise ValueError(f"Operation cost must be numeric: {operation_name} -> {cost}")""

# DISABLED:         if cost < 0:
# DISABLED:             raise ValueError(f"Operation cost must be non-negative: {operation_name} -> {cost}")""


# DISABLED: def _validate_strategy_parameters(parameters: Dict[str, Any]) -> None:
    """Validate strategy parameters configuration."""""
# DISABLED:     if not isinstance(parameters, dict):
# DISABLED:         raise ValueError("Strategy parameters must be a dictionary")""

    # Common parameter validations
# DISABLED:     numeric_params = ['restart_threshold', 'random_restart_prob', 'lookahead_depth','''''']''
# DISABLED:                      'beam_width', 'temperature', 'exploration_constant',''
# DISABLED:                      'population_size', 'mutation_rate', 'crossover_rate']''

# DISABLED:     for param_name in numeric_params:
# DISABLED:         if param_name in parameters:
# DISABLED:             value = parameters[param_name]
# DISABLED:             if not isinstance(value, (int, float)):
# DISABLED:                 raise ValueError(f"Parameter {param_name} must be numeric: {value}")""

# DISABLED:             if 'prob' in param_name or 'rate' in param_name:''
# DISABLED:                 if value < 0 or value > 1:
# DISABLED:                     raise ValueError(f"Probability/rate parameter {param_name} must be between 0 and 1: {value}")""
# DISABLED:             else:
# DISABLED:                 if value < 0:
# DISABLED:                     raise ValueError(f"Parameter {param_name} must be non-negative: {value}")""


# DISABLED: def validate_binary_data(binary_data: bytes) -> bool:
    """Validate binary data."""""
# DISABLED:     if not isinstance(binary_data, bytes):
# DISABLED:         raise ValueError("Binary data must be bytes")""

# DISABLED:     if len(binary_data) == 0:
# DISABLED:         raise ValueError("Binary data cannot be empty")""

# DISABLED:     if len(binary_data) > 100 * 1024 * 1024:  # 100MB limit
# DISABLED:         raise ValueError("Binary data too large (max 100MB)")""

# DISABLED:     return True


# DISABLED: def validate_operation_parameters(operation_name: str, params: Dict[str, Any]) -> bool:
    """Validate operation parameters."""""
# DISABLED:     if not isinstance(operation_name, str):
# DISABLED:         raise ValueError("Operation name must be string")""

# DISABLED:     if not isinstance(params, dict):
# DISABLED:         raise ValueError("Operation parameters must be dictionary")""

    # Operation-specific validations would go here
    # For now, just basic type checking
# DISABLED:     return True


# DISABLED: def validate_metrics_list(metrics: List[str]) -> bool:
    """Validate a list of metric names."""""
# DISABLED:     if not isinstance(metrics, list):
# DISABLED:         raise ValueError("Metrics must be a list")""

# DISABLED:     for metric in metrics:
# DISABLED:         if not isinstance(metric, str):
# DISABLED:             raise ValueError(f"Metric name must be string: {metric}")""

# DISABLED:     return True


# DISABLED: def validate_file_path(file_path: str) -> bool:
    """Validate a file path."""""
# DISABLED:     if not isinstance(file_path, str):
# DISABLED:         raise ValueError("File path must be string")""

# DISABLED:     if not file_path.strip():
# DISABLED:         raise ValueError("File path cannot be empty")""

# DISABLED:     return True


# DISABLED: def validate_yaml_syntax(yaml_content: str) -> bool:
    """Validate YAML syntax."""""
# DISABLED:     try:
# DISABLED:         yaml.safe_load(yaml_content)
# DISABLED:         return True
# DISABLED:     except yaml.YAMLError as e:
# DISABLED:         raise ValueError(f"Invalid YAML syntax: {e}")""


# DISABLED: def validate_policy_config(config: Dict[str, Any]) -> None:
    """Validate policy-specific configuration."""""
# DISABLED:     required_fields = ['metric_weights', 'targets']''
# DISABLED:     for field in required_fields:
# DISABLED:         if field not in config:
# DISABLED:             raise ValueError(f"Policy config missing required field: {field}")""

    # Validate targets
# DISABLED:     targets = config['targets']''
# DISABLED:     if not isinstance(targets, dict):
# DISABLED:         raise ValueError("Policy targets must be a dictionary")""

# DISABLED:     for metric_name, target in targets.items():
# DISABLED:         if target not in ['maximize', 'minimize']:''
# DISABLED:             raise ValueError(f"Target must be 'maximize' or 'minimize': {metric_name} -> {target}")""

    # Validate budget if present:
# DISABLED:     if 'budget' in config:''
# DISABLED:         budget = config['budget']''
# DISABLED:         if not isinstance(budget, dict):
# DISABLED:             raise ValueError("Policy budget must be a dictionary")""

# DISABLED:         numeric_budget_fields = ['max_operations', 'max_cost', 'max_time_seconds']''
# DISABLED:         for field in numeric_budget_fields:
# DISABLED:             if field in budget:
# DISABLED:                 if not isinstance(budget[field], (int, float)) or budget[field] <= 0:
# DISABLED:                     raise ValueError(f"Budget field {field} must be positive number")""


# DISABLED: def validate_cost_config(config: Dict[str, Any]) -> None:
    """Validate cost-specific configuration."""""
# DISABLED:     if 'base_costs' not in config:''
# DISABLED:         raise ValueError("Cost config missing required field: base_costs")""

    # Validate cost modifiers if present:
# DISABLED:     if 'cost_modifiers' in config:''
# DISABLED:         modifiers = config['cost_modifiers']''
# DISABLED:         if not isinstance(modifiers, dict):
# DISABLED:             raise ValueError("Cost modifiers must be a dictionary")""

# DISABLED:         modifier_fields = ['frequency_penalty', 'diminishing_return', 'novelty_bonus']''
# DISABLED:         for field in modifier_fields:
# DISABLED:             if field in modifiers:
# DISABLED:                 value = modifiers[field]
# DISABLED:                 if not isinstance(value, (int, float)):
# DISABLED:                     raise ValueError(f"Cost modifier {field} must be numeric: {value}")""


# DISABLED: def validate_strategy_config(config: Dict[str, Any]) -> None:
    """Validate strategy-specific configuration."""""
# DISABLED:     if 'parameters' not in config:''
# DISABLED:         raise ValueError("Strategy config missing required field: parameters")""

    # Strategy-specific parameter validation would go here
    # For now, just validate the basic structure