# -*- coding:utf-8 -*-
import logging
import itertools
from cctm import services
logger = logging.getLogger(__name__)


def main(config, url=None, save=False):
    config.load_config()
    package_store = services.DumpOrSaveWrapper(services.packages_store(config), save=save)
    repository_store = services.RepositoriesStore(config)
    new_repositories = [url] if url else []
    new_data = repository_store.extract_packages(itertools.chain(config.repositories, new_repositories))
    package_store.save(new_data)


def includeme(config):
    config.register_command("management.merge", main)
