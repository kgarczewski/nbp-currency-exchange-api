import unittest

from app.currency_rate import (
    get_avg_rate,
    get_max_buy_sell_diff,
    get_max_and_min_average_rate,
)
import pytest
import requests_mock


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
        with requests_mock.Mocker() as m:
            m.get("http://api.nbp.pl/api/exchangerates/rates/a/USD/last/10/",
                  json={"rates": [{"mid": 1.10}, {"mid": 1.15}, {"mid": 1.20}, {"mid": 1.18}, {"mid": 1.22},
                                  {"mid": 1.25}, {"mid": 1.30}, {"mid": 1.28}, {"mid": 1.24}, {"mid": 1.32}]})

            # Test case 1: Valid inputs
            min_mid, max_mid = get_max_and_min_average_rate("USD", 10)
            self.assertEqual(min_mid, 1.10)
            self.assertEqual(max_mid, 1.32)

            # Test case 2: Invalid n value
            result = get_max_and_min_average_rate("USD", 256)
            self.assertEqual(result, (
            None, None, {"error": "Invalid value for n: n must be a positive integer less than or equal to 255."}))

    def test_get_max_buy_sell_diff(self):
        with requests_mock.Mocker() as m:
            m.get("http://api.nbp.pl/api/exchangerates/rates/c/USD/last/5/",
                  json={"rates": [{"ask": 1.20, "bid": 1.15}, {"ask": 1.25, "bid": 1.20}, {"ask": 1.22, "bid": 1.18},
                                  {"ask": 1.28, "bid": 1.22}, {"ask": 1.35, "bid": 1.30}]})

            # Test case 1: Valid inputs
            max_difference = get_max_buy_sell_diff("USD", 5)
            self.assertEqual(max_difference, 0.06)

            # Test case 2: No rates found
            with self.assertRaises(Exception):
                with requests_mock.Mocker() as m:
                    m.get("http://api.nbp.pl/api/exchangerates/rates/c/FAKE/last/5/", json={"rates": []})
                    get_max_buy_sell_diff("FAKE", 5)
