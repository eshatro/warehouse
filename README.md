# Warehouse CLI Tool

Warehouse Cli tool and inventory application
============================================

## Prerequisites:
    Docker

## Installation from Dockerhub pre-build image
Run:

    $ make dh-cli-init

## Local Installation:
Run:

    $ make cli-init

And follow the instructions on screen
The commands above will build the image/pull pre-build image, run the app in a container,
open an interactive shell, execute the cli and close/remove the image when done

Other commands in the make file, or for dockerhub version, same commands with a prefix dh-*:

    $ make build

    $ make start

    $ make run-tests

    $ make clean

# Usage

To use it:

    $ warehouse-cli -if inventory.json -pf products.json


# To run tests and see coverage:
Run:

    $ make run-tests

or:

    $ make dh-run-tests
