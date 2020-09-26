import json
from game.room import Room
from system.helper import i18n

class Player(object):
    
    def __init__(self, wsclient):
        self.wsclient = wsclient
        self.name = "Bernd"
        self.room = Room.get_room_by_id(1)
        self.lang = "en"
        
        self.enter_room(1)
        
    def enter_room(self, roomid):
        newroom = Room.get_room_by_id(roomid)
        self.room.player_leaves_room(self)
        newroom.player_enters_room(self)
        if len(newroom.actions) == 0:
            actionsstring = "There is nothing you can do here, sorry..."
        else:
            actionsstring = ""
            for a in newroom.actions:
                actionsstring = actionsstring + i18n(self.lang, a['description'])+"\r\n"
                
        ans = {
              "cmd": "text",
              "data": "\r\n\r\n"+i18n(self.lang,newroom.description)+"\r\n"+actionsstring
            }
        self.wsclient.write_message(ans)
        ans = {
              "cmd": "html",
              "data": i18n(self.lang,newroom.webview)
            }
        self.wsclient.write_message(ans)
        self.room = newroom
        
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
        elif msg.startswith("room2json"):
            ans = {
              "cmd": "text",
              "data": self.room.toJSON()
            }
            self.wsclient.write_message(json.dumps(ans))
        elif not self.room.parse_user_command(self, msg):
            ans = {
              "cmd": "text",
              "data": "What you mean by '"+msg+"'"
            }
            self.wsclient.write_message(json.dumps(ans))
            