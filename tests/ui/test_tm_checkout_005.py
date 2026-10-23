from core.ui.pages.catalog_page import CatalogPage
from core.ui.pages.product_card_page import ProductCardPage
from core.ui.pages.cart_page import CartPage
from core.ui.pages.my_orders_page import MyOrdersPage

def test_tm_checkout_005(browser, base_url):

    catalog_page = CatalogPage(browser)
    product_card_page = ProductCardPage(browser)
    cart_page = CartPage(browser)
    my_orders_page = MyOrdersPage(browser)

    item_name = "Термопляшка «Щодня»"
    item_price = "500,00 грн"
    discount_price = "0,00 грн"
    delivery_price = "80,00 грн"
    total_price = "580,00 грн"

    customer_name = "Олександр Тестовий"
    email = "test@example.test"
    delivery_address = "Київ, вул. Тестова, 12"

    browser.navigate_to(base_url)

    # Передумова: Знайти товар та додати його до кошика
    catalog_page.search_for_item(item_name)
    catalog_page.assert_that_length_of_catalog_items_is(1)
    catalog_page.catalog_items[1].assert_that_title_equal_to(item_name)
    catalog_page.catalog_items[1].assert_that_price_equal_to(item_price)

    catalog_page.catalog_items[1].click()
    product_card_page.assert_that_product_title_is(item_name)
    product_card_page.assert_that_product_price_is(item_price)

    product_card_page.add_product_to_cart()
    product_card_page.close_product_card()
    catalog_page.store_header.assert_that_cart_counter_equal_to(1)

    catalog_page.store_header.open_cart()
    cart_page.assert_that_number_of_cart_items_is(1)
    
    cart_page.enter_customer_name(customer_name)
    cart_page.enter_email(email)
    cart_page.enter_deliver_address(delivery_address)
    cart_page.select_declined_payment_result()
    cart_page.click_on_place_order_button()
    cart_page.assert_that_payment_error_message_is_visible()

    cart_page.select_approved_payment_result()
    cart_page.click_on_place_order_button()

    my_orders_page.assert_orders_count_is(1)
    my_orders_page.orders[1].assert_status_is_approved()
    my_orders_page.orders[1].assert_order_total_is(total_price)
    my_orders_page.store_header.assert_that_cart_counter_equal_to(0)

    my_orders_page.orders[1].click_on_cancel_order_button()
    my_orders_page.orders[1].assert_status_is_cancelled()

    browser.reload()
    my_orders_page.assert_orders_count_is(1)
    my_orders_page.orders[1].assert_status_is_cancelled()
    my_orders_page.orders[1].assert_order_total_is(total_price)