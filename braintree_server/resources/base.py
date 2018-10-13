# coding=utf-8

import braintree
import falcon
import marshmallow
import json
from typing import Optional, Dict

from braintree_server.loggers import create_logger


class ResourceBase(object):
    """ Falcon resource base-class."""

    def __init__(self, gateway: braintree.BraintreeGateway, **kwargs):
        """Constructor.

        Args:
            gateway (braintree.BraintreeGateway): The instantiated and
                configured Braintree gateway that will be used to interact with
                Braintree.
        """

        # Internalize arguments.
        self.gateway = gateway

        # Create a class-level logger.
        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    def get_parameters(
        self,
        req: falcon.Request,
        schema: marshmallow.Schema
    ):
        """ Decodes the body of incoming requests via a `marshmallow` schema
            and returns the result.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            schema (marshmallow.Schema): The marshmallow schema instance that
                will be used to decode the body.
        """

        try:
            request_json = req.stream.read()
        except Exception as exc:
            msg_fmt = "Could not retrieve JSON body."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="InvalidRequest",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )

        try:
            if request_json:
                # If the JSON body came through as `bytes` it needs to be
                # decoded into a `str`.
                if isinstance(request_json, bytes):
                    request_json = request_json.decode("utf-8")
                # Decode the JSON body through the `marshmallow` schema.
                parameters = schema.loads(request_json).data
            else:
                parameters = {}
        except marshmallow.ValidationError as exc:
            msg_fmt = "Response body violates schema."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_422,
                title="Schema violation.",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )
        except Exception as exc:
            msg_fmt = "Could not decode JSON body."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_400,
                title="InvalidRequest",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )

        return parameters

    def prepare_response(
        self,
        resp: falcon.Response,
        result: Dict,
        schema: Optional[marshmallow.Schema] = None,
    ):
        """ Encodes a `result` either via a `marshmallow` schema or standard
            JSON-encoding and adds it to the provided `falcon.Response` object.

        Args:
            resp (falcon.Response): The Falcon `Response` object.
            result (Dict): The result that will be encoded and added to the
                `falcon.Response` object.
            schema (Optional[marshmallow.Schema] = None): The marshmallow
                schema instance that will be used to encode the result.

        Returns:
            falcon.Response: The updated response object.
        """

        try:
            if schema:
                response_json = schema.dumps(result).data
            else:
                response_json = json.dumps(result)
        except marshmallow.ValidationError as exc:
            msg_fmt = "Response body violates schema."
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_422,
                title="Schema violation.",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )
        except Exception as exc:
            msg_fmt = "Could not encode results '{0}' into JSON".format(result)
            self.logger.exception(msg_fmt)
            raise falcon.HTTPError(
                status=falcon.HTTP_500,
                title="UnhandledError",
                description=msg_fmt + ". Exception: {0}".format(str(exc))
            )

        resp.content_type = "application/json"
        resp.body = response_json

        return resp