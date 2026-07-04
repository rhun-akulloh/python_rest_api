import requests

BASE_URL = "https://world.openfoodfacts.org"
TIMEOUT = 10
HEADERS = {"User-Agent": "InventoryManagementSystem/1.0 (contact: adnanobuya@gmail.com)"}


class ExternalAPIError(Exception):
    pass


def _normalize(product):
    return {
        "product_name": product.get("product_name") or None,
        "brand": product.get("brands") or None,
        "barcode": product.get("code") or None,
        "category": product.get("categories") or None,
        "ingredients_text": product.get("ingredients_text") or None,
    }


def fetch_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError(f"failed to reach OpenFoodFacts: {exc}") from exc

    data = response.json()
    if data.get("status") != 1:
        return None
    return _normalize(data["product"])


def search_by_name(name):
    url = f"{BASE_URL}/cgi/search.pl"
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1,
    }
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExternalAPIError(f"failed to reach OpenFoodFacts: {exc}") from exc

    data = response.json()
    products = data.get("products") or []
    if not products:
        return None
    return _normalize(products[0])
