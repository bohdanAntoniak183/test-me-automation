from core.ui.web_element import WebElement
from core.ui.web_elements_list import WebElementsList
from core.ui.elements.cart_page_elements.cart_item import CartItem

class CartPage:
    def __init__(self, browser):
        self.driver = browser.driver

        self.__cart = WebElement(
            browser=browser,
            locator="//dialog[@id='bag-dialog']",
            description="Сторінка кошика"
        )

        self.cart_items = WebElementsList(
            browser=browser,
            locator="//div[@id='bag-items']//div[@data-cart-line]",
            description = "Список товарів у кошику",
            element_class = CartItem,
            parent=self.__cart
        )

        self.coupon_input = WebElement(
            browser=browser,
            locator="//input[@id='coupon']",
            description="Поле для промокоду",
            parent=self.__cart
        )

        self.apply_coupon_button = WebElement(
            browser=browser,
            locator="//button[@id='apply-coupon']",
            description="Кнопка для промокоду 'Застосувати'",
            parent=self.__cart
        )

        self.delivery_dropdown = WebElement(
            browser=browser,
            locator="//select[@id='delivery']",
            description="Обрання типу доставки",
            parent=self.__cart
        )

        self.__totals = WebElement(
            browser=browser,
            locator="//div[@id='totals']",
            description="Область опису ціни товарів, знижки, ціни доставки",
            parent=self.__cart
        )

        self.items_price = WebElement(
            browser=browser,
            locator="//span[normalize-space(text())='Товари']/following-sibling::span",
            description="Ціна всіх товарів",
            parent=self.__totals
        )

        self.discount_price = WebElement(
            browser=browser,
            locator="//span[normalize-space(text())='Знижка']/following-sibling::span",
            description="Сума знижки",
            parent=self.__totals
        )

        self.delivery_price = WebElement(
            browser=browser,
            locator="//span[normalize-space(text())='Доставка']/following-sibling::span",
            description="Сума доставки",
            parent=self.__totals
        )

        self.total_price = WebElement(
            browser=browser,
            locator="//div[@data-testid='cart-total']//span[normalize-space(text())='Разом']/following-sibling::span",
            description="Сума разом",
            parent=self.__totals
        )

        self.customer_name_input = WebElement(
            browser=browser,
            locator="//input[@id='customer-name']",
            description="Поле для ім'я та прізвища клієнта",
            parent=self.__cart
        )

        self.email_input = WebElement(
            browser=browser,
            locator="//input[@id='email']",
            description="Поле для електронної пошти клієнта",
            parent=self.__cart
        )

        self.delivery_address_input = WebElement(
            browser=browser,
            locator="//input[@id='address']",
            description="Поле для адреси доставки",
            parent=self.__cart
        )

        self.payment_result_dropdown = WebElement(
            browser=browser,
            locator="//select[@id='payment']",
            description="Обрання результату оплати",
            parent=self.__cart
        )

        self.place_order_button = WebElement(
            browser=browser,
            locator="//button[@data-testid='place-order']",
            description="Кнопка 'Оформити замовлення'",
            parent=self.__cart
        )

    def enter_coupon(self, coupon_name):
        self.coupon_input.enter_value(coupon_name)
        self.apply_coupon_button.click()

    def select_standard_delivery_option(self):
        self.delivery_dropdown.select_option_by_value("standard")

    def enter_customer_name(self, customer_name):
        self.customer_name_input.enter_value(customer_name)

    def enter_email(self, email):
        self.email_input.enter_value(email)

    def enter_deliver_address(self, address):
        self.delivery_address_input.enter_value(address)

    def select_approved_payment_result(self):
        self.payment_result_dropdown.select_option_by_value("approved")

    def click_on_place_order_button(self):
        self.place_order_button.click()

    def assert_that_number_of_cart_items_is(self, count):
        self.cart_items.assert_that_length_is_equal_to(count)

    def assert_that_items_price_is(self, price):
        self.items_price.assert_text(price)

    def assert_that_discount_is(self, discount):
        self.discount_price.assert_text(f"−{discount}")

    def assert_that_delivery_price_is(self, delivery_price):
        self.delivery_price.assert_text(delivery_price)

    def assert_that_total_is(self, total):
        self.total_price.assert_text(total)
