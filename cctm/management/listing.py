# -*- coding:utf-8 -*-
from cctm import services


def main(config):
    config.load_config()
    store = services.PackagesStore(config)

    def gen():
        for data in store.load():
            yield ("{data[name]}({data[star]}) -- {data[description]:.60}".format(data=data))

    for line in sorted(gen()):
        print(line)


def includeme(config):
    config.register_command("list", main)
