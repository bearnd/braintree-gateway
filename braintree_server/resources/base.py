# coding=utf-8

import json
from typing import Optional, Dict

import attrdict
import braintree
import falcon
import marshmallow

from braintree_server.loggers import create_logger


class ResourceBase(object):
    """ Falcon resource base-class."""

    def __init__(
        self,
        cfg: attrdict.AttrDict,
        gateway: braintree.BraintreeGateway,
        **kwargs
    ):
        """Constructor.

        Args:
            cfg (attrdict.Attrdict): The application configuration loaded with
                the methods under the `config.py` module.
            gateway (braintree.BraintreeGateway): The instantiated and
                configured Braintree gateway that will be used to interact with
                Braintree.
        """

        # Internalize arguments.
        self.cfg = cfg
        self.gateway = gateway

        # Create a class-level logger.
        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level=kwargs.get("logger_level", "DEBUG")
        )

    def check_auth(
        self,
        req: falcon.Request,
        customer_id: str
    ):
        """ Checks whether the access-token provided in the request
            authorizes the caller to access resources pertaining to a specific
            customer.

        Note:
            As in service-to-service requests there is not user ID in the
            access-token, any requests where the access-token contains a  `sub`
            including the API's `client_id` (provided during  instantiation)
            are considered authorized.

        Args:
            req (falcon.Request): The Falcon `Request` object.
            customer_id (str): The customer ID against which the check is
                performed.

        Raises:
            falcon.HTTPError: Raised with a 403 response if the incoming
                request is unathorized.
        """

        # Retrieve the decoded token payload from the request context.
        token_payload = req.context["token_payload"]

        # If the value of the token `sub` field does not contain either the
        # provided `customer_id` or the configured `client_id` (used in
        # service-to-service requests) then the response is authorized hence
        # a 403 exception is raised.
        if (
            customer_id not in token_payload["sub"] and
            self.cfg.auth0.client_id not in token_payload["sub"]
        ):
            msg = ("'Authorization' token does not grant access to customer "
                   "with ID '{}'.")
            msg_fmt = msg.format(customer_id)
            self.logger.error(msg_fmt)

            raise falcon.HTTPError(
                status=falcon.HTTP_403,
                title="Unathorized.",
                description=msg_fmt,
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
                description=msg_fmt,
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
                description=msg_fmt + " Exception: {0}".format(str(exc))
            )
        except Exception as exc:
            msg_fmt = "Could not decode JSON body '{}'.".format(request_json)
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
