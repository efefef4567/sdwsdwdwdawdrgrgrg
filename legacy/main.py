#!/usr/bin/env python3
"""
Binary Structure Exploration Engine (BSEE)

A CLI tool for analyzing binary files by applying reversible transformations
to optimize user-specified metrics.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import logging
import os

# Ensure project root is in Python path for BSEE imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Verify project root is correctly set
if not (project_root / "bsee" / "__init__.py").exists():
    print(f"Warning: BSEE module not found at {project_root}/bsee")
    print("Make sure you're running from the correct directory")

# Additional fix for virtual environment compatibility
if "VIRTUAL_ENV" in os.environ:
    venv_site_packages = Path(os.environ["VIRTUAL_ENV"]) / "Lib" / "site-packages"
    if str(venv_site_packages) not in sys.path:
        sys.path.insert(0, str(venv_site_packages))

from bsee.engine.pipeline import Pipeline
from bsee.utils.logger import setup_logging
from gui.main_window import MainWindow


def parse_arguments():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Binary Structure Exploration Engine - Analyze and transform binary files"
    )

    # Mode selection
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Launch batch processing GUI mode"
    )

    parser.add_argument(
        "--batch-daemon",
        action="store_true",
        help="Run batch processing in daemon mode (no GUI)"
    )

    # Original arguments for single file analysis
    parser.add_argument(
        "input_file",
        nargs="?",
        type=str,
        help="Binary file to analyze"
    )

    parser.add_argument(
        "--policy",
        type=str,
        default="config/policies/policy_ideality.yaml",
        help="Policy YAML file (default: config/policies/policy_ideality.yaml)"
    )

    parser.add_argument(
        "--costs",
        type=str,
        default="config/costs/cost_default.yaml",
        help="Cost YAML file (default: config/costs/cost_default.yaml)"
    )

    parser.add_argument(
        "--strategy",
        type=str,
        default="greedy",
        choices=["greedy", "beam", "annealing", "mcts", "genetic", "heuristic"],
        help="Search strategy (default: greedy)"
    )

    parser.add_argument(
        "--metrics",
        type=str,
        default="file_ideality_score,entropy_global,lz77_ratio",
        help="Comma-separated list of metrics or 'all' (default: file_ideality_score,entropy_global,lz77_ratio)"
    )

    parser.add_argument(
        "--target-metrics",
        type=str,
        default="file_ideality_score=max,entropy_global=min",
        help="Target metrics with optimization direction (default: file_ideality_score=max,entropy_global=min)"
    )

    parser.add_argument(
        "--max-operations",
        type=int,
        default=1000,
        help="Maximum number of operations (default: 1000)"
    )

    parser.add_argument(
        "--max-cost",
        type=float,
        default=10000,
        help="Maximum total cost (default: 10000)"
    )

    parser.add_argument(
        "--allowed-ops",
        type=str,
        help="Comma-separated list of allowed operations (optional)"
    )

    parser.add_argument(
        "--operation-limit",
        type=int,
        help="Maximum number of different operation types to use"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="results",
        help="Output directory for results (default: results)"
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="BSEE 1.0.0"
    )

    return parser.parse_args()


def validate_arguments(args):
    """Validate CLI arguments."""

    # If batch mode, skip most validation
    if args.batch or args.batch_daemon:
        return

    # Check if input file exists
    if not args.input_file:
        print("Error: Input file is required for analysis mode", file=sys.stderr)
        print("Use --batch to launch batch processing GUI mode", file=sys.stderr)
        sys.exit(1)

    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' does not exist", file=sys.stderr)
        sys.exit(1)

    if not input_path.is_file():
        print(f"Error: '{args.input_file}' is not a file", file=sys.stderr)
        sys.exit(1)

    # Check if configuration files exist
    policy_path = Path(args.policy)
    if not policy_path.exists():
        print(f"Error: Policy file '{args.policy}' does not exist", file=sys.stderr)
        sys.exit(1)

    costs_path = Path(args.costs)
    if not costs_path.exists():
        print(f"Error: Costs file '{args.costs}' does not exist", file=sys.stderr)
        sys.exit(1)

    # Validate numeric arguments
    if args.max_operations <= 0:
        print("Error: --max-operations must be positive", file=sys.stderr)
        sys.exit(1)

    if args.max_cost <= 0:
        print("Error: --max-cost must be positive", file=sys.stderr)
        sys.exit(1)

    if args.operation_limit is not None and args.operation_limit <= 0:
        print("Error: --operation-limit must be positive", file=sys.stderr)
        sys.exit(1)


def run_single_file_analysis(args):
    """Run single file analysis mode."""
    logger = logging.getLogger(__name__)

    try:
        logger.info(f"Starting BSEE analysis of '{args.input_file}'")
        logger.info(f"Using strategy: {args.strategy}")
        logger.info(f"Policy: {args.policy}")
        logger.info(f"Costs: {args.costs}")

        # Create and run pipeline
        pipeline = Pipeline(args)
        results = pipeline.run()

        if results.success:
            logger.info("Analysis completed successfully")
            logger.info(f"Results saved to: {results.output_directory}")
            logger.info(f"Final score: {results.final_score:.2f}")
            logger.info(f"Total operations: {results.total_operations}")
            logger.info(f"Total cost: {results.total_cost:.2f}")
        else:
            logger.error("Analysis failed")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


def run_batch_gui():
    """Launch batch processing GUI mode."""
    logger = logging.getLogger(__name__)

    try:
        logger.info("Launching BSEE Batch Processing GUI")

        # Import and create batch window
        from gui.batch_window import BatchWindow
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()  # Hide main window

        # Create batch window
        batch_window = BatchWindow(root)

        # Start the GUI
        root.mainloop()

    except KeyboardInterrupt:
        logger.info("Batch GUI interrupted by user")
    except Exception as e:
        logger.error(f"Error launching batch GUI: {e}")
        sys.exit(1)


def run_batch_daemon():
    """Run batch processing in daemon mode (no GUI)."""
    logger = logging.getLogger(__name__)

    try:
        logger.info("Starting BSEE Batch Processing Daemon")

        # BSEE modules are working
        from bsee.batch import JobManager

        job_manager = JobManager()
        job_manager.start_folder_monitoring()
        job_manager.set_auto_start(True)

        logger.info("Batch daemon started with auto-folder monitoring")
        logger.info("Press Ctrl+C to stop")

        try:
            while True:
                import time
                time.sleep(10)  # Check every 10 seconds

                # Log status periodically
                stats = job_manager.get_statistics()
                if stats['total_jobs'] > 0:
                    logger.info(f"Daemon status: {stats['running_jobs']} running, {stats['queue_length']} queued")

        except KeyboardInterrupt:
            logger.info("Batch daemon interrupted by user")
        finally:
            job_manager.shutdown()
            logger.info("Batch daemon stopped")

    except Exception as e:
        logger.error(f"Error running batch daemon: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    args = parse_arguments()
    validate_arguments(args)

    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)

    # Route to appropriate mode
    if args.batch:
        run_batch_gui()
    elif args.batch_daemon:
        run_batch_daemon()
    else:
        run_single_file_analysis(args)


if __name__ == "__main__":
    main()