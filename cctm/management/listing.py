# -*- coding:utf-8 -*-
from cctm import services


def main(config):
    store = services.PackagesStore(config)
    for data in store.load():
        print("{data[name]}({data[star]}) -- {data[description]}".format(data=data))


def includeme(config):
    config.register_command("list", main)
