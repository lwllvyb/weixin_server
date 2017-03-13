# -*- coding: utf-8 -*-
import logging
from liyanyi_utils.utils import new_logger

LOGGER = new_logger("weixin_server.log", "weixin_server")
LOGGER.setLevel(logging.INFO)

def get_logger():
    return LOGGER 