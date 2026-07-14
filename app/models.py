from itertools import count

_id_counter = count(1)

# order matters here for the CLI table output, don't reorder without checking cli/main.py
FIELDS = ("product_name", "brand", "barcode", "category", "price", "quantity", "ingredients_text")





class InventoryStore:
    """in-memory store, swap this out for a real DB later"""

    def __init__(self):
        self._items =  [{
            "id": next(_id_counter),
            "product_name": "Peanut Butter",
            "brand": "Jif",
            "barcode": "0051500241028",
            "category": "Spreads",
            "price": 4.49,
            "quantity": 15,
            "ingredients_text": "Roasted peanuts, sugar, molasses, salt.",
            },
            {
            "id": next(_id_counter),
            "product_name": "Organic Almond Milk",
            "brand": "Silk",
            "barcode": "0025293001165",
            "category": "Beverages",
            "price": 3.99,
            "quantity": 42,
            "ingredients_text": "Filtered water, almonds, cane sugar, sea salt.",
        }]
    def all(self):
        # return a  list of the items in the array
        return list(self._items)

    def get(self, item_id):
        #return a particular item in the array
        for item in self._items:
            if item["id"] == item_id:
                return item
        return None

    def create(self, data):
        # adds a new item to the array
        item = {"id": next(_id_counter)}
        for field in FIELDS:
            item[field] = data.get(field)
        self._items.append(item)
        return item

    def update(self, item_id, data):
        # updates an existing item in the array
        item = self.get(item_id)
        if not item:
            return None
        for field in FIELDS:
            if field in data:
                item[field] = data[field]
        return item

    def delete(self, item_id):
        item = self.get(item_id)
        if not item:
            return False
        self._items.remove(item)
        return True


store = InventoryStore()

