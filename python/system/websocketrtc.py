import tornado.websocket
import json
import datetime
from system.log import log
from system.webserver import Webserver
from game.player import Player

class WebsocketRTC(tornado.websocket.WebSocketHandler):
    
    websocket_send_data = []
    websocket_clients = []
    
    def websocket_send(client,data,binary=False):
        WebsocketRTC.websocket_send_data.append([client,data,binary])
        Webserver.main_loop.add_callback(WebsocketRTC.send_to_socket)
        
    def send_to_socket():
        client,data,binary = WebsocketRTC.websocket_send_data.pop(0)
        if len(WebsocketRTC.websocket_clients)>0:
            if client == True:
                for c in WebsocketRTC.websocket_clients:
                    c.write_message(data,binary)
            else:
                client.write_message(data,binary)
        else:
            log.warn("Webserver: send_to_socket: message dropped: no clients!")

    def write_all_but_me(self,message):
        for c in WebsocketRTC.websocket_clients:
            if c is not self:
                c.write_message(message)

    def open(self):
        log.debug("WebSocketRTC opened")
        WebsocketRTC.websocket_clients.append(self)
        
        #ans = {
        #      "cmd": "version"
        #    }
        #self.write_message(json.dumps(ans)) # hier ok!
        #Websocket.websocket_send(self,json.dumps(ans),False)
                 
    def on_message(self, message):
        # process json messages
        jsonmsg = json.loads(message)
        log.debug("Websocket: received message: "+str(jsonmsg))
        self.write_all_but_me(message)
        #if jsonmsg['cmd']=='ping':
        #    ans = {
        #      "cmd": "pong",
        #    }
        #    self.write_message(json.dumps(ans))
        #elif jsonmsg['cmd']=='user':
        #    self.player.parse_user_command(jsonmsg['data'])
        
            
    def on_close(self):
        log.debug("WebSocketRTC closed")
        WebsocketRTC.websocket_clients.remove(self)

        