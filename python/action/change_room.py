import json
from system.helper import i18n

class action_change_room(object):
    
    def __init__(self, json = False):
        self.data =  {  "class": "action_change_room",
                        "include": "action.change_room",
                        "command": {},
                        "description": {},
                        "roomid": 0
                     }
        if json is not False:
            self.fromJSON(json)
            
    def execute_action(self,player,msg):
        if 'roomid' in self.data:
            player.enter_room(self)
    
    def parse_user_command(self, player, msg):
        if msg.startswith(i18n(player.lang,self.data['command'])):
            self.execute_action(player, msg)
            return True
        return False
    
    def get_user_command(self,player):
        return  i18n(player.lang, self.data['command'])
    
    def get_action_description(self,player):
        return  i18n(player.lang, self.data['description'])
    
    def fromJSON(self, json):
        self.data["command"] = json["command"]
        self.data["description"] = json["description"]
        self.data["roomid"] = json["roomid"]
    
    def toJSON(self):
        return json.dumps(self.data,indent=4).replace('\n', '\r\n')
    