import logging as logger
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', logger.ERROR)
logger.basicConfig(level=LOG_LEVEL)
CPU_COUNT = os.cpu_count()

