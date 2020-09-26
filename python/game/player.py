import json
import string
from game.room import Room
from system.helper import i18n

class Player(object):
    
    actions = [ { "command": { "de": "sage"  , "en": "say" } ,
                 "function" : "action_say",
                "description":  { "de": "sagt", "en": "says" }
                },
                { "command": { "de": "umbenennen"  , "en": "rename" } ,
                 "function" : "action_rename",
                "description":  { "de": "heisst jetzt", "en": "is now known as" }
                }
              ]
    
    def __init__(self, wsclient):
        self.wsclient = wsclient
        self.name = "Bernd"
        self.room = Room.get_room_by_id(1)
        self.lang = "en"
        
        self.enter_room(1)
    
    def send_text(self, text):
        ans = {
              "cmd": "text",
              "data": text
            }
        try:
            self.wsclient.write_message(ans)
        except tornado.websocket.WebSocketClosedError:
            Websocket.websocket_clients.remove(self.wsclient)
            
    def action_say(self,a,msg):
        for p in self.room.player:
            p.send_text("\r\n"+self.name+" "+i18n(p.lang,a['description'])+" '"+msg[ len(i18n(self.lang,a['command']))+1:]+"'")
    
    def action_rename(self,a,msg):
        newname = msg[ len(i18n(self.lang,a['command']))+1:]
        for p in self.room.player:
            p.send_text("\r\n"+self.name+" "+i18n(p.lang,a['description'])+" '"+newname+"'")
        self.name = newname
       
    def send_player_new_command_list(self):
        commands = []
        for a in Player.actions:
            commands.append(i18n(self.lang,a['command']))
        ans = { "cmd" : "newcommandlist",
                "type":"player",
                "data" : commands}
        self.wsclient.write_message(ans)
        commands = self.room.get_room_command_list(self)
        ans = { "cmd" : "addcommandlist",
                "type": "room",
                "data" : commands}
        self.wsclient.write_message(ans)
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
                
        self.send_text("\r\n\r\n"+i18n(self.lang,newroom.description)+"\r\n"+actionsstring)
        ans = {
              "cmd": "html",
              "data": i18n(self.lang,newroom.webview)
            }
        self.wsclient.write_message(ans)
        self.room = newroom
        self.send_player_new_command_list()
        
    def parse_user_command(self, msg):
        answered = False
        
        for a in Player.actions:
            if msg.startswith(i18n(self.lang,a['command'])):
                getattr(self,a['function'])(a,msg)
                answered = True

        if msg.startswith("whoami"):
            self.send_text("You are "+self.name)
            answered = True
        elif msg.startswith("sleep"):
            self.send_text("You feel refreshed")
            answered = True
        elif msg.startswith("room2json"):
            self.send_text(self.room.toJSON())
            answered = True
        
        if not answered:
            answered = self.room.parse_user_command(self, msg)
        if not answered:
            self.send_text("What you mean by '"+msg+"'")
            