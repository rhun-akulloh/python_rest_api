import requests

BASE_URL = "https://world.openfoodfacts.org"
TIMEOUT = 10



def normalize(product):
    # format the data that external API returns to match our internal inventory items
    out = {}
    out["product_name"] = product.get("product_name") or None
    out["brand"] = product.get("brands") or None
    out["barcode"] = product.get("code") or None
    out["category"] = product.get("categories") or None
    out["ingredients_text"] = product.get("ingredients_text") or None
    return out


def fetch_by_barcode(barcode):
    url = BASE_URL + "/api/v2/product/" + str(barcode) + ".json"
    
    response = requests.get(url, timeout=TIMEOUT)
    if response.status_code != 200:
        return None
    else:
        data = response.json()
        product = data.get("product")
        if not product:
            return None
        return normalize(product)


def search_by_name(name):
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }
    finalUrl= f"{BASE_URL}/cgi/search.pl"

    response = requests.get(finalUrl, params=params, timeout=TIMEOUT)
    if response.status_code != 200:
        return None
    else:
        data = response.json()
        products = data.get("products")
        if not products:
            return None
        product = products[0]
        return normalize(product)
