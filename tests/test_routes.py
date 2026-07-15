def test_inventory_crud_flow(client):
    assert client.post("/inventory", json={"price": 1}).status_code == 400

    created = client.post(
        "/inventory", json={"product_name": "Widget", "price": 1.5, "quantity": 3}
    )
    assert created.status_code == 201
    item_id = created.get_json()["id"]

    get_resp = client.get(f"/inventory/{item_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["product_name"] == "Widget"

    patch_resp = client.patch(f"/inventory/{item_id}", json={"quantity": 10})
    assert patch_resp.status_code == 200
    assert patch_resp.get_json()["quantity"] == 10

    assert client.delete(f"/inventory/{item_id}").status_code == 204
    assert client.get(f"/inventory/{item_id}").status_code == 404
