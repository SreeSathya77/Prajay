import pytest
from playwright.sync_api import Page, expect
from typing import Dict
import os
from dotenv import load_dotenv
from src.utils.logger import logger
from src.utils.email_reporter import EmailReporter
from src.utils.test_results_collector import TestResultsCollector, TestCase
from src.utils.environment import is_running_in_docker
from datetime import datetime
import time

load_dotenv()


def pytest_configure(config):
    """Setup test configuration"""
    logger.info("Starting test execution")
    TestResultsCollector().reset()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collect test results during execution"""
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call':
        test_case = TestCase(
            name=item.name,
            nodeid=item.nodeid,
            duration=result.duration,
            outcome=result.outcome,
            timestamp=datetime.now().isoformat(),
            error=str(result.longrepr) if hasattr(result, 'longrepr') and result.longrepr else None
        )
        TestResultsCollector().add_test_result(test_case)


def pytest_sessionfinish(session, exitstatus):
    """Send email report after all tests have completed (only in Docker)"""
    # Wait for any pending test operations to complete
    time.sleep(2)

    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)

    # Wait for report files to be generated
    time.sleep(2)

    # Get final test results
    results = TestResultsCollector().finalize_results()

    if is_running_in_docker():
        # Initialize email reporter
        email_reporter = EmailReporter()

        # Collect report files
        report_files = []
        for report_file in ['reports/report.html', 'reports/test-results.json']:
            if os.path.exists(report_file):
                report_files.append(report_file)

        # Send email report with complete results
        email_reporter.send_report(
            results=results,
            report_files=report_files
        )
    else:
        logger.info("Skipping email report - not running in Docker")

    logger.info(f"Test execution completed with exit status: {exitstatus}")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    logger.debug("Setting up browser context arguments")
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        }
    }


@pytest.fixture(scope="function")
def page(browser):
    logger.debug("Creating new browser page")
    context = browser.new_context()
    page = context.new_page()
    yield page
    logger.debug("Closing browser context")
    context.close()