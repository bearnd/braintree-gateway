# coding=utf-8

"""
This module defines unit-tests for the `ResourceSubscription` class.
"""

import uuid
import json

from tests.base import TestBase


class TestResourceSubscription(TestBase):
    """Tests the `ResourceSubscription` class."""

    def test_get(self):
        """ Tests the `on_get` method by creating a new subscription via the
            gateway and retrieving that subscription via the API."""

        # Create a new customer via the Braintree gateway.
        customer_id = uuid.uuid4().hex
        email = "fake@email.com"
        result = self.gateway.customer.create(params={
            "id": customer_id,
            "email": email,
        })

        # Assert that the customer was created.
        self.assertTrue(result.is_success)

        # Create a new payment-method for the customer via the Braintree
        # gateway.
        payment_method_nonce = "fake-valid-visa-nonce"
        result = self.gateway.payment_method.create(params={
            "customer_id": customer_id,
            "payment_method_nonce": payment_method_nonce,
        })

        # Assert that the payment-method was created.
        self.assertTrue(result.is_success)

        # Create a new subscription via the Braintree gateway.
        plan_id = "test"
        result = self.gateway.subscription.create(params={
            "payment_method_token": result.payment_method.token,
            "plan_id": plan_id,
        })

        # Assert that the payment-method was created.
        self.assertTrue(result.is_success)

        # Retrieve the newly created subscription's ID.
        subscription_id = result.subscription.id

        # Retrieve the newly created subscription via the API.
        response = self.simulate_get("/subscription/{}".format(
            subscription_id,
        ))

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 200)

        # Assert that the subscriptions's details match the provided parameters.
        self.assertEqual(response.json["subscription_id"], subscription_id)
        self.assertEqual(response.json["plan_id"], plan_id)
        self.assertEqual(response.json["status"], "Active")
        self.assertEqual(response.json["balance"], "0.00")

        # Delete the customer via the gateway to minimize sandbox contamination.
        # This deletion will cancel the subscription and delete the payment
        # method.
        result = self.gateway.customer.delete(customer_id=customer_id)

        # Assert that the customer was deleted.
        self.assertTrue(result.is_success)

    def test_get_404(self):
        """ Tests the `on_get` method by retrieving a non-existent
            subscription.
        """

        subscription_id = uuid.uuid4().hex

        # Retrieve a non-existent subscription via the API.
        response = self.simulate_get("/subscription/{}".format(subscription_id))

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)

    def test_post(self):
        """ Tests the `on_post` method by creating a new subscription via the
            API.
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

        # Create a new subscription via the Braintree API.
        plan_id = "test"
        response = self.simulate_post(
            path="/subscription",
            body=json.dumps({
                "payment_method_nonce": "fake-valid-amex-nonce",
                "customer_id": customer_id,
                "plan_id": plan_id,
            }),
        )

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 201)

        # Assert that the subscriptions's details match the provided parameters.
        self.assertEqual(response.json["plan_id"], plan_id)
        self.assertEqual(response.json["status"], "Active")
        self.assertEqual(response.json["balance"], "0.00")

        # Delete the customer via the gateway to minimize sandbox contamination.
        # This deletion will cancel the subscription and delete the payment
        # method.
        result = self.gateway.customer.delete(customer_id=customer_id)

        # Assert that the customer was deleted.
        self.assertTrue(result.is_success)

    def test_post_404_customer(self):
        """ Tests the `on_post` method by creating a new subscription via the
            API when the defined customer is non-existent.
        """

        # Create a new customer via the Braintree gateway.
        customer_id = uuid.uuid4().hex
        # Create a new subscription via the Braintree API.
        plan_id = "test"
        response = self.simulate_post(
            path="/subscription",
            body=json.dumps({
                "payment_method_nonce": "fake-valid-nonce",
                "customer_id": customer_id,
                "plan_id": plan_id,
            }),
        )

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)

    def test_delete(self):
        """ Tests the `on_delete` method by creating a new subscription via the
            gateway and deleting that subscription via the API."""

        # Create a new customer via the Braintree gateway.
        customer_id = uuid.uuid4().hex
        email = "fake@email.com"
        result = self.gateway.customer.create(params={
            "id": customer_id,
            "email": email,
        })

        # Assert that the customer was created.
        self.assertTrue(result.is_success)

        # Create a new payment-method for the customer via the Braintree
        # gateway.
        payment_method_nonce = "fake-valid-mastercard-nonce"
        result = self.gateway.payment_method.create(params={
            "customer_id": customer_id,
            "payment_method_nonce": payment_method_nonce,
        })

        # Assert that the payment-method was created.
        self.assertTrue(result.is_success)

        # Create a new subscription via the Braintree gateway.
        plan_id = "test"
        result = self.gateway.subscription.create(params={
            "payment_method_token": result.payment_method.token,
            "plan_id": plan_id,
        })

        # Assert that the payment-method was created.
        self.assertTrue(result.is_success)

        # Retrieve the newly created subscription's ID.
        subscription_id = result.subscription.id

        # Delete the newly created subscription via the API.
        response = self.simulate_delete("/subscription/{}".format(
            subscription_id,
        ))

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 204)

        # Delete the customer via the gateway to minimize sandbox contamination.
        # This deletion will cancel the subscription and delete the payment
        # method.
        result = self.gateway.customer.delete(customer_id=customer_id)

        # Assert that the customer was deleted.
        self.assertTrue(result.is_success)

    def test_delete_404(self):
        """ Tests the `on_delete` method by deleting a non-existent
            subscription.
        """

        subscription_id = uuid.uuid4().hex

        # Delete a non-existent subscription via the API.
        response = self.simulate_delete(
            "/subscription/{}".format(subscription_id),
        )

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)
