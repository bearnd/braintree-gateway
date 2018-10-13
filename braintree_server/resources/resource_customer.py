# coding=utf-8

import falcon
import marshmallow
import braintree.exceptions

from braintree_server.resources.base import ResourceBase


class SchemaCustomerPostRequest(marshmallow.Schema):
    """Braintree customer schema used in POST requests."""

    customer_id = marshmallow.fields.String(required=True)
    email = marshmallow.fields.String(required=True)

    class Meta:
        strict = True


class SchemaCustomerResponse(marshmallow.Schema):
    """Braintree customer schema used in responses."""

    customer_id = marshmallow.fields.String(required=True)
    email = marshmallow.fields.String(required=True)
    created_at = marshmallow.fields.DateTime(required=False)
    updated_at = marshmallow.fields.DateTime(required=False)

    class Meta:
        strict = True


class ResourceCustomer(ResourceBase):
    """Resource-class to manage Braintree customers."""

    schema_post_request = SchemaCustomerPostRequest()
    schema_response = SchemaCustomerResponse()

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        customer_id: str,
    ):
        """ Retrieves an existing Braintree customer via their ID.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
            customer_id (str): The Braintree customer ID for which retrieval
                will be performed.
        """

        msg = "Retrieving customer with ID '{}'."
        msg_fmt = msg.format(customer_id)
        self.logger.info(msg_fmt)

        # Retrieve customer or respond with a 404 if no customer was found for
        # the given ID.
        try:
            customer = self.gateway.customer.find(customer_id=customer_id)
        except braintree.exceptions.NotFoundError as exc:
            msg_fmt = "Customer with ID '{}' not found.".format(customer_id)
            self.logger.exception(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_404,
                title="Not found.",
                description=msg_fmt,
            )

        result = {
            "customer_id": customer.id,
            "email": customer.email,
            "created_at": customer.created_at,
            "updated_at": customer.updated_at,
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
        """Creates a new Braintree customer.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
        """

        parameters = self.get_parameters(
            req=req,
            schema=self.schema_post_request,
        )

        # Retrieve defined customer ID.
        customer_id = parameters["customer_id"]

        msg = "Creating customer with ID '{}'."
        msg_fmt = msg.format(customer_id)
        self.logger.info(msg_fmt)

        # Create a new customer.
        result = self.gateway.customer.create(params={
            "id": customer_id,
            "email": parameters["email"],
        })

        # Respond with a 409 if the customer could not be created.
        if not result.is_success:
            msg = "Could not create customer with ID '{}': {}"
            msg_fmt = msg.format(customer_id, result.message)
            self.logger.error(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_409,
                title="Could not create.",
                description=msg_fmt,
            )

        result = {
            "customer_id": result.customer.id,
            "email": result.customer.email,
            "created_at": result.customer.created_at,
            "updated_at": result.customer.updated_at,
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
        customer_id: str,
    ):
        """ Deletes a Braintree customer.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
            customer_id (str): The Braintree customer ID for which deletion
                will be performed.

        Note:
            When a customer is deleted, all associated payment methods are also
            deleted, and all associated recurring billing subscriptions are
            cancelled.
        """

        msg = "Deleting customer with ID '{}'."
        msg_fmt = msg.format(customer_id)
        self.logger.info(msg_fmt)

        # Delete customer or respond with a 404 if no customer was found for
        # the given ID.
        try:
            result = self.gateway.customer.delete(customer_id=customer_id)
        except braintree.exceptions.NotFoundError as exc:
            msg_fmt = "Customer with ID '{}' not found.".format(customer_id)
            self.logger.exception(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_404,
                title="Not found.",
                description=msg_fmt,
            )

        # Respond with a 409 if the customer could not be deleted.
        if not result.is_success:
            msg = "Could not delete customer with ID '{}': {}"
            msg_fmt = msg.format(customer_id, result.message)
            self.logger.error(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_409,
                title="Could not delete.",
                description=msg_fmt,
            )

        resp.status = falcon.HTTP_204
