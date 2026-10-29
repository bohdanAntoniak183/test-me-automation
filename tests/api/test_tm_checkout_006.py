from http import HTTPStatus

from core.api.services.products_service import ProductsService
from core.api.services.quote_service import QuoteService
from core.api.services.orders_service import OrdersService
from core.api.models.products_service.products_catalog_response import ProductsCatalogResponse
from core.api.models.orders_service.orders_response import OrdersResponse
from core.api.models.quote_service.quote_payload import QuotePayload
from core.api.models.orders_service.orders_payload import OrdersPayload
from core.api.models.cart_item import CartItem
from core.api.models.delivery_type import DeliveryType
from core.api.models.totals import Totals
from core.api.models.orders_service.payment_status import PaymentStatus
from core.api.models.orders_service.order_status import OrderStatus

def test_tm_checkout_006(api_client):

    products_service = ProductsService(api_client)
    quote_service = QuoteService(api_client)
    orders_service = OrdersService(api_client)

    item_name = "Термопляшка «Щодня»"
    item_price = 50000
    discount_price = 5000
    shipping_price = 8000
    total_price = 53000
    coupon_name = "WELCOME10"
    customer_name = "Олександр Тестовий"
    email = "test@example.test"
    delivery_address = "Київ, вул. Тестова, 12"

    products_response = products_service.get_products()
    assert products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу: {products_response.text}"

    parsed_products = ProductsCatalogResponse.from_dict(products_response.json())
    target_product = next((product for product in parsed_products.items if item_name == product.name), None)

    assert target_product, f"Товар «{item_name}» не знайдено в каталозі"
    assert target_product.price == item_price, f"Ціна товару не відповідає очікуваній: {item_price}"

    quote_payload = QuotePayload(
        items=[CartItem(product_id=target_product.id, quantity=1)],
        coupon=coupon_name,
        delivery_type=DeliveryType.STANDARD
    )
    quote_response = quote_service.calculate_quote(quote_payload)
    assert quote_response.status_code == HTTPStatus.OK, f"Помилка розрахунку кошика: {quote_response.text}"

    cart_summary = Totals.from_dict(quote_response.json())

    assert cart_summary.subtotal == item_price
    assert cart_summary.discount == discount_price
    assert cart_summary.shipping == shipping_price
    assert cart_summary.total == total_price

    order_payload = OrdersPayload(
        items=[
            CartItem(product_id=target_product.id, quantity=1)
        ],
        coupon=coupon_name,
        delivery=DeliveryType.STANDARD,
        name=customer_name,
        email=email,
        address=delivery_address,
        payment=PaymentStatus.APPROVED
    )

    order_response = orders_service.create_order(order_payload)
    assert order_response.status_code == HTTPStatus.CREATED, f"Помилка створення замовлення: {order_response.text}"

    order = OrdersResponse.from_dict(order_response.json())

    assert order.status == OrderStatus.CONFIRMED
    assert order.totals.total == total_price

    details_response = orders_service.get_order_details(order.id)
    assert details_response.status_code == HTTPStatus.OK, f"Помилка отримання деталей замовлення: {details_response.text}"
    assert OrdersResponse.from_dict(details_response.json()) == order
