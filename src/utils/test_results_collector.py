from datetime import datetime
from typing import Dict, List
import threading
from dataclasses import dataclass, asdict
from .logger import logger


@dataclass
class TestCase:
    name: str
    nodeid: str
    duration: float
    outcome: str
    timestamp: str
    error: str = None


class TestResultsCollector:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.reset()

    def reset(self):
        """Reset all test results"""
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'duration': 0,
            'test_cases': []
        }
        self.start_time = datetime.now()

    def add_test_result(self, test_case: TestCase):
        """Add a test result safely using thread lock"""
        with self._lock:
            self.results['total'] += 1
            self.results['test_cases'].append(asdict(test_case))

            if test_case.outcome == 'passed':
                self.results['passed'] += 1
            elif test_case.outcome == 'failed':
                self.results['failed'] += 1
            elif test_case.outcome == 'skipped':
                self.results['skipped'] += 1

    def finalize_results(self) -> Dict:
        """Calculate final results including duration"""
        with self._lock:
            end_time = datetime.now()
            self.results['duration'] = (end_time - self.start_time).total_seconds()
            return self.results.copy()


# Create singleton instance
test_results_collector = TestResultsCollector()