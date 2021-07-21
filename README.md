# Warehouse CLI Tool

Warehouse Cli tool and inventory application
============================================

## Prerequisites:
    Docker

## Installation:
Run:

    $ make cli-init

And follow the instructions on screen
This command will build the image, run the app in a container,
open an interactive shell, execute the cli and close/remove the container when done

Other commands in the make file:

    $ make build

    $ make start

    $ make run-tests

# Usage

To use it:

    $ warehouse-cli -if inventory.json -pf products.json


# To run tests and see coverage:
Run:

    $ make run-tests
CLI Warehouse
# Things to look out for

Under `src/` there is the main business logic of the warehouse with 1 application/package called inventory
    under `src/inventory` there are serializers and validators for incoming data from the json files
    and inventory/repositories.py in particular hold the main state of the Articles in the inventory.

under `warehouse_cli/` is the  cli application/package used to get all the available products based on inventory
and remove products one by one with an associated quantity.

There are no state changes saved to the file `inventory.json` nor to any other new file to write the result,
that is intentionally, and the result will default to stdout for demo purposes.
CPU bound,
need to calculate the availability of products every time 1 gets removed
