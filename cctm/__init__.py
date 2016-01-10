# -*- coding:utf-8 -*-
import logging
import os.path
from cctm import services
from cctm import json
from cctm.config import Configurator
logger = logging.getLogger(__name__)


def get_configurator():
    config = Configurator()
    config.include("cctm.config")
    config.include("miniconfig_argparse")
    config.include("miniconfig_argparse.parsertree")
    return config


def register_command(config, name, fn):
    parser = config.make_parser(fn, skip_options=["config"])

    def run_command(config, parsed):
        args = [getattr(parsed, name) for name in parser.positionals]
        kwargs = {name: getattr(parsed, name, None) for name in parser.optionals}
        return fn(config, *args, **kwargs)
    parser.set_defaults(fn=run_command)
    config.add_subcommand(name, parser)


def init(config, project=None):
    if project:
        config.set_value("base_path", project)
    if os.path.exists(config.config_path):
        print("already exists. {}".format(config.config_path))
    else:
        default_config = {
            "base_path": config.base_path,
            "template_dir": config.template_dir,
            "repositories": [
                "https://raw.githubusercontent.com/podhmo/cctm/master/data/cookiecutter.index.json",
                "file://{}".format(os.path.join(config.base_path, "local.repository.json"))
            ],
            "aliases": [
                "https://raw.githubusercontent.com/podhmo/cctm/master/data/alias.json",
                "file://{}".format(os.path.join(config.base_path, "local.alias.json"))
            ]
        }
        logger.info("initialize. generating %s", os.path.abspath(config.config_path))
        config.save_config(default_config, config.config_path)


def show(config, name, tags=False):
    config.load_config()
    lookup = services.PackageLookup(config)
    data = lookup.lookup_loose(name) or "not found."
    print(json.dumps(data))
    if tags:
        # TODO: move
        import subprocess
        subprocess.call(["git", "ls-remote", "--tags", data["url"]])


def install(config, name, upgrade=False, tag=None):
    config.load_config()
    lookup = services.PackageLookup(config)
    data = lookup.lookup_loose(name)
    if data is None:
        print("not found: {}".format(name))
    else:
        installer = services.TemplateInstaller(config)
        installer.install(data, upgrade=upgrade, tag=tag)


def use(config, name, retry=True):
    config.load_config()
    lookup = services.InstalledPackageLookup(config)
    data = lookup.lookup_loose(name)
    if data:
        from cookiecutter.main import cookiecutter
        cookiecutter(data["path"])
    elif retry:
        install(config, name)
        use(config, name, retry=False)


def selfupdate(config):
    config.load_config()
    logger.info("selfupdate")
    logger.info("updating store=%s", config.store_path)
    package_store = services.packages_store(config)
    alias_store = services.aliases_store(config)
    repository_store = services.RepositoriesStore(config)
    package_store.save(repository_store.extract_packages(config.repositories))
    alias_store.save(repository_store.extract_packages(config.aliases))


def main(argv=None):
    config = get_configurator()
    logging.basicConfig(level=logging.INFO)
    config.add_directive("register_command", register_command)

    config.register_command("init", init)
    config.register_command("show", show)
    config.register_command("install", install)
    config.register_command("use", use)
    config.register_command("selfupdate", selfupdate)
    config.include("cctm.management.fetching")
    config.include("cctm.management.alias")
    config.include("cctm.management.merging")
    config.include("cctm.management.listing")
    config.include("cctm.management.removing")
    args = config.make_args(argv)
    args.fn(config, args)
