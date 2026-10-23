from core.ui.web_element import WebElement

class ProductCardPage:
    def __init__(self, browser):
        self.driver = browser.driver

        self.__product_card = WebElement(
            browser=browser,
            locator="//dialog[@id='product-dialog']",
            description="Сторінка окремого продукту"
        )

        self.product_title = WebElement(
            browser=browser,
            locator="//*[@id='detail-title']",
            description="Назва продукту",
            parent=self.__product_card
        )

        self.product_price = WebElement(
            browser=browser,
            locator="//strong[contains(@class, 'detail-price')]",
            description="Ціна продукту",
            parent=self.__product_card
        )

        self.add_to_cart_button = WebElement(
            browser=browser,
            locator="//button[normalize-space(text())='До кошика']",
            description="Кнопка 'До кошика'",
            parent=self.__product_card
        )

        self.close_product_card_button = WebElement(
            browser=browser,
            locator="//button[@data-close='product-dialog']",
            description="Кнопка закриття картки товару",
            parent=self.__product_card
        )

    def add_product_to_cart(self):
        self.add_to_cart_button.click()

    def close_product_card(self):
        self.close_product_card_button.click()

    def assert_that_product_title_is(self, product_title):
        self.product_title.assert_text(product_title)

    def assert_that_product_price_is(self, product_price):
        self.product_price.assert_text(product_price)