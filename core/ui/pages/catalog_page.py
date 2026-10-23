from core.ui.web_element import WebElement
from core.ui.web_elements_list import WebElementsList
from core.ui.elements.store_header import StoreHeader
from core.ui.elements.catalog_page_elements.catalog_item import CatalogItem

class CatalogPage:
    def __init__(self, browser):
        self.driver = browser.driver

        self.store_header = StoreHeader(browser)

        self.search_input = WebElement(
            browser=browser,
            locator="//input[@id='search']",
            description="Поле для пошуку товарів",
        )

        self.catalog_items = WebElementsList(
            browser=browser,
            locator="//div[@id='products']//article[contains(@class, 'product-card')]",
            description = "Список товарів у каталозі",
            element_class = CatalogItem
        )

    def search_for_item(self, item_name):
        self.search_input.clear_value()
        self.search_input.enter_value(item_name)

    def assert_that_length_of_catalog_items_is(self, length_value):
        self.catalog_items.assert_that_length_is_equal_to(length_value)