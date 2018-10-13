# coding=utf-8

"""
This module defines unit-tests for the `ResourceClientToken` class.
"""

import uuid

from tests.base import TestBase


class TestResourceClientToken(TestBase):
    """Tests the `ResourceClientToken` class."""

    def test_get(self):
        """ Tests the `on_get` method by retrieving a client-token for a given
            customer.
        """

        # Create a new customer via the Braintree gateway.
        customer_id = uuid.uuid4().hex
        email = "fake@email.com"
        result = self.gateway.customer.create(params={
            "id": customer_id,
            "email": email,
        })

        # Assert that the customer was created.
        self.assertTrue(result.is_success)

        # Retrieve a client-token for the newly created customer via the API.
        response = self.simulate_get("/client-token/{}".format(customer_id))

        # Assert that a token was retrieved.
        self.assertIsNotNone(response.get("token"))
