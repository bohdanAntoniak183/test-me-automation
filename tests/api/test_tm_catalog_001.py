from http import HTTPStatus

from core.api.services.products_service import ProductsService
from core.api.models.products_service.products_catalog_response import ProductsCatalogResponse
from core.api.models.products_service.sort_type import SortType

def test_tm_catalog_001(api_client):

    products_service = ProductsService(api_client)

    category = "Lifestyle"

    products_response = products_service.get_products()
    assert products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу: {products_response.text}"

    all_parsed_products = ProductsCatalogResponse.from_dict(products_response.json())

    categorised_products_response = products_service.get_products(category=category)
    assert categorised_products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу за категорією: {categorised_products_response.text}"

    categorised_parsed_products = ProductsCatalogResponse.from_dict(categorised_products_response.json())
    assert len([product for product in all_parsed_products.items if product.category == category]) == len(categorised_parsed_products.items), \
        f"Помилка фільтрації товарів за категорією '{category}' - очікувано {len([product for product in all_parsed_products.items if product.category == category])} товарів, отримано {len(categorised_parsed_products.items)}"

    for categorised_product in categorised_parsed_products.items:
        assert categorised_product.category == category, f"Помилка фільтрації товарів за категорією '{category}' - знайдено товар з категорією '{categorised_product.category}'"

    categorised_products_response = products_service.get_products(
        category=category,
        sort=SortType.PRICE_ASC
    )
    assert categorised_products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу за категорією: {categorised_products_response.text}"

    categorised_parsed_products = ProductsCatalogResponse.from_dict(categorised_products_response.json())
    sorted_products = sorted(categorised_parsed_products.items, key=lambda product: product.price)
    assert sorted_products == categorised_parsed_products.items, f"Помилка сортування товарів за зростанням ціни"

    for categorised_product in categorised_parsed_products.items:
        assert categorised_product.category == category, f"Помилка фільтрації товарів за категорією '{category}' - знайдено товар з категорією '{categorised_product.category}'"

    categorised_products_response = products_service.get_products(
        category=category,
        sort=SortType.PRICE_DESC
    )
    assert categorised_products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу за категорією: {categorised_products_response.text}"

    categorised_parsed_products = ProductsCatalogResponse.from_dict(categorised_products_response.json())
    sorted_products = sorted(categorised_parsed_products.items, key=lambda product: product.price, reverse=True)
    assert sorted_products == categorised_parsed_products.items, f"Помилка сортування товарів за спаданням ціни"

    for categorised_product in categorised_parsed_products.items:
        assert categorised_product.category == category, f"Помилка фільтрації товарів за категорією '{category}' - знайдено товар з категорією '{categorised_product.category}'"

    categorised_products_response = products_service.get_products(
        category=category,
        sort=SortType.PRICE_DESC,
        in_stock=True
    )
    assert categorised_products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу за категорією: {categorised_products_response.text}"

    categorised_parsed_products = ProductsCatalogResponse.from_dict(categorised_products_response.json())
    sorted_products = sorted(categorised_parsed_products.items, key=lambda product: product.price, reverse=True)
    assert sorted_products == categorised_parsed_products.items, f"Помилка сортування товарів за спаданням ціни"

    for categorised_product in categorised_parsed_products.items:
        assert categorised_product.category == category, f"Помилка фільтрації товарів за категорією '{category}' - знайдено товар з категорією '{categorised_product.category}'"
        assert categorised_product.stock > 0, f"Помилка фільтрації товарів за наявністю на складі - знайдено товар з нульовим запасом: '{categorised_product.name}'"

    categorised_products_response = products_service.get_products(
        category=category,
        sort=SortType.PRICE_DESC,
        in_stock=True,
        min_price=45000
    )
    assert categorised_products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу за категорією: {categorised_products_response.text}"

    categorised_parsed_products = ProductsCatalogResponse.from_dict(categorised_products_response.json())
    sorted_products = sorted(categorised_parsed_products.items, key=lambda product: product.price, reverse=True)
    assert sorted_products == categorised_parsed_products.items, f"Помилка сортування товарів за спаданням ціни"

    for categorised_product in categorised_parsed_products.items:
        assert categorised_product.category == category, f"Помилка фільтрації товарів за категорією '{category}' - знайдено товар з категорією '{categorised_product.category}'"
        assert categorised_product.stock > 0, f"Помилка фільтрації товарів за наявністю на складі - знайдено товар з нульовим запасом: '{categorised_product.name}'"
        assert categorised_product.price >= 45000, f"Помилка фільтрації товарів за мінімальною ціною - знайдено товар з ціною нижче 45000: '{categorised_product.name}'"

    categorised_products_response = products_service.get_products(
        category=category,
        sort=SortType.PRICE_DESC,
        in_stock=True,
        min_price=45000,
        max_price=60000
    )
    assert categorised_products_response.status_code == HTTPStatus.OK, f"Помилка отримання каталогу за категорією: {categorised_products_response.text}"

    categorised_parsed_products = ProductsCatalogResponse.from_dict(categorised_products_response.json())
    sorted_products = sorted(categorised_parsed_products.items, key=lambda product: product.price, reverse=True)
    assert sorted_products == categorised_parsed_products.items, f"Помилка сортування товарів за спаданням ціни"

    for categorised_product in categorised_parsed_products.items:
        assert categorised_product.category == category, f"Помилка фільтрації товарів за категорією '{category}' - знайдено товар з категорією '{categorised_product.category}'"
        assert categorised_product.stock > 0, f"Помилка фільтрації товарів за наявністю на складі - знайдено товар з нульовим запасом: '{categorised_product.name}'"
        assert categorised_product.price >= 45000, f"Помилка фільтрації товарів за мінімальною ціною - знайдено товар з ціною нижче 45000: '{categorised_product.name}'"
        assert categorised_product.price <= 60000, f"Помилка фільтрації товарів за максимальною ціною - знайдено товар з ціною вище 60000: '{categorised_product.name}'"
