# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from cctm.config import Configurator


def get_configurator():
    config = Configurator()
    config.include("cctm.config")
    config.include("miniconfig_argparse")
    config.include("miniconfig_argparse.parsertree")
    return config
