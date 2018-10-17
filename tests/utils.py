# coding=utf-8

"""
This module defines the `JwtTokenGenerator` which can be used to generate
Auth0 access-tokens used in unit-testing.
"""

import json

import requests

from braintree_server.loggers import create_logger
from braintree_server.excs import Auth0TokenRetrievalError


class JwtTokenGenerator(object):
    """ Class meant to generate Auth0 access-tokens used in unit-testing."""

    _token = None
    _token_expiry = None

    def __init__(
        self,
        auth0_client_id: str,
        auth0_client_secret: str,
        auth0_domain: str,
        auth0_audience: str,
    ):
        """ Constructor.

        Args:
            auth0_client_id (str): The Auth0 client ID.
            auth0_client_secret (str): The Auth0 client secret.
            auth0_domain (str): The Auth0 domain.
            auth0_audience (str): The Auth0 audience.
        """

        # Internalize arguments.
        self.auth0_client_id = auth0_client_id
        self.auth0_client_secret = auth0_client_secret
        self.auth0_domain = auth0_domain
        self.auth0_audience = auth0_audience

        # Assemble the Auth0 OAuth token URL.
        self.auth0_oauth_url = "https://{auth0_domain}/oauth/token".format(
            auth0_domain=self.auth0_domain,
        )

        # Create a class-level logger.
        self.logger = create_logger(
            logger_name=type(self).__name__,
            logger_level="DEBUG"
        )

    def generate(self):
        """ Generates and returns an Auth0 access-token that can be used to
            authenticate during unit-testing.

        Note:
            This method keeps a copy of the first access-token to be retrieved
            and returns it in subsequent calls.

        Returns:
            str: The access-token.
        """

        # If a token was previously retrieved return it.
        if self._token:
            return self._token

        # Perform a POST request against the Auth0 OAuth token endpoint and
        # retrieve a new access-token.
        response = requests.post(
            url=self.auth0_oauth_url,
            headers={"content-type": "application/json"},
            data=json.dumps({
                "client_id": self.auth0_client_id,
                "client_secret": self.auth0_client_secret,
                "audience": self.auth0_audience,
                "grant_type": "client_credentials",
            })
        )

        if response.ok:
            # Set the new token under `self._token`.
            self._token = response.json()["access_token"]
            # Return the token.
            return self._token
        else:
            msg = "Could not retrieve the Auth0 JWT token from URL '{}'"
            msg_fmt = msg.format(self.auth0_oauth_url)
            self.logger.error(msg_fmt)
            raise Auth0TokenRetrievalError(msg_fmt)
