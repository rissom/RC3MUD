import json
import string
import tornado
from game.room import Room
from system.helper import i18n
from system.log import log

class Player(object):
    
    actions = [ { "command": { "de": "sage"  , "en": "say" } ,
                 "function" : "action_say",
                "description":  { "de": "sagt", "en": "says" },
                "help":  { "de": "'sage <text>' wird von allen Personen im selben Raum erhört.", "en": "'say <text>' will be heard from all persons in the same room." }
                },
                { "command": { "de": "umbenennen"  , "en": "rename" } ,
                 "function" : "action_rename",
                "description":  { "de": "heisst jetzt", "en": "is now known as" },
                "help": { "de": "##tbdb##", "en": "##tbdb##" }
                },
                { "command": { "de": "wer bin ich"  , "en": "whoami" } ,
                 "function" : "action_whoami",
                "description":  { "de": "heisst jetzt", "en": "is now known as" },
                "help": { "de": "##tbdb##", "en": "##tbdb##" }
                },
                { "command": {  "en": "room2json" } ,
                 "function" : "action_room2json",
                "description":  { "en": "" },
                "help": { "de": "##tbdb##", "en": "##tbdb##" }
                },
                { "command": {  "en": "look", "de": "schaue" } ,
                 "function" : "action_look",
                "description":  { "en": "" },
                "help": { "de": "##tbdb##", "en": "##tbdb##" }
                },
                { "command": {  "en": "sleep", "de": "schlafe" } ,
                 "function" : "action_sleep",
                "description":  { "en": "You feel refrehed!", "de":"Du fühlst Dich erholt!" },
                "help": { "de": "##tbdb##", "en": "##tbdb##" }
                },
                { "command": {  "en": "help", "de": "hilfe" } ,
                 "function" : "action_help",
                "description":  { "en": "try 'help <command>'... Use TAB key to see/extend commands.", "de":"versuche 'hilfe <Kommando>'... Benutze die Tabulatortaste, um Kommandos zu sehen und zu ergänzen." },
                "help": { "de": "Setz Dich und nimm Dir nen Keks!", "en": "Have a cookie." }
                },
                { "command": {  "en": "language", "de": "Sprache" } ,
                 "function" : "action_language",
                "description":  { "en": "Your language is set to English now.", "de": "Deine Sprache ist jetzt auf Deutsch eingestellt." },
                "help": { "de": "Setzt die Sprache ( de oder en )", "en": "sets your language.( de or en )." }
                }
              ]
    
    def __init__(self, wsclient):
        self.wsclient = wsclient
        self.name = "Bernd"
        self.room = Room.get_room_by_id(1)
        self.room.player.append(self)
        self.lang = "en"
        
#        self.enter_room({ "command": { "en": "from nowhere"} ,
#                                           "description":  { "en": "to nowhere" },
#                                           "roomid": 1
#                                         })
    
    def send_text(self, text):
        ans = {
              "cmd": "text",
              "data": text
            }
        try:
            self.wsclient.write_message(ans)
        except tornado.websocket.WebSocketClosedError:
            from system.websocket import Websocket
            try:
                Websocket.websocket_clients.remove(self.wsclient)
            except:
                log.error("uuh, wsclient not in not in list, haeh?")
    '''
        actions
        
    '''
    def action_room2json(self,a,msg,parameter):
        self.send_text("\r\n"+self.room.toJSON())
    
    def action_language(self,a,msg,parameter):
        if parameter=="en":
            self.lang = "en"
        if parameter=="de":
            self.lang = "de"
        self.send_player_new_command_list()
        self.send_text(i18n(self.lang,a['description']))
 
    def action_say(self,a,msg,parameter):
        for p in self.room.player:
            p.send_text(self.name+" "+i18n(p.lang,a['description'])+" '"+msg[ len(i18n(self.lang,a['command']))+1:]+"'")
    
    def action_sleep(self,a,msg,parameter):
        self.send_text(i18n(self.lang,a['description']))
        
    def action_help(self,a,msg,parameter):
        if len(msg.split())<2:
            self.send_text(i18n(self.lang,a['description']))
            return
        for a in Player.actions:
            if msg[5:].startswith(i18n(self.lang,a['command'])):
                self.send_text(i18n(self.lang,a['help']))
                return
    
    def action_rename(self,a,msg,parameter):
        newname = msg[ len(i18n(self.lang,a['command']))+1:]
        if len(newname)<3:
            self.send_text(i18n(self.lang,{ "en":"Thats to short...", "de": "Das ist zu kurz..."}))
            return
        
        for p in self.room.player:
            p.send_text(self.name+" "+i18n(p.lang,a['description'])+" '"+newname+"'")
        self.name = newname
       
    def action_whoami(self,a,msg,parameter):
        self.send_text("You are "+self.name)
        
    def action_look(self,a,msg,parameter):
        self.send_room_actions(self.room)
        self.send_player_new_command_list()
        self.send_other_players_in_room(self.room)
        
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
    
    def send_room_actions(self,room):
        if len(room.actions) == 0:
            actionsstring = i18n(self.lang, { "en": "There is nothing you can do here, sorry...", "de": "Hier kannst Du leider nichts tun..."})
        else:
            actionsstring = ""
            for a in room.actions:
                actionsstring = actionsstring + i18n(self.lang, a['description'])+"\r\n"
                
        self.send_text("\r\n\r\n"+i18n(self.lang,room.description)+"\r\n"+actionsstring)
        ans = {
              "cmd": "html",
              "data": i18n(self.lang,room.webview)
            }
        self.wsclient.write_message(ans)
        if  room.videoview:
            ans = {
              "cmd": "video",
              "enabled": True,
              "data": i18n(self.lang,room.videoview)
            }
            self.wsclient.write_message(ans)
        else:
            ans = {
              "cmd": "video",
              "enabled": False
            }
            self.wsclient.write_message(ans)
            
    def send_other_players_in_room(self,room):
        if len(room.player)==1:
            self.send_text(i18n(self.lang, { "en": "You are here on your own...", "de": "Du bist hier ganz alleine..."}))
        elif len(room.player)<10:
            playerstr = ""
            numberofplayers = 0
            for p in room.player:
                if p.name != self.name:
                  playerstr = playerstr+p.name+" "
                  numberofplayers=numberofplayers+1
            if numberofplayers==1:
                self.send_text(i18n(self.lang, { "en": playerstr+"is idling here..."}))
            else:
                self.send_text(i18n(self.lang, { "en": playerstr+"are idling here..."}))
        else:
            self.send_text(i18n(self.lang, { "en": "Many people are idling here..."}))
            
    def enter_room(self, roomaction):
        
        roomid = roomaction['roomid']
        newroom = Room.get_room_by_id(roomid)
        if self in self.room.player:
            self.room.player.remove(self)
        for p in self.room.player:
            p.send_text(i18n(p.lang,{ "en": ""+self.name+" leaves the room..."+i18n(self.lang,roomaction['command']) } ))
        
        # enter the room, first notification then enter
        enteraction = None
        for a in newroom.actions:
            if 'roomid' in a and a['roomid']==self.room.roomid:
                enteraction = a
        if enteraction is None:
            for p in newroom.player:
                p.send_text(i18n(p.lang,{ "en": ""+self.name+" enters the room with a puff of smoke..." }))
        else:
            for p in newroom.player:
                p.send_text(i18n(p.lang,{ "en": ""+self.name+" enters the room..."+i18n(self.lang,enteraction['command']) }))

        newroom.player.append(self)
        
        self.send_room_actions(newroom)
        self.room = newroom
        self.send_player_new_command_list()
        self.send_other_players_in_room(self.room)
        
    def parse_user_command(self, msg):
        
        answered = False
        
        for a in Player.actions:
            if msg.startswith(i18n(self.lang,a['command'])):
                parameter = msg[ len(i18n(self.lang,a['command']))+1:]
                getattr(self,a['function'])(a,msg, parameter)
                answered = True

        if not answered:
            answered = self.room.parse_user_command(self, msg)
        if not answered:
            self.send_text(i18n(self.lang,{ "en":"What you mean by '","de":"Was meinst Du mit '"})+msg+i18n(self.lang,{"en":"'? Try 'help' and remember: The TAB-key has always been your friend!","de":"'? Versuche 'hilfe' und erinnere Dich: Die TAB-Taste war schon immer Dein bester Freund!"}))
            
    def ws_disconnect(self):
        for p in self.room.player:
            p.send_text(i18n(p.lang,{ "en": ""+self.name+" disconnects..." } ))
        log.debug("player "+self.name+" disconnects.")
        self.room.player.remove(self)

