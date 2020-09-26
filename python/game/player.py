import json
import string
from game.room import Room
from system.helper import i18n

class Player(object):
    
    actions = [ { "command": { "de": "sage"  , "en": "say" } ,
                 "function" : "action_say",
                "description":  { "de": "sagt", "en": "says" }
                }
              ]
    
    def __init__(self, wsclient):
        self.wsclient = wsclient
        self.name = "Bernd"
        self.room = Room.get_room_by_id(1)
        self.lang = "en"
        
        self.enter_room(1)
    
    def action_say(self,a,msg):
        for p in self.room.player:
            ans = {
              "cmd": "text",
              "data": "\r\n"+self.name+" "+i18n(p.lang,a['description'])+" '"+msg[ len(i18n(self.lang,a['command']))+1:]+"'"
            }
            p.wsclient.write_message(ans)
            
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
        answered = False
        
        for a in Player.actions:
            if msg.startswith(i18n(self.lang,a['command'])):
                getattr(self,a['function'])(a,msg)
                answered = True

        if msg.startswith("whoami"):
            ans = {
              "cmd": "text",
              "data": "You are "+self.name
            }
            self.wsclient.write_message(json.dumps(ans))
            answered = True
        elif msg.startswith("sleep"):
            ans = {
              "cmd": "text",
              "data": "You feel refreshed"
            }
            self.wsclient.write_message(json.dumps(ans))
            answered = True
        elif msg.startswith("room2json"):
            ans = {
              "cmd": "text",
              "data": self.room.toJSON()
            }
            self.wsclient.write_message(json.dumps(ans))
            answered = True
        
        if not answered:
            answered = self.room.parse_user_command(self, msg)
        if not answered:
            ans = {
              "cmd": "text",
              "data": "What you mean by '"+msg+"'"
            }
            self.wsclient.write_message(json.dumps(ans))
            