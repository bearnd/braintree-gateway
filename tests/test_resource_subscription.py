# coding=utf-8

"""
This module defines unit-tests for the `ResourceSubscription` class.
"""

import decimal
import json
import unittest.mock

import braintree.exceptions
import falcon.testing

from tests.base import TestBase
from tests import fixtures


class TestResourceSubscription(TestBase):
    """ Tests the `ResourceSubscription` class."""

    def test_get(self):
        """ Tests the `on_get` method."""

        with unittest.mock.patch(
            target="braintree.subscription_gateway.SubscriptionGateway.find",
            new=staticmethod(lambda subscription_id: fixtures.subscription),
        ):
            response = self.simulate_get(
                path="/customer/{}/subscription/{}".format(
                    fixtures.CUSTOMER_ID,
                    fixtures.SUBSCRIPTION_ID,
                ),
                headers=self.generate_jwt_headers(),
            )  # type: falcon.testing.Result

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 200)

        # Assert that the subscriptions's details match the provided parameters.
        self.assertEqual(response.json["id"], fixtures.SUBSCRIPTION_ID)
        self.assertEqual(response.json["plan_id"], fixtures.PLAN_ID)
        self.assertEqual(response.json["status"], fixtures.SUBSCRIPTION_STATUS)
        self.assertEqual(
            decimal.Decimal(response.json["balance"]),
            fixtures.SUBSCRIPTION_BALANCE,
        )

    def test_get_404(self):
        """ Tests the `on_get` method simulating a 404 response."""

        with unittest.mock.patch(
            target="braintree.subscription_gateway.SubscriptionGateway.find",
            side_effect=braintree.exceptions.NotFoundError,
        ):
            response = self.simulate_get(
                path="/customer/{}/subscription/{}".format(
                    fixtures.CUSTOMER_ID,
                    fixtures.SUBSCRIPTION_ID,
                ),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)

    @unittest.mock.patch(
        target="braintree.customer_gateway.CustomerGateway.find",
        new=staticmethod(lambda customer_id: fixtures.customer),
    )
    @unittest.mock.patch(
        target="braintree.payment_method_gateway.PaymentMethodGateway.create",
        new=staticmethod(lambda params: fixtures.result_payment_method_success),
    )
    def test_post(self):
        """ Tests the `on_post` method."""

        with unittest.mock.patch(
            target="braintree.subscription_gateway.SubscriptionGateway.create",
            new=staticmethod(
                lambda params: fixtures.result_subscription_success
            ),
        ):
            response = self.simulate_post(
                path="/customer/{}/subscription".format(fixtures.CUSTOMER_ID),
                body=json.dumps({
                    "payment_method_nonce": fixtures.PAYMENT_METHOD_NONCE,
                    "customer_id": fixtures.CUSTOMER_ID,
                    "plan_id": fixtures.PLAN_ID,
                }),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 201)

        # Assert that the subscriptions's details match the provided parameters.
        self.assertEqual(response.json["plan_id"], fixtures.PLAN_ID)
        self.assertEqual(response.json["status"], fixtures.SUBSCRIPTION_STATUS)
        self.assertEqual(
            decimal.Decimal(response.json["balance"]),
            fixtures.SUBSCRIPTION_BALANCE,
        )

    def test_post_404_customer(self):
        """ Tests the `on_post` method simulating a 404 response on customer
            retrieval.
        """

        with unittest.mock.patch(
            target="braintree.customer_gateway.CustomerGateway.find",
            side_effect=braintree.exceptions.NotFoundError,
        ):
            response = self.simulate_post(
                path="/customer/{}/subscription".format(fixtures.CUSTOMER_ID),
                body=json.dumps({
                    "payment_method_nonce": fixtures.PAYMENT_METHOD_NONCE,
                    "customer_id": fixtures.CUSTOMER_ID,
                    "plan_id": fixtures.PLAN_ID,
                }),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)

    @unittest.mock.patch(
        target="braintree.customer_gateway.CustomerGateway.find",
        new=staticmethod(lambda customer_id: fixtures.customer),
    )
    @unittest.mock.patch(
        target="braintree.payment_method_gateway.PaymentMethodGateway.create",
        new=staticmethod(lambda params: fixtures.result_payment_method_failure),
    )
    def test_post_409_payment_method(self):
        """ Tests the `on_post` method simulating a 409 response on the
            payment method creation.
        """

        response = self.simulate_post(
            path="/customer/{}/subscription".format(fixtures.CUSTOMER_ID),
            body=json.dumps({
                "payment_method_nonce": fixtures.PAYMENT_METHOD_NONCE,
                "customer_id": fixtures.CUSTOMER_ID,
                "plan_id": fixtures.PLAN_ID,
            }),
            headers=self.generate_jwt_headers(),
        )

        # Assert that the request failed with a 409.
        self.assertEqual(response.status_code, 409)

    @unittest.mock.patch(
        target="braintree.customer_gateway.CustomerGateway.find",
        new=staticmethod(lambda customer_id: fixtures.customer),
    )
    @unittest.mock.patch(
        target="braintree.payment_method_gateway.PaymentMethodGateway.create",
        new=staticmethod(lambda params: fixtures.result_payment_method_success),
    )
    def test_post_409_subscription(self):
        """ Tests the `on_post` method simulating a 409 response on the
            subscription creation.
        """

        with unittest.mock.patch(
            target="braintree.subscription_gateway.SubscriptionGateway.create",
            new=staticmethod(
                lambda params: fixtures.result_subscription_failure
            ),
        ):
            response = self.simulate_post(
                path="/customer/{}/subscription".format(fixtures.CUSTOMER_ID),
                body=json.dumps({
                    "payment_method_nonce": fixtures.PAYMENT_METHOD_NONCE,
                    "customer_id": fixtures.CUSTOMER_ID,
                    "plan_id": fixtures.PLAN_ID,
                }),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 409.
        self.assertEqual(response.status_code, 409)

    def test_delete(self):
        """ Tests the `on_delete` method."""

        with unittest.mock.patch(
            target="braintree.subscription_gateway.SubscriptionGateway.cancel",
            new=staticmethod(lambda subscription_id: fixtures.result_success),
        ):
            response = self.simulate_delete(
                path="/customer/{}/subscription/{}".format(
                    fixtures.CUSTOMER_ID,
                    fixtures.SUBSCRIPTION_ID,
                ),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request was successful.
        self.assertEqual(response.status_code, 204)

    def test_delete_404(self):
        """ Tests the `on_delete` method simulating a 404 response."""

        with unittest.mock.patch(
            target="braintree.subscription_gateway.SubscriptionGateway.cancel",
            side_effect=braintree.exceptions.NotFoundError,
        ):
            response = self.simulate_delete(
                path="/customer/{}/subscription/{}".format(
                    fixtures.CUSTOMER_ID,
                    fixtures.SUBSCRIPTION_ID,
                ),
                headers=self.generate_jwt_headers(),
            )

        # Assert that the request failed with a 404.
        self.assertEqual(response.status_code, 404)
