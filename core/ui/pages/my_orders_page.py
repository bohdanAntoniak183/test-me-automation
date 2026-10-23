from core.ui.web_element import WebElement
from core.ui.web_elements_list import WebElementsList
from core.ui.elements.store_header import StoreHeader
from core.ui.elements.my_orders_page_elements.order_item import OrderItem

class MyOrdersPage:
    def __init__(self, browser):
        self.driver = browser.driver

        self.store_header = StoreHeader(browser)

        self.orders = WebElementsList(
            browser=browser,
            locator="//div[@id='orders-list']//article[@data-testid='order-card']",
            description="Список замовлень",
            element_class=OrderItem
        )

    def assert_orders_count_is(self, orders_count):
        self.orders.assert_that_length_is_equal_to(orders_count)