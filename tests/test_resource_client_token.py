# coding=utf-8

"""
This module defines unit-tests for the `ResourceClientToken` class.
"""

import unittest.mock

import falcon.testing

from tests.base import TestBase
from tests import fixtures


class TestResourceClientToken(TestBase):
    """Tests the `ResourceClientToken` class."""

    def test_get(self):
        """ Tests the `on_get` method by retrieving a client-token for a given
            customer.
        """

        # Retrieve a client-token for the newly created customer via the API.
        with unittest.mock.patch(
            target="braintree.client_token_gateway.ClientTokenGateway.generate",
            new=staticmethod(lambda x: fixtures.CLIENT_TOKEN),
        ):
            response = self.simulate_get(
                path="/client-token/{}".format(fixtures.CUSTOMER_ID),
                headers=self.generate_jwt_headers(),
            )  # type: falcon.testing.Result

        # Assert that a token was retrieved.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("token"), fixtures.CLIENT_TOKEN)


class TestResourceClientTokenNoCustomerId(TestBase):
    """Tests the `ResourceClientTokenNoCustomerId` class."""

    def test_get(self):
        """ Tests the `on_get` method by retrieving a client-token without
            specifying a customer.
        """

        # Retrieve a client-token without specifying a customer via the API.
        with unittest.mock.patch(
            target="braintree.client_token_gateway.ClientTokenGateway.generate",
            new=staticmethod(lambda: fixtures.CLIENT_TOKEN),
        ):
            response = self.simulate_get(
                path="/client-token",
                headers=self.generate_jwt_headers(),
            )  # type: falcon.testing.Result

        # Assert that a token was retrieved.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("token"), fixtures.CLIENT_TOKEN)

    def test_get_401_missing(self):
        """ Tests the `on_get` method without an authorization header."""

        # Retrieve a client-token without specifying a customer via the API.
        with unittest.mock.patch(
            target="braintree.client_token_gateway.ClientTokenGateway.generate",
            new=staticmethod(lambda: fixtures.CLIENT_TOKEN),
        ):
            response = self.simulate_get(
                path="/client-token",
            )  # type: falcon.testing.Result

        # Assert that a token was retrieved.
        self.assertEqual(response.status_code, 401)

    def test_get_401_no_bearer(self):
        """ Tests the `on_get` method where the authorization header does
            not start with `Bearer`.
        """

        # Retrieve a client-token without specifying a customer via the API.
        with unittest.mock.patch(
            target="braintree.client_token_gateway.ClientTokenGateway.generate",
            new=staticmethod(lambda: fixtures.CLIENT_TOKEN),
        ):
            response = self.simulate_get(
                path="/client-token",
                headers={
                    "Authorization": self.token_generator.generate(),
                }
            )  # type: falcon.testing.Result

        # Assert that a token was retrieved.
        self.assertEqual(response.status_code, 401)

    def test_get_401_no_token(self):
        """ Tests the `on_get` method where the authorization header does
            not have a token.
        """

        # Retrieve a client-token without specifying a customer via the API.
        with unittest.mock.patch(
            target="braintree.client_token_gateway.ClientTokenGateway.generate",
            new=staticmethod(lambda: fixtures.CLIENT_TOKEN),
        ):
            response = self.simulate_get(
                path="/client-token",
                headers={
                    "Authorization": "Bearer",
                }
            )  # type: falcon.testing.Result

        # Assert that a token was retrieved.
        self.assertEqual(response.status_code, 401)

    def test_get_401_invalid_format(self):
        """ Tests the `on_get` method where the authorization header does
            not follow the 'Bearer <token>' format.
        """

        # Retrieve a client-token without specifying a customer via the API.
        with unittest.mock.patch(
            target="braintree.client_token_gateway.ClientTokenGateway.generate",
            new=staticmethod(lambda: fixtures.CLIENT_TOKEN),
        ):
            response = self.simulate_get(
                path="/client-token",
                headers={
                    "Authorization": "Bearer something something",
                }
            )  # type: falcon.testing.Result

        # Assert that a token was retrieved.
        self.assertEqual(response.status_code, 401)
