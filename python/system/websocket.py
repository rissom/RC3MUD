import tornado.websocket
import json
import datetime
from system.log import log
from system.webserver import Webserver

class Websocket(tornado.websocket.WebSocketHandler):
    
    websocket_send_data = []
    websocket_clients = []
    
    def websocket_send(client,data,binary=False):
        Websocket.websocket_send_data.append([client,data,binary])
        Webserver.main_loop.add_callback(Websocket.send_to_socket)
        
    def send_to_socket():
        client,data,binary = Websocket.websocket_send_data.pop(0)
        if len(Websocket.websocket_clients)>0:
            if client == True:
                for c in Websocket.websocket_clients:
                    c.write_message(data,binary)
            else:
                client.write_message(data,binary)
        else:
            log.warn("Webserver: send_to_socket: message dropped: no clients!")


    def open(self):
        print("WebSocket opened")
        self.nextIsBinary = None
        Websocket.websocket_clients.append(self)
        
        ans = {
              "cmd": "version"
            }
        self.write_message(json.dumps(ans)) # hier ok!
        #Websocket.websocket_send(self,json.dumps(ans),False)
                 
    def on_message(self, message):
        # process json messages
        jsonmsg = json.loads(message)
        log.debug("Websocket: received message: "+str(jsonmsg))
        
        if jsonmsg['cmd']=='ping':
            ans = {
              "cmd": "pong",
            }
            self.write_message(json.dumps(ans))
        elif jsonmsg['cmd']=='user':
            ans = {
                'cmd': 'text',
                'data': "what do yo mean with '"+jsonmsg['data']+"'"
            }
            self.write_message(json.dumps(ans))
        
            
    def on_close(self):
        print("WebSocket closed")
        Websocket.websocket_clients.remove(self)

        