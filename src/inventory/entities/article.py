class Article:
    def __init__(self, id: int, name: str = None, available_stock: int = 0, quantity: int = 0):
        self.id = id
        self.name = name
        self.available_stock = available_stock
        self.quantity = quantity

    def __str__(self):
        return f"{str(self.id) + '_' + self.name + ' ' + str(self.available_stock)}"
