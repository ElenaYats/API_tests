import pytest
from pathlib import Path

def pytest_addoption(parser):
    parser.addoption(
        "--url",
        help="This is request url"
    )
@pytest.fixture
def base_url(request):
    test_file = Path(str(request.node.fspath)).name
    url_option = request.config.getoption("--url")

    print(f"Command-line URL option: {url_option}")
    print(f"Detected test file: {test_file}")

    if url_option:
        print(f"Using URL from --url: {url_option}")
        return url_option

    if test_file == "test_dog_ceo.py":
        print("Using default URL for test_dog_ceo.py")
        return "https://dog.ceo/dog-api/"
    elif test_file == "test_openbrewerydb.py":
        print("Using default URL for test_openbrewerydb.py")
        return "https://www.openbrewerydb.org/"
    else:
        print("Using fallback default URL")
        return "https://jsonplaceholder.typicode.com/"
