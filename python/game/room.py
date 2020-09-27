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
        self.actions = [ { "command": {} ,
                           "description":  {  },
                           "roomid": 0
                         }
                        ]
        self.name = "__undefined__"
        self.description = { "de": "Irgendetwas lief total schief...\r\n...ein unangenehmer, aber doch vertrauter Zustand...\r\n...für den es viele Wörter gibt: Null, Void, NaN...",
                            "en": "Something went terribly wrong...\r\n...and now you ended up in a frightening but familiar state...\r\n...there are many names for this: null, void, NaN..."}
        self.items = []
        
        self.capacity = -1
        self.webview = { "en": "null", "de": "null" }
    
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
        self.name = json["name"]
        self.webview = json["webview"]
        self.capacity = json["capacity"]
        if "videoview" in json:
            self.videoview = json["videoview"]
        else:
            self.videoview = False
        
    def toJSON(self):
        ans = { "roomid" : self.roomid,
               "actions" : self.actions,
               "name" : self.name,
               "description" : self.description,
               "items" : self.items,
               "capacity" : self.capacity,
               "webview" : self.webview,
               "videoview" : self.videoview
             }
        return json.dumps(ans,indent=4).replace('\n', '\r\n')
    
    