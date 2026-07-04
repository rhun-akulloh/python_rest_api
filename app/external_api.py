import requests

BASE_URL = "https://world.openfoodfacts.org"
TIMEOUT = 10  # openfoodfacts can be slow, bumped this up from 5 after seeing timeouts locally
HEADERS = {'User-Agent': 'InventoryManagementSystem/1.0 (contact: adnanobuya@gmail.com)'}


class ExternalAPIError(Exception):
    pass


def _normalize(product):
    # off gives back a LOT more fields than we care about, just pulling what we need
    out = {}
    out["product_name"] = product.get("product_name") or None
    out["brand"] = product.get("brands") or None
    out["barcode"] = product.get("code") or None
    out["category"] = product.get("categories") or None
    out["ingredients_text"] = product.get("ingredients_text") or None
    return out


def fetch_by_barcode(barcode):
    url = BASE_URL + "/api/v2/product/" + str(barcode) + ".json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError("failed to reach OpenFoodFacts: %s" % exc) from exc

    data = response.json()
    if data.get("status") != 1:
        # status 0 just means not found, not really an error
        return None
    return _normalize(data["product"])


def search_by_name(name):
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }

    try:
        resp = requests.get(f"{BASE_URL}/cgi/search.pl", params=params, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError(f"OpenFoodFacts search failed: {exc}") from exc

    products = resp.json().get("products") or []
    if not products:
        return None
    return _normalize(products[0])
