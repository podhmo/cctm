# -*- coding:utf-8 -*-
import logging
from cctm import services
logger = logging.getLogger(__name__)


def main(config, name):
    config.load_config()
    store = services.packages_store(config)
    store_data = store.load()
    new_data = store.remove(name, store_data)
    logger.info("remove package %s from store", name)
    if len(new_data) != len(store_data):
        logger.info("%s is removed", name)
        store.save(new_data)


def includeme(config):
    config.register_command("management.remove", main)
