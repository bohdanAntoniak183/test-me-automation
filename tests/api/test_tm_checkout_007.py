from http import HTTPStatus

from core.api.services.products_service import ProductsService
from core.api.services.orders_service import OrdersService
from core.api.models.products_service.products_catalog_response import ProductsCatalogResponse
from core.api.models.orders_service.orders_response import OrdersResponse
from core.api.models.orders_service.orders_payload import OrdersPayload
from core.api.models.cart_item import CartItem
from core.api.models.delivery_type import DeliveryType
from core.api.models.orders_service.payment_status import PaymentStatus
from core.api.models.orders_service.order_status import OrderStatus

def test_tm_checkout_007(api_client):

    products_service = ProductsService(api_client)
    orders_service = OrdersService(api_client)

    item_name = "Термопляшка «Щодня»"
    customer_name = "Олександр Тестовий"
    email = "test@example.test"
    delivery_address = "Київ, вул. Тестова, 12"

    products_response = products_service.get_products()
    assert products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу: {products_response.text}"

    parsed_products = ProductsCatalogResponse.from_dict(products_response.json())
    target_product = next((product for product in parsed_products.items if item_name == product.name), None)

    assert target_product, f"Товар «{item_name}» не знайдено в каталозі"

    order_payload = OrdersPayload(
        items=[
            CartItem(product_id=target_product.id, quantity=1)
        ],
        name=customer_name,
        email=email,
        address=delivery_address,
        delivery=DeliveryType.STANDARD,
        payment=PaymentStatus.APPROVED
    )

    order_response = orders_service.create_order(order_payload)
    assert order_response.status_code == HTTPStatus.CREATED, f"Помилка створення замовлення: {order_response.text}"

    order = OrdersResponse.from_dict(order_response.json())

    assert order.status == OrderStatus.CONFIRMED

    cancel_order_response = orders_service.cancel_order(order.id)
    assert cancel_order_response.status_code == HTTPStatus.OK, f"Помилка скасування замовлення: {cancel_order_response.text}"

    cancelled_order = OrdersResponse.from_dict(cancel_order_response.json())
    assert cancelled_order.id == order.id, "ID скасованого замовлення не збігається з ID створеного замовлення"
    assert cancelled_order.status == OrderStatus.CANCELLED, "Статус скасованого замовлення не відповідає очікуваному"

    details_response = orders_service.get_order_details(cancelled_order.id)
    assert details_response.status_code == HTTPStatus.OK, f"Помилка отримання деталей замовлення: {details_response.text}"

    received_order_details = OrdersResponse.from_dict(details_response.json())

    assert received_order_details.id == cancelled_order.id, "ID отриманого замовлення не збігається з ID скасованого замовлення"
    assert received_order_details.status == OrderStatus.CANCELLED, "Статус отриманого замовлення не відповідає очікуваному після скасування"

    cancel_order_response = orders_service.cancel_order(order.id)
    assert cancel_order_response.status_code == HTTPStatus.CONFLICT, f"Очікувано помилку 409 при повторному скасуванні замовлення, але отримано: {cancel_order_response.status_code}"

    details_response = orders_service.get_order_details(cancelled_order.id)
    assert details_response.status_code == HTTPStatus.OK, f"Помилка отримання деталей замовлення: {details_response.text}"

    received_order_details = OrdersResponse.from_dict(details_response.json())

    assert received_order_details.id == cancelled_order.id, "ID отриманого замовлення не збігається з ID скасованого замовлення"
    assert received_order_details.status == OrderStatus.CANCELLED, "Статус отриманого замовлення не відповідає очікуваному після повторного скасування"
