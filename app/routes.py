from flask import Blueprint, jsonify, request

from app.models import store

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.get("/inventory")
def list_items():
    return jsonify(store.all())


@inventory_bp.get("/inventory/<int:item_id>")
def get_item(item_id):
    item = store.get(item_id)
    if item is None:
        return jsonify({"error": "item not found"}), 404
    return jsonify(item)


@inventory_bp.post("/inventory")
def create_item():
    data = request.get_json(silent=True)
    if not data or not data.get("product_name"):
        return jsonify({"error": "product_name is required"}), 400
    item = store.create(data)
    return jsonify(item), 201


@inventory_bp.patch("/inventory/<int:item_id>")
def update_item(item_id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "request body is required"}), 400
    item = store.update(item_id, data)
    if item is None:
        return jsonify({"error": "item not found"}), 404
    return jsonify(item)


@inventory_bp.delete("/inventory/<int:item_id>")
def delete_item(item_id):
    deleted = store.delete(item_id)
    if not deleted:
        return jsonify({"error": "item not found"}), 404
    return "", 204
