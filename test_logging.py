# https://develop.blue/2020/02/python-use-logging/

import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logging.error("ERROR MESSAGE")


# https://ryoz001.com/1154.html#toc3
logger = logging.getLogger(__name__)

consoleHandler = logging.StreamHandler()
logger.addHandler(consoleHandler)

logger.debug("でっばくだよん")
logger.info("infoだよん")
logger.warning("WARNINGだよん")
logger.error("errorだよん")
logger.critical("CRITICALだよん")
