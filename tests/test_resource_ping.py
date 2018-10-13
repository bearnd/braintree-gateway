# coding=utf-8

"""
This module defines unit-tests for the `ResourcePing` class.
"""

from tests.base import TestBase


class TestResourcePing(TestBase):
    """Tests the `ResourcePing` class."""

    def test_get(self):
        """ Tests the `on_get` method by pinging the service and retrieving its
            status.
        """

        response = self.simulate_get('/ping')

        result_refr = {
            "status": "OK"
        }

        self.assertEqual(response.json, result_refr)
