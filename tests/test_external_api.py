from unittest.mock import Mock, patch

import pytest
import requests

from app.external_api import ExternalAPIError, fetch_by_barcode


def test_fetch_by_barcode_found_not_found_and_error():
    with patch("app.external_api.requests.get") as mock_get:
        mock_get.return_value = Mock(
            json=lambda: {
                "status": 1,
                "product": {"product_name": "Nutella", "brands": "Ferrero", "code": "123"},
            }
        )
        result = fetch_by_barcode("123")
        assert result["product_name"] == "Nutella"

        mock_get.return_value = Mock(json=lambda: {"status": 0})
        assert fetch_by_barcode("000") is None

        mock_get.side_effect = requests.RequestException("boom")
        with pytest.raises(ExternalAPIError):
            fetch_by_barcode("123")
