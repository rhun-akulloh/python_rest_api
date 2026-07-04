from unittest.mock import Mock, patch

from click.testing import CliRunner

from cli.main import cli


def test_cli_list_add_and_error():
    runner = CliRunner()
    with patch("cli.main.requests.request") as mock_request:
        mock_request.return_value = Mock(
            status_code=200,
            json=lambda: [
                {"id": 1, "product_name": "Widget", "brand": "Acme", "price": 1.0, "quantity": 2}
            ],
        )
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "Widget" in result.output

        mock_request.return_value = Mock(status_code=201, json=lambda: {"id": 2})
        result = runner.invoke(
            cli, ["add", "--name", "New Item", "--price", "3", "--quantity", "1"]
        )
        assert result.exit_code == 0
        assert "Created item 2" in result.output

        mock_request.return_value = Mock(
            status_code=404, json=lambda: {"error": "item not found"}
        )
        result = runner.invoke(cli, ["get", "999"])
        assert result.exit_code != 0
        assert "item not found" in result.output
