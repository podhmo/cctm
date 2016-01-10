# -*- coding:utf-8 -*-
import requests
import logging
from cctm import services
from cctm import json
from cctm import github
logger = logging.getLogger(__name__)


def fetch(repository, show_all):
    full_name = github.get_fullname(repository)
    url = github.Namespace(full_name).summary_url
    logger.info("fetching url=%s", url)
    # TODO: auth
    data = requests.get(url).json()

    if not show_all:
        remapper = github.SummaryRemapper()
        data = remapper(data)
    return data


def main(config, repository, show_all=False, save=False, store=None):
    config.load_config()
    data = fetch(repository, show_all=show_all)
    if not save:
        print(json.dumps(data))
    else:
        package_store = services.packages_store(config, path=store)
        store_data = package_store.update(data, package_store.load())
        package_store.save(store_data)
        if store is None:
            local_store = services.packages_store(config, path=config.control.resolve_path("local.repository.json"))
            store_data = local_store.update(data, local_store.load())
            local_store.save(store_data)


def includeme(config):
    config.register_command("management.fetch", main)
