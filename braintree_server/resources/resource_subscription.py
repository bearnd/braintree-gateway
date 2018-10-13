# coding=utf-8

import falcon
import marshmallow.validate
import braintree.exceptions

from braintree_server.resources.base import ResourceBase


class SchemaSubscriptionPostRequest(marshmallow.Schema):
    """Braintree customer schema used in POST requests."""

    payment_method_nonce = marshmallow.fields.String(required=True)
    customer_id = marshmallow.fields.String(required=True)
    plan_id = marshmallow.fields.String(required=True)

    class Meta:
        strict = True


class SchemaSubscriptionResponse(marshmallow.Schema):
    """Braintree subscription schema used in responses."""

    subscription_id = marshmallow.fields.String(required=True)
    plan_id = marshmallow.fields.String(required=True)
    status = marshmallow.fields.String(
        required=True,
        validate=marshmallow.validate.OneOf(choices=[
            "Active",
            "Canceled",
            "Expired",
            "Past Due",
            "Pending",
        ])
    )
    balance = marshmallow.fields.Decimal(required=False, as_string=True)
    billing_day_of_month = marshmallow.fields.Integer(required=False)
    created_at = marshmallow.fields.DateTime(required=False)
    updated_at = marshmallow.fields.DateTime(required=False)

    class Meta:
        strict = True


class ResourceSubscription(ResourceBase):
    """ Resource-class to manage Braintree subscriptions."""

    schema_post_request = SchemaSubscriptionPostRequest()
    schema_response = SchemaSubscriptionResponse()

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        subscription_id: str,
    ):
        """ Retrieves an existing Braintree subscription via their ID.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
            subscription_id (str): The Braintree subscription ID for which
                retrieval will be performed.
        """

        msg = "Retrieving subscription with ID '{}'."
        msg_fmt = msg.format(subscription_id)
        self.logger.info(msg_fmt)

        # Retrieve subscription or respond with a 404 if no subscription was
        # found for the given ID.
        try:
            subscription = self.gateway.subscription.find(
                subscription_id=subscription_id,
            )
        except braintree.exceptions.NotFoundError as exc:
            msg = "Subscription with ID '{}' not found."
            msg_fmt = msg.format(subscription_id)
            self.logger.exception(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_404,
                title="Not found.",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )

        result = {
            "subscription_id": subscription.id,
            "plan_id": subscription.plan_id,
            "status": subscription.status,
            "balance": subscription.balance,
            "billing_day_of_month": subscription.billing_day_of_month,
            "created_at": subscription.created_at,
            "updated_at": subscription.updated_at,
        }

        resp = self.prepare_response(
            resp=resp,
            result=result,
            schema=self.schema_response,
        )
        resp.status = falcon.HTTP_200

    def on_post(
        self,
        req: falcon.Request,
        resp: falcon.Response,
    ):
        """ Creates a new Braintree payment-method and subscription to a given
            plan.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
        """

        parameters = self.get_parameters(
            req=req,
            schema=self.schema_post_request,
        )

        # Retrieve the customer ID.
        customer_id = parameters["customer_id"]

        msg = "Creating subscription for customer with ID '{}'."
        msg_fmt = msg.format(customer_id)
        self.logger.info(msg_fmt)

        # Retrieve customer or respond with a 404 if no customer was found for
        # the given ID.
        try:
            self.gateway.customer.find(customer_id=customer_id)
        except braintree.exceptions.NotFoundError as exc:
            msg_fmt = "Customer with ID '{}' not found.".format(customer_id)
            self.logger.exception(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_404,
                title="Not found.",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )

        # Create a new default payment-method under the customer.
        pm_result = self.gateway.payment_method.create(params={
            "customer_id": customer_id,
            "payment_method_nonce": parameters["payment_method_nonce"],
            "options": {
                "make_default": True,
            },
        })

        # Respond with a 409 if the payment-method could not be created.
        if not pm_result.is_success:
            msg = ("Could not create payment-method for customer with ID "
                   "'{}': {}")
            msg_fmt = msg.format(customer_id, pm_result.message)
            self.logger.error(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_409,
                title="Could not create.",
                description=msg_fmt,
            )

        # Create a new subscription.
        result = self.gateway.subscription.create(params={
            "payment_method_token": pm_result.payment_method.token,
            "plan_id": parameters["plan_id"],
        })

        # Respond with a 409 if the subscription could not be created.
        if not result.is_success:
            msg = "Could not create subscription for customer with ID '{}': {}"
            msg_fmt = msg.format(customer_id, result.message)
            self.logger.error(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_409,
                title="Could not create.",
                description=msg_fmt,
            )

        result = {
            "subscription_id": result.subscription.id,
            "plan_id": result.subscription.plan_id,
            "status": result.subscription.status,
            "balance": result.subscription.balance,
            "billing_day_of_month": result.subscription.billing_day_of_month,
            "created_at": result.subscription.created_at,
            "updated_at": result.subscription.updated_at,
        }

        resp = self.prepare_response(
            resp=resp,
            result=result,
            schema=self.schema_response,
        )
        resp.status = falcon.HTTP_201

    def on_delete(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        subscription_id: str,
    ):
        """ Cancels a Braintree subscription.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
            subscription_id (str): The Braintree subscription ID for which
                cancellation will be performed.
        """

        msg = "Deleting subscription with ID '{}'."
        msg_fmt = msg.format(subscription_id)
        self.logger.info(msg_fmt)

        # Cancel subscription or respond with a 404 if no subscription was
        # found for the given ID.
        try:
            result = self.gateway.subscription.cancel(
                subscription_id=subscription_id,
            )
        except braintree.exceptions.NotFoundError as exc:
            msg = "Subscription with ID '{}' not found."
            msg_fmt = msg.format(subscription_id)
            self.logger.exception(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_404,
                title="Not found.",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )

        # Respond with a 409 if the subscription could not be cancelled.
        if not result.is_success:
            msg = "Could not cancel subscription with ID '{}': {}"
            msg_fmt = msg.format(subscription_id, result.message)
            self.logger.error(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_409,
                title="Could not cancel.",
                description=msg_fmt,
            )

        resp.status = falcon.HTTP_204
