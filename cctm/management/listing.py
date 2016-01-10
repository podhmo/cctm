# -*- coding:utf-8 -*-
from cctm import services
from cctm.path import safe_listdir


def main(config, installed=False):
    config.load_config()
    if installed:
        for path in safe_listdir(config.template_dir):
            print(path.replace(".", "-", 1))
    else:
        store = services.PackagesStore(config)

        def gen():
            for data in store.load():
                yield ("{data[name]}({data[star]}) -- {data[description]:.60}".format(data=data))

        for line in sorted(gen()):
            print(line)


def includeme(config):
    config.register_command("list", main)
