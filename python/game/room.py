import json
from system.serializer import Serializer
from system.log import log
from system.helper import i18n


class Room(object):
    
    all_rooms = []
    
    # class function to get a room by id
    def get_room_by_id(roomid):
        for room in Room.all_rooms:
            if room.roomid == roomid:
                return room
        room = Serializer.get_room(roomid)
        Room.all_rooms.append(room)
        return room
    
    
    def __init__(self, roomid):
        self.roomid = roomid
        self.player = []  # player in this room
        self.actions = [ { "command": { "de": "gehe norden"  , "en": "go north" } ,
                           "description":  { "de": "$$nix$$Im Norden ist irgendwas.", "en": "$$null$$You see something in the north" },
                           "roomid": 2 
                         }
                        ]
        self.name = "__undefined__"
        self.description = { "en": "This is the well known undefined void where nothing has been created yet.\r\nThere are no exits and there is nothing to find here."}
        self.items = []
        
        self.capacity = -1
        self.webview = "<b>Hier ist die HTML Beschreibung</b>"
    
    def player_leaves_room(self,player):
        if player in self.player:
            self.player.remove(player)
        for p in self.player:
            p.send_text(i18n(p.lang,{ "en": ""+player.name+" leaves the room..." } ))
    
    def get_room_command_list(self,player):
        commands = []
        for a in self.actions:
            commands.append(i18n(player.lang,a['command']))
        return commands
                
    def player_enters_room(self,player):
        for p in self.player:
            p.send_text(i18n(p.lang,{ "en": ""+player.name+" enters the room..." }))
        self.player.append(player)
        
    def execute_action(self,player,action):
        if 'roomid' in action:
            player.enter_room(action['roomid'])
        
    def parse_user_command(self, player, msg):
        for a in self.actions:
            if msg.startswith(i18n(player.lang,a['command'])):
                self.execute_action(player,a)
                return True
        return False
        
    def fromJSON(self, json):
        self.description = json["description"]
        self.actions = json["actions"]
        self.webview = json["webview"]
        
    def toJSON(self):
        ans = { "roomid" : self.roomid,
               "actions" : self.actions,
               "name" : self.name,
               "description" : self.description,
               "items" : self.items,
               "capacity" : self.capacity,
               "webview" : self.webview
             }
        return json.dumps(ans,indent=4).replace('\n', '\r\n')
    
    