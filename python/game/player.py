import json
from game.room import Room

class Player(object):
    
    def __init__(self, wsclient):
        self.wsclient = wsclient
        self.name = "Bernd"
        self.room = None
        self.enter_room(1)
        
    def enter_room(self, roomid):
        newroom = Room.get_room_by_id(roomid)
        ans = {
              "cmd": "text",
              "data": newroom.description
            }
        self.wsclient.write_message(ans)
        
    def parse_user_command(self, msg):
        
        if msg.startswith("whoami"):
            ans = {
              "cmd": "text",
              "data": "You are "+self.name
            }
            self.wsclient.write_message(json.dumps(ans))
        elif msg.startswith("sleep"):
            ans = {
              "cmd": "text",
              "data": "You feel refreshed"
            }
            self.wsclient.write_message(json.dumps(ans))
        else:
            ans = {
              "cmd": "text",
              "data": "What you mean by '"+msg+"'"
            }
            self.wsclient.write_message(json.dumps(ans))