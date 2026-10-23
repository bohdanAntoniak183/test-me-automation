from core.ui.pages.catalog_page import CatalogPage
from core.ui.pages.product_card_page import ProductCardPage
from core.ui.pages.cart_page import CartPage

def test_tm_cart_001(browser, base_url):

    catalog_page = CatalogPage(browser)
    product_card_page = ProductCardPage(browser)
    cart_page = CartPage(browser)

    item_name = "Термопляшка «Щодня»"
    item_price = "500,00 грн"

    browser.navigate_to(base_url)

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
    cart_page.cart_items[1].assert_title(item_name)
    cart_page.cart_items[1].assert_price(item_price)
    cart_page.cart_items[1].assert_quantity(1)

    cart_page.cart_items[1].remove_item_from_the_cart()
    cart_page.assert_that_number_of_cart_items_is(0)

    browser.reload()
    catalog_page.store_header.assert_that_cart_counter_equal_to(0)
    catalog_page.store_header.open_cart()
    cart_page.assert_that_number_of_cart_items_is(0)
