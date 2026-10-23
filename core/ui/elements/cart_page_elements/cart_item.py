from core.ui.web_element import WebElement

class CartItem(WebElement):
    def __init__(self, browser, locator, description):
        super().__init__(browser=browser, locator=locator, description=description)
        
        self.title = WebElement(
            browser=browser,
            locator="//h3",
            description=f"Назва товару",
            parent=self
        )

        self.price = WebElement(
            browser=browser,
            locator="//span[@class='price']",
            description=f"Ціна товару повністю",
            parent=self
        )

        self.quantity = WebElement(
            browser=browser,
            locator="//div[@class='quantity']//span[contains(@data-testid, 'quantity')]",
            description=f"Кількість товару",
            parent=self
        )

    def assert_title(self, value):
        self.title.assert_text(value)

    def assert_price(self, value):
        self.price.assert_text(value)

    def assert_quantity(self, value):
        self.quantity.assert_text(str(value))