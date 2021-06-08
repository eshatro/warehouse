from abc import ABC
from src.inventory.validators import val_str, val_int, check_type


class Serializer(ABC):
    fields = {}
    required_fields = []
    name = "BaseSerializer"

    def __init__(self, data: list or str):
        self.data = data
        self.errors = {}

    def clean(self):
        return self.data

    def is_valid(self):
        data = self.clean()
        self.errors[self.name] = []
        for value in data:
            for key, field in self.fields.items():
                item = value.get(key)

                if not item and key in self.required_fields:
                    self.errors[self.name].append({key: "This field is required"})
                    continue

                if not item and key not in self.required_fields:
                    continue

                if not field.get("validator"):
                    continue

                valid, error_message = field["validator"](item)
                if not valid:
                    self.errors[self.name].append({key: error_message})

        if self.errors[self.name]:
            return False

        return True

    def print_errors(self) -> str:
        return f"{': '.join(self.errors)}\n"

    @property
    def validated_data(self):
        if not self.is_valid():
            return None

        for data in self.clean():
            new_field = {}
            for key, field in self.fields.items():
                item = data.get(key)
                if not item:
                    continue

                if not field.get("validator"):
                    continue

                new_field.update({
                    field["name"]: field.get("validator")(item).message
                })

                if field.get("serializer"):
                    new_field.update({
                        field["name"]: [i for i in field["serializer"](item).validated_data]
                    })

            yield new_field


class ArticleSerializer(Serializer):
    name = "Article"
    required_fields = ["art_id"]
    fields = {
        "art_id": {"name": "id", "type": int, "validator": val_int},
        "name": {"name": "name", "type": str, "validator": val_str},
        "stock": {"name": "available_stock", "type": int, "default": 0, "validator": val_int},
        "amount_of": {"name": "quantity", "type": int, "default": 0, "validator": val_int},
    }


class ProductSerializer(Serializer):
    name = "Product"
    required_fields = ["name", "contain_articles"]
    fields = {
        "name": {"name": "name", "type": str, "validator": val_str},
        "contain_articles": {"name": "articles", "type": list, "serializer": ArticleSerializer,
                             "validator": check_type},
    }
