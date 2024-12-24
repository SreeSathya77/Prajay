import pytest
from playwright.sync_api import Page
from src.utils.config import config
from src.utils.api_client import APIClient
from src.utils.ai_healing import SmartLocator

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.fixture(scope="function")
def smart_locator(page):
    return SmartLocator(page)

@pytest.fixture(scope="function")
def context_config(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "base_url": config.base_url,
        "timeout": config.timeout
    }