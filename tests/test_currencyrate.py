import unittest

from app.currency_rate import (
    get_avg_rate,
    get_max_buy_sell_diff,
    get_max_and_min_average_rate,
)
import pytest


class TestEndpoints(unittest.TestCase):
    def test_get_avg_rate(self):
        # Test a valid currency and date
        assert get_avg_rate("GBP", "2022-04-22") == 5.5327

        # Test an invalid currency
        with pytest.raises(
            Exception,
            match=r"Failed to fetch data from http://api.nbp.pl/api/exchangerates/rates/a/ABC/2022-04-22/: 404",
        ):
            get_avg_rate("ABC", "2022-04-22")

        # Test an invalid date
        with pytest.raises(
            Exception,
            match=r"Failed to fetch data from http://api.nbp.pl/api/exchangerates/rates/a/GBP/9999-99-99/: 404",
        ):
            get_avg_rate("GBP", "9999-99-99")

    def test_get_max_and_min_average_rate(self):
        # Test a valid currency and n (quotations)
        assert get_max_and_min_average_rate("GBP", 5) == (5.2086, 5.2529)

        # Test an invalid currency
        with pytest.raises(
            Exception,
            match=r"Failed to fetch data from http://api.nbp.pl/api/exchangerates/rates/a/ABC/last/5/: 404",
        ):
            get_max_and_min_average_rate("ABC", 5)

        # Test an invalid n (quotations)
        result = get_max_and_min_average_rate("GBP", 0)
        assert result == (
            None,
            None,
            {
                "error": "Invalid value for n: n must be a positive integer less than or equal to 255."
            },
        )

    def test_get_max_buy_sell_diff(self):
        # Test a valid currency and n (quotations)
        assert get_max_buy_sell_diff("GBP", 5) == 0.1048

        # Test an invalid currency
        with pytest.raises(
            Exception,
            match=r"Failed to fetch data from http://api.nbp.pl/api/exchangerates/rates/c/ABC/last/5/: 404",
        ):
            get_max_buy_sell_diff("ABC", 5)

        # Test an invalid n (quotations)
        with pytest.raises(
            Exception,
            match=r"Failed to fetch data from http://api.nbp.pl/api/exchangerates/rates/c/GBP/last/0/: 404",
        ):
            get_max_buy_sell_diff("GBP", 0)
