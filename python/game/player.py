import json


class Player(object):
    
    def __init__(self):
        self.name = "Bernd"
        
        #TODO: self.location
        
    def parse_user_command(self, wsclient, msg):
        
        if msg.startswith("whoami"):
            ans = {
              "cmd": "text",
              "data": "You are "+self.name
            }
            wsclient.write_message(json.dumps(ans))
        elif msg.startswith("sleep"):
            ans = {
              "cmd": "text",
              "data": "You feel refreshed"
            }
            wsclient.write_message(json.dumps(ans))
        else:
            ans = {
              "cmd": "text",
              "data": "What you mean by '"+msg+"'"
            }
            wsclient.write_message(json.dumps(ans))