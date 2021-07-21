import pytest

from warehouse_cli.cli import get_raw_data


@pytest.fixture
def inventory_file():
    return "tests/cli/data/inventory_invalid.json"


@pytest.fixture
def products_file():
    return "tests/cli/data/products_invalid.json"


@pytest.fixture
def invalid_inventory_file():
    return "tests/cli/data/inventory.json"


@pytest.fixture
def invalid_products_file():
    return "tests/cli/data/products.json"


@pytest.fixture
def valid_inventory_data(inventory_file):
    return get_raw_data(inventory_file)["inventory"]


@pytest.fixture
def valid_products_data(products_file):
    return get_raw_data(products_file)["products"]


@pytest.fixture
def invalid_inventory_data(invalid_inventory_file):
    return get_raw_data(inventory_file)["inventory"]


@pytest.fixture
def invalid_products_data(invalid_products_file):
    return get_raw_data(products_file)["products"]


# @pytest.fixture
# def designs_and_available_flowers(file, request):
#     designs, flowers = get_text(open(request.getfixturevalue(file), "r"))
#     return designs, build_available_flowers_histogram(flowers)
