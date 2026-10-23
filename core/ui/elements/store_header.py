from core.ui.web_element import WebElement

# Даний елемент винесений окремо, оскільки він може
# використовуватись у різних місцях веб-аплікації (сторінках).

# Також він не буде винесений для спільного використання у всіх сторінках,
# оскільки деякі сторінки веб-аплікації можуть не мати даного елементу.

# Тому він буде застосовуватись окремо для кожної із сторінок.
class StoreHeader(WebElement):
    def __init__(self, browser):
        super().__init__(browser=browser, locator="//header", description="Шапка сторінки")

        self.cart_button = WebElement(
            browser=browser,
            locator="//button[@id='open-cart']",
            description=f"Кошик",
            parent=self
        )

        self.cart_counter = WebElement(
            browser=browser,
            locator="//*[@id='cart-count']",
            description=f"Лічильник кошика",
            parent=self
        )

    def open_cart(self):
        self.cart_button.click()

    def assert_that_cart_counter_equal_to(self, value):
        self.cart_counter.assert_text(str(value))