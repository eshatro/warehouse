from typing import List, Dict
from .article import Article
from .product import Product


def inventory_factory(articles: List[Dict]):
    for article in articles:
        yield Article(**article)


def products_factory(products: List[Dict]):
    for product in products:
        product["articles"] = [Article(**article_data) for article_data in product["articles"]]
        yield Product(**product)
