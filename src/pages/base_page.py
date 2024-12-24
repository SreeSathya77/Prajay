from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        
    async def wait_for_load(self):
        await self.page.wait_for_load_state('networkidle')