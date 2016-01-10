# -*- coding:utf-8 -*-
import logging
from cctm import get_configurator
logger = logging.getLogger(__name__)


def register_command(config, name, fn):
    parser = config.make_parser(fn, skip_options=["config"])

    def run_command(config, parsed):
        args = [getattr(parsed, name) for name in parser.positionals]
        kwargs = {name: getattr(parsed, name) for name in parser.optionals}
        return fn(config, *args, **kwargs)
    parser.set_defaults(fn=run_command)
    config.add_subcommand(name, parser)


def init(config):
    logger.info("initialize")
    config.init_config()


def main(argv=None):
    config = get_configurator()
    config.add_directive("register_command", register_command)

    config.register_command("init", init)
    config.include("cctm.management.fetching")
    args = config.make_args(argv)
    args.fn(config, args)
