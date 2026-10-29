import pytest

from core.api.api_client import APIClient

def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode (no GUI)"
    )

    parser.addoption(
        "--url",
        action="store",
        help="Required parameter to specify application url",
        required=True
    )

@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")

@pytest.fixture(scope="session")
def headless(request):
    return request.config.getoption("--headless")

@pytest.fixture(scope="function")
def api_client(base_url):
    return APIClient(base_url)

# Наступний рядок дозволяє отримати нове окреме середовище,
# яке можна буде використовувати для окремого тесту (тобто окремий тест
# буде мати доступ до двох різних середовищ одночасно).
second_api_client = api_client