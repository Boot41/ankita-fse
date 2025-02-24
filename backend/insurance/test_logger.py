import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional

class TestLogger:
    """Logger for tracking test case execution."""
    
    def __init__(self, log_dir: str = 'test_logs'):
        """Initialize the test logger.
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Create a new log file for each test run
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(log_dir, f'test_run_{timestamp}.log')
        
        # Configure logging
        self.logger = logging.getLogger('test_logger')
        self.logger.setLevel(logging.INFO)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Initialize counters
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.error_tests = 0
        self.skipped_tests = 0
        
        self.logger.info("Test execution started")
        
    def log_test_start(self, test_name: str) -> None:
        """Log the start of a test case."""
        self.logger.info(f"Starting test: {test_name}")
        self.total_tests += 1
        
    def log_test_result(
        self,
        test_name: str,
        result: str,
        execution_time: float,
        error: Optional[str] = None,
        extra_data: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log the result of a test case.
        
        Args:
            test_name: Name of the test case
            result: Test result (PASS/FAIL/ERROR/SKIP)
            execution_time: Time taken to execute the test
            error: Error message if test failed/errored
            extra_data: Additional test data to log
        """
        if result == 'PASS':
            self.passed_tests += 1
            level = logging.INFO
        elif result == 'FAIL':
            self.failed_tests += 1
            level = logging.ERROR
        elif result == 'ERROR':
            self.error_tests += 1
            level = logging.ERROR
        else:  # SKIP
            self.skipped_tests += 1
            level = logging.WARNING
            
        message = f"Test: {test_name} - Result: {result} - Time: {execution_time:.3f}s"
        if error:
            message += f"\nError: {error}"
        if extra_data:
            message += f"\nAdditional Data: {extra_data}"
            
        self.logger.log(level, message)
        
    def log_summary(self) -> None:
        """Log the summary of all test executions."""
        summary = f"""
Test Execution Summary:
----------------------
Total Tests: {self.total_tests}
Passed: {self.passed_tests}
Failed: {self.failed_tests}
Errors: {self.error_tests}
Skipped: {self.skipped_tests}
Success Rate: {(self.passed_tests / self.total_tests * 100):.2f}%
----------------------"""
        self.logger.info(summary)
