# -*- coding:utf-8 -*-
import logging
import os.path
import subprocess
logger = logging.getLogger(__name__)


class TemplateInstaller(object):
    def __init__(self, config):
        self.config = config

    def install(self, data):
        logger.info("install {data[name]}".format(data=data))
        outdir = os.path.join(self.config.template_dir, data["name"].replace("/", "."))
        if not os.path.exists(outdir):
            subprocess.call(["git", "clone", "--depth=1", data["url"], outdir])
