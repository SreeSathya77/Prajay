import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser = playwright_instance.chromium.launch(headless=False)  # Set headless=False to see browser action
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def browser_backup():
    """Set up and return the Playwright browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

def login_to_app(page, username, password):
    """Helper function to log into the application."""
    page.goto("https://example.com/login")
    page.fill("input[name='username']", username)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
