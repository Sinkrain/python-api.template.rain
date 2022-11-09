# -*- coding: utf-8 -*-

import logging

from config import LOGGER_LEVEL


logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S', level=logging.INFO)
logger = logging.getLogger(__name__)

logger.setLevel(LOGGER_LEVEL)
