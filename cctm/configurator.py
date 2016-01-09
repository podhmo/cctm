# -*- coding:utf-8 -*-
import json
import os.path
import logging
from miniconfig import ConfiguratorCore, Control
from cached_property import cached_property as reify
from .path import pickup_file, safe_open
logger = logging.getLogger(__name__)


class CCTMControl(Control):
    DEFAULT_BASE_PATH = "~/.cctm/"

    @reify
    def base_path(self):
        return os.path.expanduser(self.settings.get("base_path", self.DEFAULT_BASE_PATH))

    @reify
    def current_path(self):
        return self.settings.get("current_path") or os.getcwd()

    @reify
    def config_path(self):
        return self.resolve_path("config.json")

    def resolve_path(self, target_file):
        return pickup_file(self.current_path, target_file) or os.path.join(self.base_path, target_file)


class Configurator(ConfiguratorCore):
    def __init__(self, settings=None, module=None, control=None):
        control = control or CCTMControl()
        super(Configurator, self).__init__(settings, module, control)
        control.settings = self.settings  # xxx
        includeme(self)


def load_config(config, path=None):
    path = path or config.config_path
    if not os.path.exists(path):
        logger.info("%s is not found. create as default configuration")
        config.init_config(path=path)

    with open(path) as rf:
        return json.load(rf)


def save_config(config, settings, path=None):
    path = path or config.config_path
    with safe_open(path, "w") as wf:
        json.dump(settings, wf, indent=2, ensure_ascii=False)


def init_config(config, path=None):
    path = path or config.config_path
    default_config = {}
    config.save_config(default_config, path=path)


def includeme(config):
    config.add_directive("load_config", load_config)
    config.add_directive("save_config", save_config)
    config.add_directive("init_config", init_config)
