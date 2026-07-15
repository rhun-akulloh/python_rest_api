from unittest.mock import Mock, patch

from app.external_api import fetch_by_barcode, search_by_name


def test_fetch_by_barcode_found():
    with patch("app.external_api.requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {
                "status": 1,
                "product": {"product_name": "Nutella", "brands": "Ferrero", "code": "123"},
            },
        )
        result = fetch_by_barcode("123")
        assert result["product_name"] == "Nutella"
        assert result["brand"] == "Ferrero"


def test_fetch_by_barcode_not_found():
    with patch("app.external_api.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: {"status": 0})
        assert fetch_by_barcode("000") is None


def test_fetch_by_barcode_http_error():
    with patch("app.external_api.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=403, json=lambda: {})
        assert fetch_by_barcode("123") is None


def test_search_by_name_found():
    with patch("app.external_api.requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: {"products": [{"product_name": "Nutella", "brands": "Ferrero"}]},
        )
        result = search_by_name("nutella")
        assert result["product_name"] == "Nutella"


def test_search_by_name_not_found():
    with patch("app.external_api.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: {"products": []})
        assert search_by_name("doesnotexist") is None
