from typing import List, Dict, Optional
import difflib
from playwright.sync_api import Page, Locator

class SmartLocator:
    def __init__(self, page: Page):
        self.page = page
        self.history: Dict[str, List[str]] = {}
        
    def find_element(self, selector: str) -> Optional[Locator]:
        try:
            return self.page.locator(selector)
        except:
            alternative = self._find_alternative(selector)
            if alternative:
                return self.page.locator(alternative)
        return None
        
    def _find_alternative(self, selector: str) -> Optional[str]:
        if selector not in self.history:
            return None
            
        content = self.page.content()
        matches = difflib.get_close_matches(
            selector,
            self.history[selector],
            n=1,
            cutoff=0.7
        )
        return matches[0] if matches else None
        
    def learn(self, original: str, working: str):
        if original not in self.history:
            self.history[original] = []
        self.history[original].append(working)


class SelfHealing:
    def __init__(self):
        self.locator_history: Dict[str, List[str]] = {}

    def find_alternative_locator(self, original_locator: str, page_source: str) -> str:
        """
        Uses similarity matching to find alternative locators when original fails
        """
        if original_locator not in self.locator_history:
            return None

        alternatives = self.locator_history[original_locator]
        for alt in alternatives:
            if alt in page_source:
                return alt
        return None

    def learn_locator(self, original: str, successful: str):
        """
        Records successful locator alternatives for future use
        """
        if original not in self.locator_history:
            self.locator_history[original] = []
        if successful not in self.locator_history[original]:
            self.locator_history[original].append(successful)