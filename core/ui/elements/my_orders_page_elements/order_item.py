from core.ui.web_element import WebElement

class OrderItem(WebElement):
    def __init__(self, browser, locator, description):
        super().__init__(browser=browser, locator=locator, description=description)

        self.status = WebElement(
            browser=browser,
            locator="//header//span[@class='status-pill']",
            description="Статус замовлення",
            parent=self
        )

        self.order_total = WebElement(
            browser=browser,
            locator="//header/following-sibling::p[1]",
            description="Сума замовлення разом",
            parent=self
        )

        self.__details = WebElement(
            browser=browser,
            locator="//details",
            description="Опис замовлення",
            parent=self
        )

        self.details_button = WebElement(
            browser=browser,
            locator="//summary",
            description="Кнопка відкриття/закриття опису замовлення",
            parent=self.__details
        )

        self.order_id = WebElement(
            browser=browser,
            locator="//p[@class='order-id']",
            description="Кнопка відкриття/закриття опису замовлення",
            parent=self.__details
        )

        self.price_summary = WebElement(
            browser=browser,
            locator="//p[last()]",
            description="Опис суми замовлення разом",
            parent=self.__details
        )

    def get_order_id(self):
        return self.order_id.get_text()

    def click_on_details_button(self):
        self.details_button.click()

    def assert_status_is_approved(self):
        self.status.assert_text("Підтверджено")

    def assert_order_id_is(self, order_id):
        self.order_id.assert_text(order_id)

    def assert_order_total_is(self, order_total):
        self.order_total.assert_text_contains(order_total)

    def assert_price_summary(self, items_price, discount_price, delivery_price):
        self.price_summary.assert_text(f"Товари: {items_price} · Знижка: {discount_price} · Доставка: {delivery_price}")