"""
test_cryptocurrency.py This file tests the /cryptocurrency routes.
"""

import requests
from unittest import TestCase


class TestCryptoCurrencyEndpoints(TestCase):
    """
    This class tests the /cryptocurrency endpoints.
    """

    def test_get_latest_quotes(self):
        """
        This function tests the /cryptocurrency/quotes/latest endpoint.
        :return:
        """

        # Make the request.
        response = requests.get("http://127.0.0.1:8000/cryptocurrency/quotes/latest?symbol=BTC&symbol=ETH")

        # Assert the response.
        self.assertEqual(response.status_code, 200)

    def test_get_info(self):
        """
        This function tests the /cryptocurrency/info endpoint.
        :return:
        """

        # Make the request.
        response = requests.get("http://127.0.0.1:8000/cryptocurrency/info?symbol=BTC&symbol=ETH&aux=logo")

        import pprint
        pprint.pprint(response.json())

        # Assert the response.
        self.assertEqual(response.status_code, 200)
