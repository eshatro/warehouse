from typing import List

from .article import Article


class Product:
    def __init__(
        self,
        name: str,
        articles: List[Article],
        price: float = None,
        possible_quantity: int = None,
    ):
        self.name = name
        self.price = price
        self.articles = articles
        self.possible_quantity = possible_quantity

    def __str__(self):
        return f"{self.name} ({self.possible_quantity})"

    @property
    def product_articles(self) -> set:
        return {f.id for f in self.articles}

    def calculate_possible_quantity(self, available_articles):
        possible_quantity = 99999999999999
        if not available_articles:
            self.possible_quantity = 0
            return self.possible_quantity

        for product_article in self.articles:
            stock_article = available_articles.get(product_article.id)
            times = int(stock_article.available_stock / product_article.quantity)
            if times <= 0:
                self.possible_quantity = 0
                return self.possible_quantity

            if times < possible_quantity:
                possible_quantity = times

        self.possible_quantity = possible_quantity
        return possible_quantity

    def are_product_articles_in_stock(self, available_articles):
        return (
            self.product_articles.issubset(available_articles)
            and self.calculate_possible_quantity(available_articles) > 0
        )
