import pytest

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