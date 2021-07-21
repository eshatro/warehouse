import pytest

from src.inventory.serializers import ArticleSerializer, ProductSerializer


@pytest.mark.parametrize(
    "article_data, expected, expected_errors",
    [
        (
            [{"art_id": "1", "name": "leg", "stock": "12"}],
            [{"id": 1, "name": "leg", "available_stock": 12}],
            [],
        ),
        (
            [{"art_id": "leg", "name": "leg", "stock": "leg"}],
            [],
            [
                {"art_id": "Value 'leg' is not a valid integer"},
                {"stock": "Value 'leg' is not a valid integer"},
            ],
        ),
        (
            [{"art_id": "1", "name": "leg", "stock": "1", "amount_of": "test"}],
            [],
            [{"amount_of": "Value 'test' is not a valid integer"}],
        ),
        ([{"name": "leg", "stock": "12"}], [], [{"art_id": "This field is required"}]),
    ],
)
def test_design_serializer(article_data, expected, expected_errors):
    article_serializer = ArticleSerializer(data=article_data)

    assert expected == [d for d in article_serializer.validated_data]
    assert expected_errors == article_serializer.errors[article_serializer.name]


@pytest.mark.parametrize(
    "product_data, expected, expected_errors",
    [
        (
            [
                {"contain_articles": ""},
            ],
            [],
            [
                {"name": "This field is required"},
                {"contain_articles": "This field is required"},
            ],
        ),
        (
            [
                {
                    "name": "Dinning Table",
                    "contain_articles": [{"art_id": "1", "amount_of": "4"}],
                }
            ],
            [{"name": "Dinning Table", "articles": [{"id": 1, "quantity": 4}]}],
            [],
        ),
    ],
)
def test_flower_serializer(product_data, expected, expected_errors):
    p = ProductSerializer(data=product_data)

    assert expected == [p for p in p.validated_data]
    assert expected_errors == p.errors[p.name]
