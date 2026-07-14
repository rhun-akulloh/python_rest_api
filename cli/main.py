import os

import click
import requests

API_URL = os.environ.get("INVENTORY_API_URL", "http://127.0.0.1:5000")


def _request(method, path, **kwargs):
    try:
        response = requests.request(method, f"{API_URL}{path}", timeout=10, **kwargs)
    except requests.RequestException as exc:
        raise click.ClickException(f"could not reach API at {API_URL}: {exc}")

    if response.status_code >= 400:
        try:
            message = response.json().get("error", response.text)
        except ValueError:
            message = response.text
        raise click.ClickException(f"API error ({response.status_code}): {message}")

    return response


@click.group()
def cli():
    """Inventory management CLI."""


@cli.command("add")
@click.option("--name", "product_name", required=True, help="Product name")
@click.option("--brand")
@click.option("--barcode")
@click.option("--category")
@click.option("--price", type=float, default=0)
@click.option("--quantity", type=int, default=0)
def add(product_name, brand, barcode, category, price, quantity):
    """Add a new inventory item."""
    payload = {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "category": category,
        "price": price,
        "quantity": quantity,
    }
    item = _request("POST", "/inventory", json=payload).json()
    click.echo(f"Added item {item['id']}: {item['product_name']}")


@cli.command("view")
@click.argument("item_id", type=int, required=False)
def view(item_id):
    """View all items, or a single item by id."""
    if item_id is None:
        items = _request("GET", "/inventory").json()
        if not items:
            click.echo("No inventory items.")
            return
        for item in items:
            click.echo(
                f"[{item['id']}] {item['product_name']} - ${item['price']} - qty {item['quantity']}"
            )
    else:
        item = _request("GET", f"/inventory/{item_id}").json()
        for key, value in item.items():
            click.echo(f"{key}: {value}")


@cli.command("update")
@click.argument("item_id", type=int)
@click.option("--price", type=float, help="New price")
@click.option("--quantity", type=int, help="New stock level")
def update(item_id, price, quantity):
    """Update an item's price and/or stock level."""
    payload = {}
    if price is not None:
        payload["price"] = price
    if quantity is not None:
        payload["quantity"] = quantity

    if not payload:
        raise click.ClickException("provide --price and/or --quantity")

    item = _request("PATCH", f"/inventory/{item_id}", json=payload).json()
    click.echo(f"Updated item {item['id']}: price=${item['price']}, quantity={item['quantity']}")


@cli.command("delete")
@click.argument("item_id", type=int)
def delete(item_id):
    """Delete an item."""
    _request("DELETE", f"/inventory/{item_id}")
    click.echo(f"Deleted item {item_id}")


@cli.command("find")
@click.option("--barcode")
@click.option("--name")
def find(barcode, name):
    """Find a product on the external API by barcode or name."""
    if not barcode and not name:
        raise click.ClickException("provide --barcode or --name")

    params = {"barcode": barcode} if barcode else {"name": name}
    product = _request("GET", "/inventory/lookup", params=params).json()
    for key, value in product.items():
        click.echo(f"{key}: {value}")


if __name__ == "__main__":
    cli()
