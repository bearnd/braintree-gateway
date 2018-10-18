# coding=utf-8

"""
This module defines unit-tests for the `ResourceCustomer` class.
"""

import json
import unittest.mock

import braintree.exceptions
import falcon.testing

from tests.base import TestBase
from tests import fixtures


class TestResourceCustomer(TestBase):
    """Tests the `ResourceCustomer` class."""

    def test_get(self):
        """Tests the `on_get` method."""

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.find",
            new=staticmethod(lambda customer_id: fixtures.customer),
        ):
            response = self.simulate_get(
                path="/customer/{}".format(fixtures.CUSTOMER_ID),
                headers=self.generate_jwt_headers(),
            )  # type: falcon.testing.Result

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 200)

        # Assert that the customer's details match the provided parameters.
        self.assertEqual(response.json["id"], fixtures.CUSTOMER_ID)
        self.assertEqual(response.json["email"], fixtures.CUSTOMER_EMAIL)

    def test_get_404(self):
        """Tests the `on_get` method simulating a 404 response."""

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.find",
            side_effect=braintree.exceptions.NotFoundError,
        ):
            response = self.simulate_get(
                path="/customer/{}".format(fixtures.CUSTOMER_ID),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        """ Tests the `on_post` method."""

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.create",
            new=staticmethod(lambda params: fixtures.result_customer_success),
        ):
            response = self.simulate_post(
                path="/customer",
                body=json.dumps({
                    "customer_id": fixtures.CUSTOMER_ID,
                    "email": fixtures.CUSTOMER_EMAIL,
                }),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 201)

        # Assert that the customer's details match the provided parameters.
        self.assertEqual(response.json["id"], fixtures.CUSTOMER_ID)
        self.assertEqual(response.json["email"], fixtures.CUSTOMER_EMAIL)

    def test_post_409(self):
        """ Tests the `on_post` method simulating a 409 response."""

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.create",
            new=staticmethod(lambda params: fixtures.result_failure),
        ):
            response = self.simulate_post(
                path="/customer",
                body=json.dumps({
                    "customer_id": fixtures.CUSTOMER_ID,
                    "email": fixtures.CUSTOMER_EMAIL,
                }),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 409.
        self.assertEqual(response.status_code, 409)

    def test_delete(self):
        """Tests the `on_delete` method."""

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.delete",
            new=staticmethod(lambda customer_id: fixtures.result_success),
        ):
            response = self.simulate_delete(
                path="/customer/{}".format(fixtures.CUSTOMER_ID),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 204)

    def test_delete_404(self):
        """ Tests the `on_delete` method simulating a 404 response."""

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.delete",
            side_effect=braintree.exceptions.NotFoundError,
        ):
            response = self.simulate_delete(
                path="/customer/{}".format(fixtures.CUSTOMER_ID),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)

    def test_delete_409(self):
        """ Tests the `on_delete` method simulating a 409 response."""

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.delete",
            new=staticmethod(lambda customer_id: fixtures.result_failure),
        ):
            response = self.simulate_delete(
                path="/customer/{}".format(fixtures.CUSTOMER_ID),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 409.
        self.assertEqual(response.status_code, 409)
