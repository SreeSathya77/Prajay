# QMaasTestLab AI-Powered Test Automation Framework

A comprehensive test automation framework featuring:
- UI Testing with Playwright
- API Testing
- Performance Testing
- Self-healing Tests
- Advanced HTML Reports
- AI-powered Test Analysis

## Setup

1. Install Python 3.9+
2. Install dependencies:
   ```bash
   pip install poetry
   poetry install
   ```
3. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Running Tests

- UI Tests: `pytest tests/ui`
- API Tests: `pytest tests/api`
- Performance Tests: `locust -f tests/performance/test_performance.py`
- All Tests: `pytest`

Reports are generated in the `reports` directory.