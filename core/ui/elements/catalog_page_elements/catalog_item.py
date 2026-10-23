from core.ui.web_element import WebElement

class CatalogItem(WebElement):
    def __init__(self, browser, locator, description):
        super().__init__(browser=browser, locator=locator, description=description)
        
        self.title_button = WebElement(
            browser=browser,
            locator="//button[contains(@class, 'product-title')]",
            description=f"Назва товару",
            parent=self
        )
        
        self.price = WebElement(
            browser=browser,
            locator="//*[contains(@class, 'price')]",
            description=f"Ціна товару",
            parent=self
        )

    def click(self):
        self.title_button.click()

    def assert_that_title_equal_to(self, value):
        self.title_button.assert_text(value)

    def assert_that_price_equal_to(self, value):
        self.price.assert_text(value)