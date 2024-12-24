import pytest
from playwright.sync_api import expect
from .pages.login_page import LoginPage

def test_successful_login(page):
    login_page = LoginPage(page)
    page.goto("/login")
    login_page.login("testuser", "password123")
    expect(page).to_have_url("/dashboard")