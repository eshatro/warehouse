import json

import click

from src.inventory.entities.factories import inventory_factory, products_factory
from src.inventory.repositories import ProductRepository
from src.inventory.serializers import ArticleSerializer, ProductSerializer


@click.command()
@click.option(
    "--inventory_file",
    "-if",
    is_flag=False,
    help="Specify a file input with designs and flowers.",
    type=click.File("r"),
)
@click.option(
    "--product_file",
    "-pf",
    is_flag=False,
    help="Specify a file input with designs and flowers.",
    type=click.File("r"),
)
def main(inventory_file, product_file):
    """CLI Warehouse"""

    # get raw data from json input
    raw_inventory = get_raw_data(inventory_file)
    raw_products = get_raw_data(product_file)

    # init the serializers
    inventory_serializer = ArticleSerializer(raw_inventory.get("inventory", []))
    product_serializer = ProductSerializer(raw_products.get("products", []))

    # validate and check for errors
    errors = [e for e in produce_errors([inventory_serializer, product_serializer])]
    if errors:
        return [click.secho(**e) for e in errors]

    # Produce Inventory and Products entities from primitive validated data
    validated_inventory_data = [i for i in inventory_serializer.validated_data]
    validated_product_data = [p for p in product_serializer.validated_data]

    inventory_articles = {
        article.id: article for article in inventory_factory(validated_inventory_data)
    }
    products = [product for product in products_factory(validated_product_data)]

    # init the product repository to deal with getting all available products and deleting a product
    product_repository = ProductRepository(products, inventory_articles)
    ps = product_repository.products

    if len(product_repository.all_available_products()) == 0:
        click.echo("No available products, update inventory!")
        return

    while len(product_repository.all_available_products()) > 0:
        click.echo("All available products, based on current inventory: ")
        [
            click.echo(
                f"{i + 1} => Product '{p.name}' with Quantity: {p.possible_quantity}"
            )
            for i, p in enumerate(product_repository.all_available_products())
        ]

        choices = [
            str(i + 1) for i in range(len(product_repository.all_available_products()))
        ]

        value = click.prompt(
            "Select a product to Remove(sell)",
            type=click.Choice(choices),
            show_choices=True,
        )
        value = int(value)
        product_index = value - 1
        selected_product_to_remove = ps[product_index]

        if not click.confirm(
            f"Product {selected_product_to_remove} is going to be deleted.\nDo you want to continue?"
        ):
            return

        quantity = selected_product_to_remove.possible_quantity
        if quantity > 1:
            quantity = click.prompt(
                "Choose a quantity for the selected product: \n",
                type=click.Choice([str(i) for i in range(1, quantity + 1)]),
                show_choices=True,
            )

        # Delete/Subtract Inventory Articles for a given Product with its Articles.
        product_repository.remove_one_product(
            product_repository.all_available_products(), product_index, int(quantity)
        )
        # TODO: write the new state of inventory into a stdout file as a means of data persistence.
        # currently defaulting to stdout
        click.echo(f"Deleted product: {ps[product_index]}")
        inventory = [
            inventory_item.__dict__
            for inventory_item in product_repository.inventory_articles.values()
        ]
        click.echo(f"Inventory: \n {inventory} \n")
    return click.echo(
        "There are no available Articles in the inventory, update inventory!"
    )


def produce_errors(serializers):
    for serializer in serializers:

        if serializer.is_valid():
            continue

        yield {
            "message": f"{serializer.name} format is not valid \n {serializer.errors}",
            "err": True,
            "fg": "red",
        }


def get_raw_data(file) -> dict:
    with file as f:
        return json.load(f)
