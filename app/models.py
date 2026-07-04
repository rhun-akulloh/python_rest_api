from itertools import count

_id_counter = count(1)

FIELDS = (
    "product_name",
    "brand",
    "barcode",
    "category",
    "price",
    "quantity",
    "ingredients_text",
)


def _seed():
    return [
        {
            "id": next(_id_counter),
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "barcode": "0025293001165",
            "category": "Beverages",
            "price": 3.99,
            "quantity": 42,
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt.",
        },
        {
            "id": next(_id_counter),
            "product_name": "Peanut Butter",
            "brand": "Jif",
            "barcode": "0051500241028",
            "category": "Spreads",
            "price": 4.49,
            "quantity": 15,
            "ingredients_text": "Roasted peanuts, sugar, molasses, salt.",
        },
    ]


class InventoryStore:
    def __init__(self):
        self._items = _seed()

    def all(self):
        return list(self._items)

    def get(self, item_id):
        return next((item for item in self._items if item["id"] == item_id), None)

    def create(self, data):
        item = {"id": next(_id_counter)}
        item.update({field: data.get(field) for field in FIELDS})
        self._items.append(item)
        return item

    def update(self, item_id, data):
        item = self.get(item_id)
        if item is None:
            return None
        item.update({field: data[field] for field in FIELDS if field in data})
        return item

    def delete(self, item_id):
        item = self.get(item_id)
        if item is None:
            return False
        self._items.remove(item)
        return True


store = InventoryStore()
