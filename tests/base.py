# coding=utf-8

from falcon import testing

from braintree_server.config import import_config
from braintree_server.api import create_api

from tests.utils import JwtTokenGenerator


fname_config_file = "/etc/braintree-gateway/braintree-gateway-test.json"
cfg = import_config(fname_config_file=fname_config_file)

# Singleton placeholders.
_token_generator = None
_app = None


def _get_token_generator():
    """Returns an instance of `JwtTokenGenerator` configured for unit-testing.

    Returns:
        JwtTokenGenerator: The `JwtTokenGenerator` instance configured for
            unit-testing.
    """

    global _token_generator

    # If the token-generator has not been previously instantiated then do so
    # with the unit-test configuration.
    if not _token_generator:
        _token_generator = JwtTokenGenerator(
            auth0_client_id=cfg.auth0.client_id,
            auth0_client_secret=cfg.auth0.client_secret,
            auth0_domain=cfg.auth0.domain,
            auth0_audience=cfg.auth0.audience,
        )

    return _token_generator


def _get_app():
    """Returns an instance of the `falcon.API` configured for unit-testing.

    Returns:
        falcon.API: The `falcon.API` instance configured for unit-testing.
    """

    global _app

    # If the API has not been previously instantiated then do so with the
    # unit-test configuration.
    if not _app:
        _app = create_api(
            cfg=cfg,
            logger_level="CRITICAL",
        )

    return _app


class TestBase(testing.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()

        # Retrieve the `JwtTokenGenerator` singleton.
        self.token_generator = _get_token_generator()

        # Retrieve the `falcon.API` singleton.
        self.app = _get_app()

    def generate_jwt_headers(self):
        """ Generates headers with a populated `Authorization` header.

        Returns:
            dict: The generated headers.
        """

        # Generate an access-token.
        token = self.token_generator.generate()

        headers = {
            "Authorization": "Bearer {}".format(token),
        }

        return headers
