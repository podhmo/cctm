# -*- coding:utf-8 -*-
import sys
from cctm import services


def main(config, name, alias, store=None):
    config.load_config()
    lookup = services.PackageLookup(config)
    data = lookup.lookup_loose(name)
    if not data:
        sys.stderr.write("{} is not found".format(name))
    alias_store = services.aliases_store(config, path=store)

    data = {"name": alias, "link": name}
    store_data = alias_store.update(data, alias_store.load())
    alias_store.save(store_data)

    if store is None:
        local_store = services.aliases_store(config, path=config.control.resolve_path("local.alias.json"))
        store_data = local_store.update(data, local_store.load())
        local_store.save(store_data)


def includeme(config):
    config.register_command("management.alias", main)
