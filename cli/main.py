import os

import click
import requests

DEFAULT_API_URL = "http://127.0.0.1:5000"


def _api_url():
    return os.environ.get("INVENTORY_API_URL", DEFAULT_API_URL)


def _request(method, path, **kwargs):
    url = f"{_api_url()}{path}"
    try:
        response = requests.request(method, url, timeout=10, **kwargs)
    except requests.RequestException as exc:
        raise click.ClickException(f"could not reach API at {url}: {exc}")

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


@cli.command("list")
def list_items():
    items = _request("GET", "/inventory").json()
    if not items:
        click.echo("No inventory items.")
        return
    for item in items:
        click.echo(
            f"[{item['id']}] {item['product_name']} - {item.get('brand') or 'n/a'} "
            f"- ${item.get('price')} - qty {item.get('quantity')}"
        )


@cli.command("get")
@click.argument("item_id", type=int)
def get_item(item_id):
    click.echo(_request("GET", f"/inventory/{item_id}").json())


@cli.command("add")
@click.option("--name", "product_name", required=True)
@click.option("--brand")
@click.option("--barcode")
@click.option("--category")
@click.option("--price", type=float, default=0)
@click.option("--quantity", type=int, default=0)
@click.option("--ingredients", "ingredients_text")
def add_item(product_name, brand, barcode, category, price, quantity, ingredients_text):
    payload = {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "category": category,
        "price": price,
        "quantity": quantity,
        "ingredients_text": ingredients_text,
    }
    item = _request("POST", "/inventory", json=payload).json()
    click.echo(f"Created item {item['id']}")


@cli.command("update")
@click.argument("item_id", type=int)
@click.option("--name", "product_name")
@click.option("--brand")
@click.option("--barcode")
@click.option("--category")
@click.option("--price", type=float)
@click.option("--quantity", type=int)
@click.option("--ingredients", "ingredients_text")
def update_item(item_id, product_name, brand, barcode, category, price, quantity, ingredients_text):
    payload = {
        k: v
        for k, v in {
            "product_name": product_name,
            "brand": brand,
            "barcode": barcode,
            "category": category,
            "price": price,
            "quantity": quantity,
            "ingredients_text": ingredients_text,
        }.items()
        if v is not None
    }
    if not payload:
        raise click.ClickException("provide at least one field to update")
    item = _request("PATCH", f"/inventory/{item_id}", json=payload).json()
    click.echo(f"Updated item {item['id']}")


@cli.command("delete")
@click.argument("item_id", type=int)
def delete_item(item_id):
    _request("DELETE", f"/inventory/{item_id}")
    click.echo(f"Deleted item {item_id}")


@cli.command("find-external")
@click.option("--barcode")
@click.option("--name")
def find_external(barcode, name):
    if not barcode and not name:
        raise click.ClickException("provide --barcode or --name")
    params = {"barcode": barcode} if barcode else {"name": name}
    click.echo(_request("GET", "/inventory/lookup", params=params).json())


@cli.command("import-external")
@click.option("--barcode")
@click.option("--name")
@click.option("--price", type=float, default=0)
@click.option("--quantity", type=int, default=0)
def import_external(barcode, name, price, quantity):
    if not barcode and not name:
        raise click.ClickException("provide --barcode or --name")
    payload = {"barcode": barcode, "name": name, "price": price, "quantity": quantity}
    item = _request("POST", "/inventory/import", json=payload).json()
    click.echo(f"Imported item {item['id']}")


if __name__ == "__main__":
    cli()
