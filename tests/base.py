# coding=utf-8

import braintree
from falcon import testing

from braintree_server.config import import_config
from braintree_server.api import create_api


fname_config_file = "/etc/braintree-gateway/braintree-gateway-test.json"
_gateway = None


def get_gateway():
    global _gateway

    if not _gateway:
        cfg = import_config(fname_config_file=fname_config_file)

        _gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                environment=cfg.braintree.environment,
                merchant_id=cfg.braintree.merchant_id,
                public_key=cfg.braintree.public_key,
                private_key=cfg.braintree.private_key,
            )
        )

    return _gateway


class TestBase(testing.TestCase):

    def setUp(self):
        super(TestBase, self).setUp()

        self.gateway = get_gateway()

        self.app = create_api(gateway=self.gateway, logger_level="CRITICAL")
