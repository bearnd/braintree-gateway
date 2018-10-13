# coding=utf-8

"""
This module defines unit-tests for the `ResourceCustomer` class.
"""

import json
import uuid

from tests.base import TestBase


class TestResourceCustomer(TestBase):
    """Tests the `ResourceCustomer` class."""

    def test_get(self):
        """ Tests the `on_get` method by creating a new customer via the gateway
            and retrieving that customer via the API."""

        # Create a new customer via the Braintree gateway.
        customer_id = uuid.uuid4().hex
        email = "fake@email.com"
        result = self.gateway.customer.create(params={
            "id": customer_id,
            "email": email,
        })

        # Assert that the customer was created.
        self.assertTrue(result.is_success)

        # Retrieve the newly created customer via the API.
        response = self.simulate_get("/customer/{}".format(customer_id))

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 200)

        # Assert that the customer's details match the provided parameters.
        self.assertEqual(response.json["customer_id"], result.customer.id)
        self.assertEqual(response.json["email"], result.customer.email)

        # Delete the customer via the gateway to minimize sandbox contamination.
        result = self.gateway.customer.delete(customer_id=customer_id)

        # Assert that the customer was deleted.
        self.assertTrue(result.is_success)

    def test_get_404(self):
        """ Tests the `on_get` method by retrieving a non-existent customer."""

        customer_id = uuid.uuid4().hex

        # Retrieve a non-existent customer via the API.
        response = self.simulate_get("/customer/{}".format(customer_id))

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        """ Tests the `on_post` method by creating a new customer via the
            API.
        """

        # Create a new customer via the Braintree API.
        customer_id = uuid.uuid4().hex
        email = "fake@email.com"
        response = self.simulate_post(
            path="/customer",
            body=json.dumps({
                "customer_id": customer_id,
                "email": email,
            }),
        )

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 201)

        # Assert that the customer's details match the provided parameters.
        self.assertEqual(response.json["customer_id"], customer_id)
        self.assertEqual(response.json["email"], email)

        # Delete the customer via the gateway to minimize sandbox contamination.
        result = self.gateway.customer.delete(customer_id=customer_id)

        # Assert that the customer was deleted.
        self.assertTrue(result.is_success)

    def test_post_409(self):
        """ Tests the `on_post` method by creating a duplicate customer via the
            API.
        """

        # Create a new customer via the Braintree gateway.
        customer_id = uuid.uuid4().hex
        email = "fake@email.com"
        response = self.simulate_post(
            path="/customer",
            body=json.dumps({
                "customer_id": customer_id,
                "email": email,
            }),
        )

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 201)

        # Assert that the customer's details match the provided parameters.
        self.assertEqual(response.json["customer_id"], customer_id)
        self.assertEqual(response.json["email"], email)

        # Attempt to create a duplicate of the customer.
        response = self.simulate_post(
            path="/customer",
            body=json.dumps({
                "customer_id": customer_id,
                "email": email,
            }),
        )

        # Assert that the request failed with a 409.
        self.assertEqual(response.status_code, 409)

        # Delete the customer via the gateway to minimize sandbox contamination.
        result = self.gateway.customer.delete(customer_id=customer_id)

        # Assert that the customer was deleted.
        self.assertTrue(result.is_success)

    def test_delete(self):
        """ Tests the `on_delete` method by creating a new customer via the
            gateway and deleting that customer via the API."""

        # Create a new customer via the Braintree gateway.
        customer_id = uuid.uuid4().hex
        email = "fake@email.com"
        result = self.gateway.customer.create(params={
            "id": customer_id,
            "email": email,
        })

        # Assert that the customer was created.
        self.assertTrue(result.is_success)

        # Delete the newly created customer via the API.
        response = self.simulate_delete("/customer/{}".format(customer_id))

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 204)

    def test_delete_404(self):
        """ Tests the `on_delete` method by deleting a non-existent customer."""

        customer_id = uuid.uuid4().hex

        # Delete a non-existent customer via the API.
        response = self.simulate_delete("/customer/{}".format(customer_id))

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)
