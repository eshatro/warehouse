import pytest
from click.testing import CliRunner

from warehouse_cli import cli

expected_errors = (
    "Article format is not valid \n"
    " {'Article': [{'art_id': \"Value 'lll' is not a valid integer\"}, "
    "{'stock': \"Value 'leg' is not a valid integer\"}]}\n"
    "Product format is not valid \n"
    " {'Product': [{'contain_articles': 'This field is required'}]}"
)


@pytest.fixture
def runner():
    return CliRunner()


def test_cli(runner):
    result = runner.invoke(cli.main)
    assert result.exit_code == 1
    assert isinstance(result.exception, AttributeError)


def test_cli_without_option_1(runner):
    result = runner.invoke(cli.main, ["--f"])
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 2


def test_cli_without_option_2(runner, inventory_file):
    result = runner.invoke(cli.main, args=["-fi", inventory_file, "-fp", ""])
    assert isinstance(result.exception, SystemExit)
    assert result.exit_code == 2


@pytest.mark.parametrize(
    "inventory_file, products_file, expected",
    [
        (
            "tests/cli/data/inventory_invalid.json",
            "tests/cli/data/products_invalid.json",
            expected_errors,
        ),
    ],
)
def test_cli_with_arg_invalid_files(runner, inventory_file, products_file, expected):
    result = runner.invoke(cli.main, args=["-if", inventory_file, "-pf", products_file])
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == expected


expected_text = (
    "All available products, based on current inventory: \n"
    "1 => Product 'Dining Chair' with Quantity: 2\n"
    "2 => Product 'Dinning Table' with Quantity: 1\n"
    "Select a product to Remove(sell) (1, 2): 2\n"
    "Product Dinning Table (1) is going to be deleted.\n"
    "Do you want to continue? [y/N]:"
)


@pytest.mark.parametrize(
    "inventory_file, products_file, expected",
    [
        (
            "tests/cli/data/inventory.json",
            "tests/cli/data/products.json",
            expected_text,
        ),
    ],
)
def test_cli_with_arg(runner, inventory_file, products_file, expected):
    result = runner.invoke(
        cli.main, args=["-if", inventory_file, "-pf", products_file], input="2\n"
    )
    assert result.exit_code == 0
    assert not result.exception
    assert result.output.strip() == expected
