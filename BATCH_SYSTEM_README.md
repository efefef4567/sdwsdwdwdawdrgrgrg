# BSEE Batch Processing System

A comprehensive batch processing system for the Binary Structure Exploration Engine (BSEE) that enables automated job management, resource monitoring, and performance analytics.

## Overview

The batch processing system provides:
- **Automated job discovery and management**
- **Real-time resource monitoring**
- **Comprehensive GUI with job panels**
- **Enhanced CLI interface**
- **Performance analytics and profiling**
- **Pipeline validation and health checking**
- **Error handling and recovery**
- **Multiple job templates**

## Quick Start

### GUI Access

1. **Launch from Main GUI**: Open Tools → Batch Processing (Ctrl+B)
2. **Launch via CLI**: `python legacy/main.py --batch`
3. **Launch Daemon Mode**: `python legacy/main.py --batch-daemon`

### Create Your First Batch Job

1. Create a folder in `batch_jobs/` directory
2. Add required configuration files:
   - `config.yaml` (required)
   - `strategy.yaml` (optional)
   - `cost_model.yaml` (optional)
   - `metrics.yaml` (optional)

3. The system will auto-discover and queue your job

## Directory Structure

```
├── batch_jobs/                    # Root for all batch jobs
│   ├── Job_001_test_analysis/     # Individual job folder
│   │   ├── config.yaml           # Main job configuration
│   │   ├── strategy.yaml         # Strategy configuration
│   │   ├── cost_model.yaml       # Cost model parameters
│   │   ├── metrics.yaml          # Metrics configuration
│   │   ├── queue_settings.yaml   # Scheduling settings
│   │   └── resource_limits.yaml  # Resource constraints
│   └── Job_002_neural_optimization/
├── results/                       # Job results (auto-created)
│   ├── Job_001_test_analysis/
│   └── Job_002_neural_optimization/
└── logs/
    └── batch_operations.log       # Batch operation logs
```

## Configuration Files

### config.yaml (Required)
Main job configuration:
```yaml
name: "Job Name"
description: "Job description"
strategy: "greedy"
max_operations: 1000
max_cost: 10000
```

### strategy.yaml (Optional)
Search strategy configuration:
```yaml
strategy: "genetic"
parameters:
  population_size: 50
  generations: 100
  mutation_rate: 0.1
```

### metrics.yaml (Optional)
Metrics and optimization targets:
```yaml
metrics:
  - "file_ideality_score"
  - "entropy_global"
  - "compression_ratio"

target_metrics:
  "file_ideality_score": "max"
  "entropy_global": "min"
```

## Job Templates

Pre-configured templates are available in `config/presets/batch_templates/`:

- **neural_analysis.yaml** - Neural network optimization
- **performance_optimization.yaml** - Fast and efficient analysis
- **research_batch.yaml** - Comprehensive research analysis
- **custom_strategy.yaml** - Template for custom strategies

Use templates via CLI:
```bash
python legacy/main.py batch create my_job --template neural_analysis
```

## CLI Commands

### Job Management
```bash
# List all jobs
python legacy/main.py batch list

# Start a job
python legacy/main.py batch start <job_id>

# Pause a job
python legacy/main.py batch pause <job_id>

# Queue a job for specific time
python legacy/main.py batch queue <job_id> --time 14:30

# Show job status
python legacy/main.py batch status <job_id>

# Show job logs
python legacy/main.py batch logs <job_id>

# Open results folder
python legacy/main.py batch results <job_id>
```

### System Configuration
```bash
# Configure batch system
python legacy/main.py batch config --max-jobs 4

# Create new job from template
python legacy/main.py batch create my_job --template neural_analysis

# Monitor system resources
python legacy/main.py batch monitor
```

## GUI Features

### Main Window Layout

1. **Left Panel - Job List**
   - All jobs with status, progress, and resource usage
   - Individual play/pause/queue controls
   - Auto-start checkbox
   - Filter by status

2. **Center Panel - Job Details**
   - Selected job information
   - Analytics dropdown panels
   - Resource usage meters
   - Action buttons (Results, History, Binary Viewer)
   - Real-time logs

3. **Right Panel - System Resources**
   - Overall system resource usage
   - Job queue summary
   - System limits and configuration
   - "Add New Jobs" button

### Key Features

- **Auto-Discovery**: Jobs automatically detected when folders are added
- **Real-time Updates**: 2-second refresh interval (configurable)
- **Resource Monitoring**: CPU, memory, and thread usage per job
- **Analytics**: Performance metrics, bottlenecks, and trends
- **Job Control**: Start, pause, queue, and cancel operations
- **Results Access**: Direct access to job results and history

## Analytics and Performance

### Available Analytics

- **Performance Metrics**: Execution time, resource usage, efficiency
- **Resource Trends**: CPU and memory usage over time
- **Job Statistics**: Success rates, failure analysis, common errors
- **Bottleneck Detection**: Identify slow functions and operations
- **Historical Comparison**: Compare performance between jobs

### Performance Profiling

- **Function-Level Timing**: Detailed timing for all functions
- **Memory Profiling**: Track memory usage and leaks
- **Thread Activity**: Monitor thread utilization
- **Performance Events**: Track important performance milestones

## Error Handling

### Error Categories

- **Configuration**: Invalid job configurations
- **Resource**: Memory, disk, or CPU issues
- **Execution**: Runtime errors during analysis
- **I/O**: File access and permission issues
- **Validation**: Input validation failures
- **System**: Operating system or environment errors

### Recovery Mechanisms

- **Automatic Retry**: Configurable retry attempts with exponential backoff
- **Error Isolation**: Failed jobs don't affect other jobs
- **Auto-Recovery**: Automatic fixes for common issues
- **Error Reporting**: Detailed error logging and statistics

## System Integration

### Integration Points

- **Main Window GUI**: Tools → Batch Processing menu
- **App Controller**: Batch-specific settings and directories
- **Parallel Processor**: Batch-aware resource management
- **Logger**: Dedicated batch operation logging

### Settings

Batch settings are stored in `gui_settings.json`:
```json
{
  "batch_auto_start": false,
  "batch_max_concurrent": 4,
  "batch_refresh_interval": 2000,
  "batch_default_template": "neural_analysis"
}
```

## Monitoring and Maintenance

### Log Files

- **Main Log**: `logs/batch_operations.log`
- **Error Log**: Integrated with error handling system
- **Performance Log**: Detailed performance metrics

### Performance Tuning

- **Resource Limits**: Configure per-job memory and time limits
- **Concurrency**: Adjust maximum concurrent jobs
- **Monitoring**: Real-time resource usage tracking
- **Analytics**: Export performance data for analysis

## Best Practices

### Job Configuration

1. **Use Templates**: Start with existing templates when possible
2. **Set Realistic Limits**: Configure appropriate resource constraints
3. **Monitor Progress**: Use the GUI to track job execution
4. **Review Logs**: Check logs for errors and performance issues

### Performance Optimization

1. **Batch Similar Jobs**: Group similar analysis tasks together
2. **Resource Management**: Monitor system resources during execution
3. **Error Recovery**: Configure appropriate retry strategies
4. **Regular Cleanup**: Clean up old jobs and logs periodically

### Troubleshooting

1. **Check Job Status**: Use GUI or CLI to verify job status
2. **Review Configuration**: Validate YAML configuration files
3. **Monitor Resources**: Check system resource availability
4. **Examine Logs**: Review batch operation logs for errors

## Advanced Features

### Pipeline Validation

- **Configuration Validation**: Validate job configurations before execution
- **Health Monitoring**: Real-time pipeline health checking
- **Performance Prediction**: Estimate resource requirements and execution time
- **Optimization Suggestions**: Get recommendations for job improvement

### Custom Extensions

- **Custom Strategies**: Implement your own search strategies
- **Custom Metrics**: Add domain-specific metrics
- **Custom Templates**: Create job templates for specific use cases
- **Integration Hooks**: Extend system functionality with custom handlers

## API Reference

### Core Classes

- **JobManager**: Central job management and orchestration
- **Job**: Individual job representation and execution
- **FolderMonitor**: Automatic job discovery from file system
- **JobValidator**: Configuration validation and health checking

### Analytics Classes

- **AnalyticsCollector**: Performance data collection
- **PipelineValidator**: Pipeline validation and health monitoring
- **PerformanceProfiler**: Detailed performance profiling

### Error Handling

- **ErrorHandler**: Centralized error handling and recovery
- **ErrorContext**: Context manager for error handling
- **BatchError**: Error representation with metadata

## Configuration Reference

### Global Configuration (config/batch_config.yaml)

System-wide settings for resource limits, logging, validation, and performance optimization.

### Job Configuration

Per-job configuration files for strategy, cost model, metrics, and resource limits.

## Support and Contributing

For issues, questions, or contributions:
1. Check existing documentation and logs
2. Review configuration files for errors
3. Use the GUI monitoring tools
4. Export analytics data for debugging
5. Report issues with detailed error information

## Version History

- **v1.0.0**: Initial implementation with full batch processing capabilities
- **v1.1.0**: Enhanced analytics and performance profiling
- **v1.2.0**: Advanced pipeline validation and error handling

---

*This batch processing system provides enterprise-grade job management capabilities while maintaining the flexibility and power of the BSEE analysis engine.*