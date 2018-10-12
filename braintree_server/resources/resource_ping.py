# coding=utf-8

import falcon
import marshmallow

from braintree_server.resources.base import ResourceBase


class SchemaPingResponse(marshmallow.Schema):
    """Marshmallow schema for ping response."""

    status = marshmallow.fields.String(required=True)


class ResourcePing(ResourceBase):
    """Resource-class to perform ping-requests."""

    schema = SchemaPingResponse()

    def on_get(
        self,
        req: falcon.Request,
        resp: falcon.Response,
    ):
        """Responds with the service status.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            resp (falcon.Response): The Falcon `Response` object.
        """

        msg_fmt = "Processing 'ping' request."
        self.logger.info(msg_fmt)

        resp = self.prepare_response(
            resp=resp,
            result={"status": "OK"},
            schema=self.schema,
        )
        resp.status = falcon.HTTP_200
