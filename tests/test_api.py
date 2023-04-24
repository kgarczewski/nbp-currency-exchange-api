import pytest
from flask_testing import TestCase
from app.api import app
from app.currency_rate import get_avg_rate
from app.utils import currencies


class TestCurrencyExchangeAPI(TestCase):
    def create_app(self):
        return app

    def test_get_avg_exchange_rate(self):
        # Test valid request
        currency = "usd"
        date = "2023-04-21"
        response = self.client.get(f"/exchanges/{currency}/{date}")

        assert response.status_code == 200
        json_data = response.json
        assert json_data["currency"] == currency.upper()
        assert json_data["date"] == date

        # You can either mock the `get_avg_rate` function or use a specific date
        # with a known exchange rate for testing purposes
        assert json_data["average_exchange_rate"] == get_avg_rate(currency, date)

        # Test invalid currency
        invalid_currency = "invalid"
        response = self.client.get(f"/exchanges/{invalid_currency}/{date}")

        assert response.status_code == 400
        expected_error = (
            f"Invalid currency {invalid_currency}, must be one of {currencies}."
        )
        assert response.json["error"] == expected_error

        # Test invalid date
        invalid_date = "invalid"
        response = self.client.get(f"/exchanges/{currency}/{invalid_date}")

        assert response.status_code == 400
        assert response.json["error"] == "Invalid date format, should be YYYY-MM-DD."

    def test_max_and_min_average(self):
        # Test valid request
        currency = "usd"
        quotations = 5
        response = self.client.get(f"/averages/{currency}/{quotations}")

        assert response.status_code == 200
        json_data = response.json
        assert json_data["currency"] == currency.upper()
        assert json_data["quotations"] == quotations
        assert "min_average" in json_data
        assert "max_average" in json_data

        # Test invalid quotations
        invalid_quotations = 0
        response = self.client.get(f"/averages/{currency}/{invalid_quotations}")

        assert response.status_code == 400
        assert (
            response.json["error"]
            == "Invalid number of quotations, should be between 1 and 255 inclusive."
        )

        # Test invalid currency
        invalid_currency = "invalid"
        response = self.client.get(f"/averages/{invalid_currency}/{quotations}")

        assert response.status_code == 400
        expected_error = (
            f"Invalid currency {invalid_currency}, must be one of {currencies}."
        )
        assert response.json["error"] == expected_error

    def test_major_difference_buy_ask(self):
        # Test valid request
        currency = "usd"
        quotations = 5
        response = self.client.get(f"/buy-ask-rate/{currency}/{quotations}")

        assert response.status_code == 200
        json_data = response.json
        assert json_data["currency"] == currency.upper()
        assert json_data["quotations"] == quotations
        assert "major difference" in json_data

        # Test invalid currency
        invalid_currency = "invalid"
        response = self.client.get(f"/buy-ask-rate/{invalid_currency}/{quotations}")

        assert response.status_code == 400
        expected_error = (
            f"Invalid currency {invalid_currency}, must be one of {currencies}."
        )
        assert response.json["error"] == expected_error


@pytest.fixture
def test_client():
    with app.test_client() as testing_client:
        yield testing_client


if __name__ == "__main__":
    pytest.main(["-v", "test_api.py"])
