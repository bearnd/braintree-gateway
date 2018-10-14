# coding=utf-8

import falcon
import braintree

from braintree_server.loggers import create_logger

from braintree_server.resources.resource_ping import ResourcePing
from braintree_server.resources.resource_customer import ResourceCustomer
from braintree_server.resources.resource_subscription import (
    ResourceSubscription
)
from braintree_server.resources.resource_client_token import ResourceClientToken


def create_api(gateway: braintree.BraintreeGateway, logger_level: str):
    """ Creates a Falcon API and adds resources for the GraphQL and GraphiQL
        endpoints.

    Args:
        gateway (braintree.BraintreeGateway): The instantiated and
            configured Braintree gateway that will be used to interact with
            Braintree.
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

    # Create the API.
    api = falcon.API()

    msg_fmt = u"Initializing API resources."
    logger.info(msg_fmt)

    # Add the route used to ping the service.
    api.add_route(
        uri_template="/ping",
        resource=ResourcePing(gateway=gateway, logger_level=logger_level),
    )

    # Add the route used to retrieve (GET) or delete (DELETE) customers.
    api.add_route(
        uri_template="/customer/{customer_id}",
        resource=ResourceCustomer(gateway=gateway, logger_level=logger_level),
    )

    # Add the route used to create (POST) customers.
    api.add_route(
        uri_template="/customer",
        resource=ResourceCustomer(gateway=gateway, logger_level=logger_level),
    )

    # Add the route used to retrieve (GET) or delete (DELETE) subscriptions.
    api.add_route(
        uri_template="/subscription/{subscription_id}",
        resource=ResourceSubscription(
            gateway=gateway,
            logger_level=logger_level,
        ),
    )

    # Add the route used to create (POST) subscriptions.
    api.add_route(
        uri_template="/subscription",
        resource=ResourceSubscription(
            gateway=gateway,
            logger_level=logger_level,
        )
    )

    # Add the route used to retrieve (GET) client-tokens.
    api.add_route(
        uri_template="/client-token/{customer_id}",
        resource=ResourceClientToken(gateway=gateway, logger_level=logger_level)
    )

    msg_fmt = u"API initialization complete."
    logger.info(msg_fmt)

    return api
