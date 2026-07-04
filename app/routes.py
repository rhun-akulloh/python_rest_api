from flask import Blueprint, jsonify, request

from app.external_api import ExternalAPIError, fetch_by_barcode, search_by_name
from app.models import store

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.get("/inventory")
def list_items():
    return jsonify(store.all())


@inventory_bp.get("/inventory/<int:item_id>")
def get_item(item_id):
    item = store.get(item_id)
    if not item:
        return jsonify({"error": "item not found"}), 404
    return jsonify(item)


@inventory_bp.post("/inventory")
def create_item():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="request body is required"), 400
    if not data.get("product_name"):
        return jsonify(error="product_name is required"), 400

    item = store.create(data)
    return jsonify(item), 201


@inventory_bp.patch("/inventory/<int:item_id>")
def update_item(item_id):
    item = store.get(item_id)
    if not item:
        return jsonify(error="item not found"), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="request body is required"), 400

    updated = store.update(item_id, data)
    return jsonify(updated)


@inventory_bp.delete("/inventory/<int:item_id>")
def delete_item(item_id):
    ok = store.delete(item_id)
    if not ok:
        return jsonify(error="item not found"), 404
    return "", 204


@inventory_bp.get("/inventory/lookup")
def lookup_external():
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    if not barcode and not name:
        return jsonify(error="barcode or name query param is required"), 400

    try:
        if barcode:
            product = fetch_by_barcode(barcode)
        else:
            product = search_by_name(name)
    except ExternalAPIError as exc:
        return jsonify(error=str(exc)), 502

    if not product:
        return jsonify(error="product not found"), 404
    return jsonify(product)


@inventory_bp.post("/inventory/import")
def import_external():
    data = request.get_json(silent=True) or {}
    barcode = data.get("barcode")
    name = data.get("name")

    if not barcode and not name:
        return jsonify(error="barcode or name is required"), 400

    try:
        if barcode:
            product = fetch_by_barcode(barcode)
        else:
            product = search_by_name(name)
    except ExternalAPIError as exc:
        return jsonify(error=str(exc)), 502

    if not product:
        return jsonify(error="product not found"), 404

    # off doesn't know about price/qty obviously, so just bolt those on from the request
    product["price"] = data.get("price", 0)
    product["quantity"] = data.get("quantity", 0)

    item = store.create(product)
    return jsonify(item), 201
