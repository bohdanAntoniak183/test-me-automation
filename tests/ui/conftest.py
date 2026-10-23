import pytest

from core.ui.browser import Browser

@pytest.fixture(scope="function")
def browser(headless):
    browser_instance = Browser(headless)
    yield browser_instance
    browser_instance.terminate()