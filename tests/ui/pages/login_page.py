from playwright.sync_api import Page, expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        
    async def login(self, username: str, password: str):
        await self.username_input.fill(username)
        await self.password_input.fill(password)
        await self.login_button.click()
        await self.page.wait_for_load_state('networkidle')