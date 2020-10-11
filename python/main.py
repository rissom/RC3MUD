from system.log import log
from system.webserver import Webserver
from system.config import Config

import sys
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    raise Exception("Must be using Python 3.7 or higher")

log.info("starting...")

ws = Webserver()
ws.run(port=Config.getSingleton().getInt("webserverport"))
