
from system.webserver import Webserver
from system.config import Config



print("starting...")
ws = Webserver()

ws.run(port=Config.getSingleton().getInt("webserverport"))

