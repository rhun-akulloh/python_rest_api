from flask import jsonify, request, Flask

from app.external_api import  fetch_by_barcode, search_by_name

from app.models import store

app = Flask(__name__)


# GET-read/retreieve, DELETE-delete, POST-add, PATCH-update

@app.get("/inventory")
def list_items():
    return jsonify(store.all())


@app.get("/inventory/<int:item_id>")
def get_item(item_id):
    item = store.get(item_id)
    if not item:
        return jsonify({"error": "item not found"}), 404
    else:
        return jsonify(item)


@app.post("/inventory")
def create_item():
    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="request body is required"), 400
    if not data.get("product_name"):
        return jsonify(error="product_name is required"), 400

    item = store.create(data)
    return jsonify(item), 201


@app.patch("/inventory/<int:item_id>")
def update_item(item_id):
    item = store.get(item_id)
    if not item:
        return jsonify(error="item not found"), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify(error="request body is required"), 400

    updated_item = store.update(item_id, data)
    return jsonify(updated_item)


@app.delete("/inventory/<int:item_id>")
def delete_item(item_id):
    item = store.get(item_id)
    if not item:
        return jsonify(error="item not found"), 404
    deleted = store.delete(item_id)
    if not deleted:
        return jsonify(error="Cannot delete item"), 404
    return "", 204


@app.get("/inventory/lookup")
def lookup_external():
    barcode = request.args.get("barcode")
    name = request.args.get("name")
    if not barcode and not name:
        return jsonify(error="barcode or name query param is required"), 400

    if barcode:
        product = fetch_by_barcode(barcode)
    else:
        product = search_by_name(name)

    if not product:
        return jsonify(error="product not found"), 404
    else:
        return jsonify(product)


@app.post("/inventory/import")
def import_external():
    data = request.get_json(silent=True) or {}
    barcode = data.get("barcode")
    name = data.get("name")

    if not barcode and not name:
        return jsonify(error="barcode or name is required"), 400

    if barcode:
        product = fetch_by_barcode(barcode)
    else:
        product = search_by_name(name)

    if not product:
        return jsonify(error="product not found"), 404

    product["price"] = data.get("price", 0)
    product["quantity"] = data.get("quantity", 0)

    item = store.create(product)
    return jsonify(item), 201

if __name__ == "__main__":
    app.run(debug=True)