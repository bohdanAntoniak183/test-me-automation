from http import HTTPStatus

from core.api.services.products_service import ProductsService
from core.api.services.favorites_service import FavoritesService
from core.api.services.orders_service import OrdersService
from core.api.models.products_service.products_catalog_response import ProductsCatalogResponse
from core.api.models.products_service.review_payload import ReviewPayload
from core.api.models.products_service.review_response import ReviewResponse
from core.api.models.favorites_service.favorites import Favorites
from core.api.models.orders_service.orders_payload import OrdersPayload
from core.api.models.orders_service.orders_response import OrdersResponse
from core.api.models.cart_item import CartItem
from core.api.models.delivery_type import DeliveryType
from core.api.models.orders_service.payment_status import PaymentStatus
from core.api.models.orders_service.order_status import OrderStatus

def test_tm_catalog_001(api_client):

    products_service = ProductsService(api_client)
    favorites_service = FavoritesService(api_client)
    orders_service = OrdersService(api_client)

    first_item_name = "Термопляшка «Щодня»"
    second_item_name = "Механічна клавіатура «Студія»"
    first_item_price = 50000
    second_item_price = 320000
    total_price = first_item_price + second_item_price
    customer_name = "Олександр Тестовий"
    email = "test@example.test"
    delivery_address = "Київ, вул. Тестова, 12"

    products_response = products_service.get_products()
    assert products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу: {products_response.text}"

    parsed_products = ProductsCatalogResponse.from_dict(products_response.json())
    first_product = next((product for product in parsed_products.items if first_item_name == product.name), None)
    second_product = next((product for product in parsed_products.items if second_item_name == product.name), None)

    assert first_product, f"Товар «{first_item_name}» не знайдено в каталозі"
    assert second_product, f"Товар «{second_item_name}» не знайдено в каталозі"
    assert first_product.price == first_item_price, f"Ціна товару «{first_item_name}» не відповідає очікуваній: {first_item_price}"
    assert second_product.price == second_item_price, f"Ціна товару «{second_item_name}» не відповідає очікуваній: {second_item_price}"

    favorites = Favorites(product_ids=[first_product.id])
    favorites_response = favorites_service.add_to_favorites(favorites)

    assert favorites_response.status_code == HTTPStatus.OK, f"Помилка додавання до обраного: {favorites_response.text}"
    assert Favorites.from_dict(favorites_response.json()) == favorites, "Повідомлення про успішне додавання не відповідає очікуваному"

    favorites_response = favorites_service.get_favorites()
    assert favorites_response.status_code == HTTPStatus.OK, f"Помилка отримання обраного: {favorites_response.text}"
    assert Favorites.from_dict(favorites_response.json()) == favorites, "Повідомлення про успішне отримання обраного не відповідає очікуваному"

    favorites = Favorites(product_ids=[first_product.id, second_product.id])
    favorites_response = favorites_service.add_to_favorites(favorites)

    assert favorites_response.status_code == HTTPStatus.OK, f"Помилка додавання до обраного: {favorites_response.text}"
    assert Favorites.from_dict(favorites_response.json()) == favorites, "Повідомлення про успішне додавання не відповідає очікуваному"

    favorites_response = favorites_service.get_favorites()
    assert favorites_response.status_code == HTTPStatus.OK, f"Помилка отримання обраного: {favorites_response.text}"
    assert Favorites.from_dict(favorites_response.json()) == favorites, "Повідомлення про успішне отримання обраного не відповідає очікуваному"

    order_payload = OrdersPayload(
        items=[
            CartItem(product_id=first_product.id, quantity=1),
            CartItem(product_id=second_product.id, quantity=1)
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

    assert order.status == OrderStatus.CONFIRMED, f"Статус замовлення не відповідає очікуваному: {OrderStatus.CONFIRMED}"
    assert order.totals.total == total_price, f"Загальна сума замовлення не відповідає очікуваній: {total_price}, отримано: {order.totals.total}"

    details_response = orders_service.get_order_details(order.id)
    assert details_response.status_code == HTTPStatus.OK, f"Помилка отримання деталей замовлення: {details_response.text}"

    parsed_order_details = OrdersResponse.from_dict(details_response.json())

    assert parsed_order_details == order, "Деталі замовлення не відповідають очікуваному замовленню"
    assert parsed_order_details.totals.total == total_price, f"Загальна сума замовлення в деталях не відповідає очікуваній: {total_price}, отримано: {parsed_order_details.totals.total}"

    review = ReviewPayload(rating=1, text="Поганий продукт, не рекомендую.")
    product_review_response = products_service.leave_product_review(first_product.id, review)

    assert product_review_response.status_code == HTTPStatus.CREATED, f"Помилка залишення відгуку: {product_review_response.text}"
    assert ReviewResponse.from_dict(product_review_response.json()).review == review, "Відгук не відповідає очікуваному"

    product_review_response = products_service.get_product_review(first_product.id)
    assert product_review_response.status_code == HTTPStatus.OK, f"Помилка отримання відгуку: {product_review_response.text}"
    assert ReviewResponse.from_dict(product_review_response.json()).review == review, "Отриманий відгук не відповідає очікуваному"

    review = ReviewPayload(rating=5, text="Клавіатура клас, думаю замовити ще одну.")
    product_review_response = products_service.leave_product_review(second_product.id, review)

    assert product_review_response.status_code == HTTPStatus.CREATED, f"Помилка залишення відгуку: {product_review_response.text}"
    assert ReviewResponse.from_dict(product_review_response.json()).review == review, "Відгук не відповідає очікуваному"

    product_review_response = products_service.get_product_review(second_product.id)
    assert product_review_response.status_code == HTTPStatus.OK, f"Помилка отримання відгуку: {product_review_response.text}"
    assert ReviewResponse.from_dict(product_review_response.json()).review == review, "Отриманий відгук не відповідає очікуваному"
