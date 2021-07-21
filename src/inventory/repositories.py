from typing import Dict, List

from src.inventory.entities import Article, Product


class ProductRepository:
    def __init__(self, products: List[Product], inventory_articles: Dict[int, Article]):
        self.products = products
        self.inventory_articles = inventory_articles

    def get_all_available_products(self):
        for product in self.products:
            if not product.are_product_articles_in_stock(self.inventory_articles):
                return
            yield product

    def all_available_products(self) -> List[Product]:
        return [p for p in self.get_all_available_products()]

    def remove_one_product(self, products, product_idx: int, quantity: int):
        product = products.pop(product_idx)
        for product_article in product.articles:
            self.inventory_articles[product_article.id].available_stock -= (
                quantity * product_article.quantity
            )
