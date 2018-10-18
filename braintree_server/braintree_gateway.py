# coding: utf-8

"""Main module."""

import os
import argparse

from braintree_server.config import import_config
from braintree_server.api import create_api


_cfg = None


def load_config(filename_config_file=None):
    if filename_config_file:
        cfg = import_config(fname_config_file=filename_config_file)
    elif "BRAINTREE_GATEWAY_CONFIG" in os.environ:
        fname_config_file = os.environ["BRAINTREE_GATEWAY_CONFIG"]
        cfg = import_config(fname_config_file=fname_config_file)
    else:
        msg_fmt = "Configuration file path not defined."
        raise ValueError(msg_fmt)

    return cfg


def get_cfg(filename_config_file=None):
    global _cfg
    if _cfg is None:
        _cfg = load_config(filename_config_file=filename_config_file)

    return _cfg


def main(filename_config_file=None):

    cfg = load_config(filename_config_file=filename_config_file)

    api = create_api(cfg=cfg, logger_level=cfg.logger_level)

    return api


# main sentinel
if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(
        description=("fightfor-graphql: GraphQL API over the SQLAlchemy ORM "
                     "serving the project data via Falcon.")
    )
    argument_parser.add_argument(
        "--config-file",
        dest="config_file",
        help="configuration file",
        required=False
    )
    arguments = argument_parser.parse_args()

    if arguments.config_file:
        _filename_config_file = arguments.config_file
    else:
        _filename_config_file = None

    main(filename_config_file=_filename_config_file)
