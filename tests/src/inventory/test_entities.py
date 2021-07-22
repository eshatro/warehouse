import pytest

from src.inventory.entities import Article, Product


@pytest.mark.parametrize(
    "article_data, expected",
    [
        ([2, "leg", 12], "2_leg 12"),
        ([3, "table_top", 2], "3_table_top 2"),
    ],
)
def test_article(article_data, expected):
    article = Article(*article_data)
    assert str(article) == expected


@pytest.mark.parametrize(
    "product_data, inventory_articles, expected_product_str, "
    "expected_product_articles, "
    "are_products_in_stock, expected_possible_quantity",
    [
        (
            (
                "Chair",
                [
                    Article(1, "leg", quantity=4),
                    Article(2, "seat", quantity=1),
                    Article(3, "screw", quantity=8),
                ],
            ),
            {},
            "Chair (0)",
            {1, 2, 3},
            False,
            0,
        ),
        (
            (
                "Chair",
                [
                    Article(1, "leg", quantity=4),
                    Article(2, "seat", quantity=1),
                    Article(3, "screw", quantity=8),
                ],
            ),
            {
                1: Article(1, "leg", available_stock=4),
                2: Article(1, "seat", available_stock=2),
                3: Article(1, "screw", available_stock=8),
            },
            "Chair (1)",
            {1, 2, 3},
            True,
            1,
        ),
        (
            (
                "Chair",
                [
                    Article(1, "leg", quantity=4),
                    Article(2, "seat", quantity=1),
                    Article(3, "screw", quantity=8),
                ],
            ),
            {
                1: Article(1, "leg", available_stock=8),
                2: Article(1, "seat", available_stock=2),
                3: Article(1, "screw", available_stock=17),
            },
            "Chair (2)",
            {1, 2, 3},
            True,
            2,
        ),
    ],
)
def test_product(
    product_data,
    inventory_articles,
    expected_product_str,
    expected_product_articles,
    are_products_in_stock,
    expected_possible_quantity,
):
    p = Product(*product_data)

    assert expected_product_articles == p.product_articles
    assert p.are_product_articles_in_stock(inventory_articles) == are_products_in_stock
    assert (
        p.calculate_possible_quantity(inventory_articles) == expected_possible_quantity
    )
    assert str(p) == expected_product_str
