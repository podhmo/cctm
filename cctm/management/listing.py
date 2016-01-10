# -*- coding:utf-8 -*-
import sys
from cctm import services
from cctm.path import safe_listdir


def main(config, installed=False, alias=False):
    config.load_config()
    if installed:
        for path in safe_listdir(config.store_dir):
            print(path.replace(".", "/", 1))
    elif alias:
        store = services.aliases_store(config)
        for data in store.load():
            print("{data[name]} -> {data[link]}".format(data=data))
    else:
        def gen():
            sys.stderr.write("-- template --\n")
            store = services.packages_store(config)
            for data in store.load():
                yield ("{data[name]}({data[star]}) -- {data[description]:.60}".format(data=data))
            sys.stderr.write("-- alias --\n")
            store = services.aliases_store(config)
            for data in store.load():
                yield("{data[name]} -> {data[link]}".format(data=data))

        for line in gen():
            print(line)


def includeme(config):
    config.register_command("list", main)
