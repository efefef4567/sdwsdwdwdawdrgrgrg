"""
Batch Processing Test Runner
Runs all batch processing tests and generates a report
"""

import unittest
import sys
import time
import traceback
from pathlib import Path
import io

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class BatchTestResult:
    """Container for test results"""
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.errors = []
        self.failures = []
        self.start_time = None
        self.end_time = None
        self.execution_time = 0.0


class BatchTestRunner:
    """Test runner for batch processing tests"""

    def __init__(self):
        self.test_modules = [
            'test_job_creation',
            'test_job_manager',
            'test_folder_monitor',
            'test_batch_integration'
        ]
        self.result = BatchTestResult()

    def run_all_tests(self, verbose=True):
        """Run all batch processing tests"""
        print("=" * 60)
        print("BSEE Batch Processing Test Suite")
        print("=" * 60)

        self.result.start_time = time.time()

        # Create test suite
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        # Load test modules
        for module_name in self.test_modules:
            try:
                module = __import__(module_name)
                suite.addTests(loader.loadTestsFromModule(module))
                print(f"✓ Loaded {module_name}")
            except Exception as e:
                print(f"✗ Failed to load {module_name}: {e}")
                self.result.errors.append(f"Module loading error in {module_name}: {e}")

        # Run tests
        if verbose:
            runner = unittest.TextTestRunner(
                verbosity=2,
                stream=sys.stdout,
                buffer=True
            )
        else:
            # Capture output for summary
            stream = io.StringIO()
            runner = unittest.TextTestRunner(
                verbosity=1,
                stream=stream,
                buffer=True
            )

        print(f"\nRunning {suite.countTestCases()} tests...")
        print("-" * 60)

        # Execute tests
        test_result = runner.run(suite)

        self.result.end_time = time.time()
        self.result.execution_time = self.result.end_time - self.result.start_time

        # Collect results
        self.result.total_tests = test_result.testsRun
        self.result.passed_tests = test_result.testsRun - len(test_result.failures) - len(test_result.errors)
        self.result.failed_tests = len(test_result.failures) + len(test_result.errors)

        # Store error details
        for test, traceback_str in test_result.failures:
            self.result.failures.append(f"FAIL: {test}")
            self.result.failures.append(traceback_str)

        for test, traceback_str in test_result.errors:
            self.result.errors.append(f"ERROR: {test}")
            self.result.errors.append(traceback_str)

        return self.result

    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)

        print(f"Total Tests:     {self.result.total_tests}")
        print(f"Passed:          {self.result.passed_tests}")
        print(f"Failed:          {self.result.failed_tests}")
        print(f"Success Rate:    {(self.result.passed_tests / max(1, self.result.total_tests) * 100):.1f}%")
        print(f"Execution Time:  {self.result.execution_time:.2f}s")

        if self.result.passed_tests == self.result.total_tests:
            print("\n🎉 ALL TESTS PASSED!")
        else:
            print(f"\n⚠️  {self.result.failed_tests} TEST(S) FAILED")

        # Show errors and failures
        if self.result.errors or self.result.failures:
            print("\n" + "=" * 60)
            print("FAILED TEST DETAILS")
            print("=" * 60)

            if self.result.errors:
                print("\nERRORS:")
                for error in self.result.errors[:5]:  # Limit to first 5 errors
                    print(f"  {error}")

            if self.result.failures:
                print("\nFAILURES:")
                for failure in self.result.failures[:5]:  # Limit to first 5 failures
                    print(f"  {failure}")

        return self.result

    def run_specific_test(self, test_name):
        """Run a specific test module"""
        print(f"Running specific test: {test_name}")

        try:
            module = __import__(test_name)
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)

            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)

            return {
                'tests_run': result.testsRun,
                'passed': result.testsRun - len(result.failures) - len(result.errors),
                'failed': len(result.failures) + len(result.errors),
                'success': result.wasSuccessful()
            }

        except Exception as e:
            print(f"Error running {test_name}: {e}")
            return {
                'tests_run': 0,
                'passed': 0,
                'failed': 1,
                'success': False,
                'error': str(e)
            }


def main():
    """Main test runner entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="BSEE Batch Processing Test Runner")
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--test', '-t',
        help='Run specific test module (e.g., test_job_creation)'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available test modules'
    )

    args = parser.parse_args()

    runner = BatchTestRunner()

    if args.list:
        print("Available test modules:")
        for module in runner.test_modules:
            print(f"  - {module}")
        return

    if args.test:
        if args.test in runner.test_modules:
            result = runner.run_specific_test(args.test)
            if result['success']:
                print(f"✓ {args.test} passed ({result['passed']}/{result['tests_run']})")
                sys.exit(0)
            else:
                print(f"✗ {args.test} failed ({result['failed']}/{result['tests_run']})")
                sys.exit(1)
        else:
            print(f"Unknown test module: {args.test}")
            print("Available modules:")
            for module in runner.test_modules:
                print(f"  - {module}")
            sys.exit(1)

    # Run all tests
    result = runner.run_all_tests(verbose=args.verbose)
    runner.generate_report()

    # Exit with appropriate code
    sys.exit(0 if result.passed_tests == result.total_tests else 1)


if __name__ == '__main__':
    main()