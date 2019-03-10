import os
import logging
import yaml
from logging import config


"""
Init global config for server.
"""

# config global log config
fileDir = os.path.dirname(os.path.realpath('__file__'))
filename = os.path.join(fileDir, 'logging.yaml')

with open(filename) as f:
    # use safe_load instead load
    loggingConfig = yaml.safe_load(f)
    logging.basicConfig()
    config.dictConfig(loggingConfig)

log = logging.getLogger(__name__)


app_port = 4321