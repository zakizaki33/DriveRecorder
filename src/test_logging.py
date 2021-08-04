# https://develop.blue/2020/02/python-use-logging/

import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logging.error("ERROR MESSAGE")
