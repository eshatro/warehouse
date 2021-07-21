import pytest

from src.inventory.entities import Article, Product
from src.inventory.repositories import ProductRepository


@pytest.mark.parametrize(
    "inventory, products, expected_quantity",
    [
        (
            {1: Article(1, "item", available_stock=10)},
            [Product("Prod", [Article(1, quantity=5)])],
            2,
        ),
        (
            {
                1: Article(1, "item", available_stock=10),
                2: Article(2, "item", available_stock=5),
            },
            [Product("Prod", [Article(1, quantity=5), Article(2, quantity=2)])],
            2,
        ),
        (
            {
                1: Article(1, "item", available_stock=10),
                2: Article(2, "item", available_stock=5),
            },
            [
                Product("Prod", [Article(1, quantity=5)]),
                Product("Prod 2", [Article(2, quantity=2)]),
            ],
            4,
        ),
    ],
)
def test_product_repository_all_available_products(
    inventory, products, expected_quantity
):
    product_repository = ProductRepository(products, inventory)
    possible_quantities = sum(
        [p.possible_quantity for p in product_repository.all_available_products()]
    )

    assert possible_quantities == expected_quantity


@pytest.mark.parametrize(
    "inventory, products, quantity, expected_inventory",
    [
        (
            {1: Article(1, "item", available_stock=10)},
            [Product("Prod", [Article(1, quantity=5)])],
            1,
            "1_item 5",
        ),
        (
            {1: Article(1, "item", available_stock=10)},
            [Product("Prod", [Article(1, quantity=10)])],
            1,
            "1_item 0",
        ),
        (
            {
                1: Article(1, "item", available_stock=10),
                2: Article(2, "item", available_stock=5),
            },
            [
                Product("Prod", [Article(1, quantity=5)]),
                Product("Prod 2", [Article(2, quantity=2)]),
            ],
            2,
            "1_item 0",
        ),
    ],
)
def test_product_repository_remove_available_product(
    inventory, products, quantity, expected_inventory
):
    product_repository = ProductRepository(products, inventory)
    available_products = [p for p in product_repository.all_available_products()]

    assert len(available_products) == len(products)

    product_repository.remove_one_product(available_products, 0, quantity)
    assert len(available_products) == len(products) - 1
    assert str(product_repository.inventory_articles[1]) == expected_inventory
