# -*- coding:utf-8 -*-
import logging
from cctm import get_configurator
from cctm import services
logger = logging.getLogger(__name__)


def register_command(config, name, fn):
    parser = config.make_parser(fn, skip_options=["config"])

    def run_command(config, parsed):
        args = [getattr(parsed, name) for name in parser.positionals]
        kwargs = {name: getattr(parsed, name, None) for name in parser.optionals}
        return fn(config, *args, **kwargs)
    parser.set_defaults(fn=run_command)
    config.add_subcommand(name, parser)


def init(config):
    logger.info("initialize")
    config.init_config()


def selfupdate(config):
    config.load_config()
    logger.info("selfupdate")
    logger.info("updating store=%s", config.store_path)
    package_store = services.PackagesStore(config)
    repository_store = services.RepositoriesStore(config)
    package_store.save(repository_store.extract_packages())


def main(argv=None):
    config = get_configurator()
    logging.basicConfig(level=logging.INFO)
    config.add_directive("register_command", register_command)

    config.register_command("init", init)
    config.register_command("selfupdate", selfupdate)
    config.include("cctm.management.fetching")
    config.include("cctm.management.merging")
    config.include("cctm.management.listing")
    config.include("cctm.management.removing")
    args = config.make_args(argv)
    args.fn(config, args)
