# MIT License
#
# Copyright (c) 2024 Clivern
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import click

from pexy import __version__
from pexy.command import (
    StoreInfoCommand,
    AccessScopesCommand,
    ListAllProductsCommand,
    CountProductsCommand,
)


@click.group(help="🐺 Shopify Store Swiss Knife.")
@click.version_option(version=__version__, help="Show the current version")
@click.option(
    "--name", required=True, help="Your Shopify store name (without .myshopify.com)"
)
@click.option("--token", required=True, help="Your Shopify access token")
def main(name, token):
    """Main command group for Shopify CLI."""
    global NAME, TOKEN
    NAME = name
    TOKEN = token


@main.group(help="Commands related to product operations")
def product():
    """Product command group for product operations."""
    pass


@main.group(help="Commands related to store operations")
def store():
    """Store command group for store operations."""
    pass


@product.command(help="Get products list")
def list():
    """Command to retrieve all products."""
    command = ListAllProductsCommand(NAME, TOKEN)
    return command.exec()


@product.command(help="Get products count")
def count():
    """Command to retrieve products count."""
    command = CountProductsCommand(NAME, TOKEN)
    return command.exec()


@main.group(help="Commands related to store access")
def access():
    """Access command group for scopes and permissions."""
    pass


@store.command(help="Get store information from Shopify")
def info():
    """Command to retrieve and display the store information."""
    command = StoreInfoCommand(NAME, TOKEN)
    return command.exec()


@access.command(help="Get access scope information from Shopify")
def scope():
    """Command to retrieve access scope information."""
    command = AccessScopesCommand(NAME, TOKEN)
    return command.exec()


if __name__ == "__main__":
    main()
