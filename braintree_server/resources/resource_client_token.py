# coding=utf-8

import falcon
import marshmallow

from braintree_server.resources.base import ResourceBase


class SchemaClientToken(marshmallow.Schema):
    """Marshmallow schema for Braintree client-token response."""

    token = marshmallow.fields.String(required=True)

    class Meta:
        strict = True


class ResourceClientToken(ResourceBase):
    """Resource-class to manage Braintree client-tokens."""

    schema = SchemaClientToken()

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
        customer_id: str,
    ):
        """ Generates and responds with a Braintree client-token for a given
            customer.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
            customer_id (str): The Braintree customer ID for which the token
                will be generated.
        """

        msg = "Generating customer-token for customer with ID '{}'."
        msg_fmt = msg.format(customer_id)
        self.logger.info(msg_fmt)

        # Generate client-token.
        token = self.gateway.client_token.generate({
            "customer_id": customer_id,
        })

        resp = self.prepare_response(
            resp=resp,
            result={"token": token},
            schema=self.schema,
        )
        resp.status = falcon.HTTP_200
