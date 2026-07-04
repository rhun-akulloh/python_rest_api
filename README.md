# Inventory Management System

Flask REST API and CLI for managing retail inventory, with OpenFoodFacts lookups.

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the API

```
python run.py
```

Runs at http://127.0.0.1:5000

## API endpoints

Basic CRUD on `/inventory`:

- `GET /inventory` - list all items
- `GET /inventory/<id>` - get one item
- `POST /inventory` - create an item (requires `product_name`)
- `PATCH /inventory/<id>` - update an item
- `DELETE /inventory/<id>` - delete an item

There are also a couple of endpoints that hit OpenFoodFacts directly:

- `GET /inventory/lookup?barcode=<code>` (or `?name=<name>`) looks up a product without saving it.
- `POST /inventory/import` does the same lookup and adds the result to inventory. Body needs `barcode` or `name`, and you can pass `price`/`quantity` too since OpenFoodFacts obviously doesn't know those.

## CLI

With the API running, use the CLI in a separate terminal:

```
python -m cli.main list
python -m cli.main get 1
python -m cli.main add --name "Widget" --price 9.99 --quantity 10
python -m cli.main update 1 --quantity 20
python -m cli.main delete 1
python -m cli.main find-external --barcode 3017620422003
python -m cli.main import-external --barcode 3017620422003 --price 4.99 --quantity 15
```

Set `INVENTORY_API_URL` if the API isn't running on the default address.

## Tests

```
pytest
```
