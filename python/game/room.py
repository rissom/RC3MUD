import json
from system.serializer import Serializer
from system.log import log
from system.helper import i18n
from game.area import Area

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
        self.areaid = 0    # area object to determine admins
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
        
    def get_room_command_list(self,player):
        commands = []
        for a in self.actions:
            commands.append(a.get_user_command(player))
        return commands
        
    def execute_action(self,player,action):
        if 'roomid' in action:
            player.enter_room(action)
        
    def parse_user_command(self, player, msg):
        for a in self.actions:
            if a.parse_user_command(player,msg):
                return True
        if msg.startswith("roomeditor"):
            if Area.get_area_by_id(self.areaid).are_ids_in_chain(player.admin_for_area):
                data = { "roomid" : self.roomid,
                   "areaid": self.areaid,
                   "actions" : [],
                   "name" : self.name,
                   "description" : self.description,
                   "items" : self.items,
                   "capacity" : self.capacity,
                   "webview" : self.webview,
                   "videoview" : self.videoview
                 }
                for a in self.actions:
                    data["actions"].append(a.toJSON())
                ans = { "cmd": "editroom",
                       "data": data }
                player.wsclient.write_message(ans)
                return True
        if msg.startswith("saveroom"):
            room = Room(99)
            Serializer.save_room(room)
            return True
        
        return False
        
    def fromJSON(self, json):
        
        self.areaid = json["areaid"]
        self.description = json["description"]
        #self.actions = json["actions"]
        self.name = json["name"]
        
        self.capacity = json["capacity"]
        if "webview" in json:
            self.webview = json["webview"]
        else:
            self.webview = { "en":"" }
        if "videoview" in json and "en" in json["videoview"]:
            self.videoview = json["videoview"]
        else:
            self.videoview = { "en":"" }
        self.actions = []
        from action.change_room import action_change_room
        for a in json["actions"]:
            self.actions.append(action_change_room(a))
        
        if "iframeurl" in json:
            self.iframe_url=json["iframeurl"]
        else:
            self.iframe_url=""
        if "iframehtml" in json:
            self.iframe_url=json["iframehtml"]
        else:
            self.iframe_html='<body><div id="videoview" style="width: 400px; height: 225px;" class="">'
            #self.iframe_html=self.iframe_html+'<iframe width="400" height="225" allow="autoplay" src="https://media.ccc.de/v/36c3-11223-opening_ceremony/oembed" frameborder="0" allowfullscreen=""></iframe>'
            self.iframe_html=self.iframe_html+self.videoview["en"]
            self.iframe_html=self.iframe_html+'</div><div id="webview" style="width: 400px; height: 50%;">'
            #self.iframe_html=self.iframe_html+'<h1>Opening Ceremony</h1>bleeptrack and blinry'
            self.iframe_html=self.iframe_html+self.webview["en"]
            self.iframe_html=self.iframe_html+'</div></body>'
            self.iframe_html = { "en": self.iframe_html }
        
    def toJSON(self):
        ans = { "roomid" : self.roomid,
               "areaid": self.areaid,
               "actions" : self.actions,
               "name" : self.name,
               "description" : self.description,
               "items" : self.items,
               "capacity" : self.capacity,
               "webview" : self.webview,
               #"videoview" : self.videoview
             }
        return json.dumps(ans,indent=4).replace('\n', '\r\n')
    
    