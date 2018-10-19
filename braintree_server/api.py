# coding=utf-8

import attrdict
import falcon
import braintree

from braintree_server.loggers import create_logger
from braintree_server.middlewares.auth0 import MiddlewareCors
from braintree_server.middlewares.auth0 import MiddlewareAuth0
from braintree_server.resources.resource_ping import ResourcePing
from braintree_server.resources.resource_customer import ResourceCustomer
from braintree_server.resources.resource_subscription import (
    ResourceSubscription
)
from braintree_server.resources.resource_client_token import ResourceClientToken
from braintree_server.resources.resource_client_token import (
    ResourceClientTokenNoCustomerId
)


def create_api(
    cfg: attrdict.AttrDict,
    logger_level: str
):
    """ Creates a Falcon API and adds resources the different endpoints.

    Args:
        cfg (attrdict.Attrdict): The application configuration loaded with the
            methods under the `config.py` module.
        logger_level (str): The logger level to be set in the Falcon resource
            classes.

    Returns:
        falcon.api.API: The instantiate Falcon API.
    """

    # Create logger.
    logger = create_logger(
        logger_name=__name__,
        logger_level=logger_level
    )

    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=cfg.braintree.environment,
            merchant_id=cfg.braintree.merchant_id,
            public_key=cfg.braintree.public_key,
            private_key=cfg.braintree.private_key,
        )
    )

    # Create the API.
    api = falcon.API(
        middleware=[
            # Instantiate and add the CORS middleware.
            MiddlewareCors(logger_level=logger_level),
            # Instantiate and add the Auth0 authentication middleware.
            MiddlewareAuth0(
                auth0_domain=cfg.auth0.domain,
                auth0_audience=cfg.auth0.audience,
                auth0_jwks_url=cfg.auth0.jwks_url,
                exlcude=["/ping"],
                logger_level=logger_level,
            ),
        ],
    )

    msg_fmt = u"Initializing API resources."
    logger.info(msg_fmt)

    # Add the route used to ping the service.
    api.add_route(
        uri_template="/ping",
        resource=ResourcePing(
            cfg=cfg,
            gateway=gateway,
            logger_level=logger_level,
        ),
    )

    # Add the route used to retrieve (GET) or delete (DELETE) customers.
    api.add_route(
        uri_template="/customer/{customer_id}",
        resource=ResourceCustomer(
            cfg=cfg,
            gateway=gateway,
            logger_level=logger_level,
        ),
    )

    # Add the route used to create (POST) customers.
    api.add_route(
        uri_template="/customer",
        resource=ResourceCustomer(
            cfg=cfg,
            gateway=gateway,
            logger_level=logger_level,
        ),
    )

    # Add the route used to retrieve (GET) or delete (DELETE) subscriptions.
    api.add_route(
        uri_template="/customer/{customer_id}/subscription/{subscription_id}",
        resource=ResourceSubscription(
            cfg=cfg,
            gateway=gateway,
            logger_level=logger_level,
        ),
    )

    # Add the route used to create (POST) subscriptions.
    api.add_route(
        uri_template="/customer/{customer_id}/subscription",
        resource=ResourceSubscription(
            cfg=cfg,
            gateway=gateway,
            logger_level=logger_level,
        )
    )

    # Add the route used to retrieve (GET) client-tokens without a customer ID.
    api.add_route(
        uri_template="/client-token",
        resource=ResourceClientTokenNoCustomerId(
            cfg=cfg,
            gateway=gateway,
            logger_level=logger_level,
        ),
    )

    # Add the route used to retrieve (GET) client-tokens with a customer ID.
    api.add_route(
        uri_template="/client-token/{customer_id}",
        resource=ResourceClientToken(
            cfg=cfg,
            gateway=gateway,
            logger_level=logger_level,
        ),
    )

    msg_fmt = u"API initialization complete."
    logger.info(msg_fmt)

    return api
