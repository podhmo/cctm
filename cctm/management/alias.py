# -*- coding:utf-8 -*-
import sys
from cctm import services


def main(config, name, alias, store=None):
    config.load_config()
    lookup = services.PackageLookup(config)
    data = lookup.lookup_loose(name)
    if not data:
        sys.stderr.write("{} is not found".format(name))
    store = services.aliases_store(config, path=store)
    store_data = store.update({"name": alias, "link": name}, store.load())
    data = store.save(store_data)


def includeme(config):
    config.register_command("management.alias", main)
