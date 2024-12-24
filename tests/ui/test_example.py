import pytest
from playwright.sync_api import expect

def test_homepage(page, smart_locator):
    page.goto("/")
    title_locator = smart_locator.find_element("h1")
    expect(title_locator).to_be_visible()
    expect(page).to_have_title("Example Domain")