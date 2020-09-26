from system.log import log
from system.webserver import Webserver
from system.config import Config


log.info("starting...")
ws = Webserver()

ws.run(port=Config.getSingleton().getInt("webserverport"))

