import random
import unittest
from app.utils import validate_currency, validate_date, validate_currency_quotes
from app.api import currencies
import datetime


class TestInputValidations(unittest.TestCase):
    def test_valid_currencies(self):
        valid_currencies = currencies

        for currency in valid_currencies:
            result = validate_currency(currency, currencies)
            self.assertIsNone(result)

    def test_invalid_currencies(self):
        invalid_currencies = ["INVALID", "abc", "123"]

        for currency in invalid_currencies:
            result = validate_currency(currency, currencies)
            self.assertIsNotNone(result)
            self.assertIn(currency, result)

    def test_case_insensitive(self):
        valid_currency = "usd"
        result = validate_currency(valid_currency, currencies)
        self.assertIsNone(result)

    def test_validate_date(self):
        # Test valid date
        valid_date = (datetime.datetime.today() - datetime.timedelta(days=3)).strftime(
            "%Y-%m-%d"
        )
        self.assertIsNone(validate_date(valid_date))

        # Test invalid date format
        invalid_date_format = "2023-13-32"
        self.assertEqual(
            validate_date(invalid_date_format),
            "Invalid date format, should be YYYY-MM-DD.",
        )

        # Test weekend date
        weekend_date = "2023-04-22"  # Assuming it's a Saturday
        self.assertEqual(
            validate_date(weekend_date), "Invalid date, should be a weekday."
        )

        # Test future date
        future_date = (
            datetime.datetime.today() + datetime.timedelta(days=10)
        ).strftime("%Y-%m-%d")
        self.assertEqual(
            validate_date(future_date), "Invalid date, should be a past date."
        )

    def test_validate_currency_quotations(self):
        # Test valid quotations
        valid_quotations = random.randint(1, 255)
        self.assertIsNone(validate_currency_quotes(valid_quotations))

        # Test invalid quotations
        invalid_quotations = ["INVALID", "123", 265]
        for quotation in invalid_quotations:
            result = validate_currency_quotes(quotation)
            self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
