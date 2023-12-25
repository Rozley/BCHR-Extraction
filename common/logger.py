import os
import sys
from datetime import datetime
from typing import Any

from loguru import logger

import common.config
from common.config import LOG_LEVEL

log_path = './logs'
if not os.path.exists(log_path):
    os.mkdir(log_path)

log_file = '{0}/{1}.log'.format(log_path, datetime.now().strftime('%Y-%m-%d'))

logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL)
logger.add(log_file, rotation="12:00", retention="1 days", enqueue=True)


def debug_log(message: str, *args: Any, **kwargs: Any):
    if common.config.DEBUG:
        logger.debug(message, *args, **kwargs)
