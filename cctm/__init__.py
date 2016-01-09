# -*- coding:utf-8 -*-
import logging
logger = logging.getLogger(__name__)
from cctm.configurator import Configurator


def get_configurator():
    return Configurator()
