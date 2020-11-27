import logging
import time

logging.basicConfig(filename='app.log'.format(time.time()),
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)

logger = logging.getLogger(__name__)

logging.debug("a")
logging.info("b")
logging.warning("c")
logging.error("d")
logging.critical("e")

