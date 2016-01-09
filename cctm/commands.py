# -*- coding:utf-8 -*-
from cctm import get_configurator


def main():
    config = get_configurator()
    print(config.load_config())
